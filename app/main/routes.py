from functools import wraps

from flask import request, escape, render_template, redirect, flash, url_for, jsonify, current_app
from app.main import bp 
from flask_login import current_user, login_required

import json
import html
from datetime import datetime
from time import time

from app.auth.models import User
from app.models import *
from app.main.tasks import process_netflix_api
from app.main.models import Review, Survey
from app.main.forms import AddReviewForm, EditReviewForm, AddDiscussionForm, EditDiscussionForm, AnswerDiscussionForm, EditAnswerDiscussionForm

from .survey import SurveySwitchForm

''' function eseguita dopo che un utente completa il login '''
def check_survey_mandatory(function):
    @wraps(function)
    def wrapper(**kwargs):
        if current_user.is_authenticated:
            mandatory_surveys = Survey.objects.filter(mandatory=True)
            for survey in mandatory_surveys:
                if survey.user_not_compiled(current_user):
                    return redirect(url_for("main.show_survey", unique_key=survey.unique_key))

        return function(**kwargs)
    return wrapper

@bp.route("/")
@check_survey_mandatory
def homepage():
    #process_netflix_api()   
    #recommended_by_genre = Title.recommended_by_genre()
    #recommended_by_title = Title.recommended_by_title()

    last_movies = Title.get_last_movies()
    last_series = Title.get_last_series()
    last_movies_imported = Title.get_last_titles_imported()

    total_films = Title.get_all_movies().count()
    total_series = Title.get_all_series().count()
    total_users = User.objects.count()

    return render_template("homepage.html", body_classes="homepage", header_classes="header-fixed header-transparent text-white", 
        user=current_user,
        total_films=total_films, total_series=total_series, total_users=total_users,
        last_movies=last_movies, last_series=last_series, last_movies_imported=last_movies_imported)

@bp.route("/title")
@check_survey_mandatory
def list_title():
    titles = Title.objects()
    return render_template("title/list.html", titles=titles)

@bp.route("/title/<id>")
@check_survey_mandatory
def view_title(id):
    title = Title.get_by_id(id)
    if title is None:
        abort(404)

    reviews = Review.get_by_title(title)
    review_form = AddReviewForm(request.values, title_parent_id=str(title.id))
    review_form.custom_action = url_for('main.add_review')

    discussion_form = AddDiscussionForm(request.values, title_parent_id=str(title.id))
    discussion_form.custom_action = url_for("main.add_discussion")

    answer_form = AnswerDiscussionForm(request.values, title_parent_id=str(title.id))

    return render_template("title/view.html", title=html.unescape(title.name), t=title, reviews=reviews, review_form=review_form, discussion_form=discussion_form, answer_form=answer_form)

@bp.route("/title/review/add", methods=["POST"])
@login_required
def add_review():
    review_form = AddReviewForm()
    if not review_form.validate_on_submit():
        print(review_form.errors)
        flash("Richiesta non valida")
        return redirect(url_for("main.list_title"))
    
    title_parent_id = review_form.title_parent_id.data
    title_parent = Title.get_by_id(title_parent_id)
    if title_parent is None:
        flash("Titolo non trovato")
        return redirect(url_for("main.list_title"))
    
    n_review = Review(
        title=(review_form.title.data),
        content=(review_form.content.data),
        rating=review_form.rating.data,
        titleparent=title_parent.id,
        author=current_user.id,
        recommended=review_form.recommended.data
    )

    n_review.save()

    n_review.add_pros(review_form.pros.data)
    n_review.add_cons(review_form.cons.data)

    n_review.save()
    flash("Recensione aggiunta correttamente")
    return redirect(url_for("main.view_title", id=title_parent_id))

@bp.route("/title/review/<review_id>/remove")
@login_required
def remove_review(review_id):
    review = Review.get_by_id(review_id)
    if review is None:
        flash("Recensione non trovata")
        return redirect(url_for("main.list_title"))
    
    title_id = review.titleparent
    if not review.is_author(current_user):
        flash("Non è possibile cancellare recensioni di altri utenti")
        return redirect(url_for("main.view_title", id=title_id))
    

    review.delete()
    flash("Recensione eliminata correttamente")
    return redirect(url_for("main.view_title", id=title_id))

@bp.route("/title/review/<review_id>/edit", methods=["GET", "POST"])
@login_required
@check_survey_mandatory
def edit_review(review_id):
    review = Review.get_by_id(review_id)
    if review is None:
        flash("Recensione non trovata")
        return redirect(url_for("main.list_title"))
    
    title_id = review.titleparent
    if not review.is_author(current_user):
        flash("Non è possibile modificare recensioni di altri utenti")
        return redirect(url_for("main.view_title", id=title_id))

    review_form = EditReviewForm()
    if not review_form.validate_on_submit():
        review_form.title.data = review.title
        review_form.content.data = review.content
        review_form.rating.data = review.rating
        review_form.recommended.data = review.recommended

        for pros in review.pros_as_string():
            review_form.pros.append_entry(pros)
        
        for cons in review.cons_as_string():
            review_form.cons.append_entry(cons)

        return render_template("review/edit.html", title="Modifica recensione {name}".format(name=review.title), review_form=review_form)

    
    review.title = review_form.title.data
    review.content = review_form.content.data
    review.rating = review_form.rating.data
    review.recommended = True if review_form.recommended.data == 1 else False
    review.remove_all_points()

    review.add_pros(review_form.pros.data)
    review.add_cons(review_form.cons.data)
    review.save()

    flash("Recensione modificata correttamente")
    return redirect(url_for("main.view_title", id=title_id))

    
@bp.route("/title/discussion/add", methods=["POST"])
@login_required
def add_discussion():
    discussion_form = AddDiscussionForm()

    if not discussion_form.validate_on_submit():
        print(discussion_form.errors)
        flash("Richiesta non valida")
        return redirect(url_for("main.list_title"))

    title_parent_id = discussion_form.title_parent_id.data
    title_parent = Title.get_by_id(title_parent_id)
    if title_parent is None:
        flash("Titolo non trovato")
        return redirect(url_for("main.list_title"))

    n_discussion = Discussion(
        title=(discussion_form.title.data),
        description=(discussion_form.description.data),
        created_at=datetime.now,
        parent=title_parent_id,
        author=current_user.id,
        is_answer=False
    )

    n_discussion.save()
    flash("Discussione aggiunta correttamente")
    return redirect(url_for("main.view_title", id=title_parent_id))

@bp.route("/title/discussion/<discussion_id>/remove")
@login_required
def remove_discussion(discussion_id):
    discussion = Discussion.get_by_id(discussion_id)
    if discussion is None:
        flash("Discussione non trovata")
        return redirect(url_for("main.list_title"))
    
    title_id = discussion.parent
    if not discussion.is_author(current_user):
        flash("Non è possibile eliminare discussioni di altri utenti")
        return redirect(url_for("main.view_title", id=title_id))
    
    discussion.delete_all_answers()
    discussion.delete_all_upvotes()
    discussion.delete()

    flash("Discussione eliminata correttamente")
    return redirect(url_for("main.view_title", id=title_id))

@bp.route("/title/discussion/<discussion_id>/edit", methods=["GET", "POST"])
@login_required
@check_survey_mandatory
def edit_discussion(discussion_id):
    discussion = Discussion.get_by_id(discussion_id)
    if discussion is None:
        flash("Discussione non trovata")
        return redirect(url_for("main.list_title"))
    
    title_id = discussion.parent
    if not discussion.is_author(current_user):
        flash("Non è possibile modificare discussioni di altri utenti")
        return redirect(url_for("main.view_title", id=title_id))
    
    discussion_form = EditDiscussionForm()
    if not discussion_form.validate_on_submit():
        discussion_form.title.data = discussion.title
        discussion_form.description.data = discussion.description

        return render_template("discussion/edit.html", discussion_form=discussion_form)

    discussion.title = discussion_form.title.data
    discussion.description = discussion_form.description.data

    discussion.save()
    flash("Discussione modificata correttamente")
    return redirect(url_for("main.view_title", id=title_id))


@bp.route("/title/discussion/<discussion_id>/answer/add", methods=["POST"])
@login_required
def add_answer(discussion_id):
    answer_form = AnswerDiscussionForm()
    if not answer_form.validate_on_submit():
        print(answer_form.errors)
        flash("Richiesta non valida")
        return redirect(url_for("main.list_title"))
    
    title_parent_id = answer_form.title_parent_id.data
    title_parent = Title.get_by_id(title_parent_id)
    if title_parent is None:
        flash("Titolo non trovato")
        return redirect(url_for("main.list_title"))

    try:
        discussion = Discussion.get_by_id(discussion_id)
    except:
        flash("Discussione non trovata")
        return redirect(url_for("main.view_title", id=title_parent_id))
    
    if discussion is None:
        flash("Discussione non trovata")
        return redirect(url_for("main.view_title", id=title_parent_id))

    n_answer = Discussion(
        title="",
        description=answer_form.description.data,
        created_at=datetime.now,
        parent=title_parent_id,
        author=current_user.id,
        is_answer=True
    )

    n_answer.save()
    discussion.answers.append(n_answer)

    discussion.save()
    flash("Risposta aggiunta correttamente")
    return redirect(url_for("main.view_title", id=title_parent_id))

@bp.route("/title/discussion/answer/<answer_id>/edit", methods=["GET", "POST"])
@login_required
@check_survey_mandatory
def edit_answer(answer_id):
    answer = Discussion.get_by_id(answer_id)
    if answer is None:
        flash("Risposta non trovata")
        return redirect(url_for("main.list_title"))
    
    title_id = answer.parent
    if not answer.is_author(current_user):
        flash("Non è possibile modificare risposte di altri utenti")
        return redirect(url_for("main.view_title", id=title_id))
    
    answer_form = EditAnswerDiscussionForm()
    if not answer_form.validate_on_submit():
        answer_form.description.data = answer.description
        answer_form.custom_action = url_for("main.edit_answer", answer_id=answer_id)

        return render_template("discussion/answer/edit.html", answer_form=answer_form, discussion=None)
    
    answer.description = answer_form.description.data
    answer.save()

    flash("Risposta modificata correttamente")
    return redirect(url_for("main.view_title", id=title_id))
    

@bp.route("/title/discussion/<discussion_id>/upvotes/add", methods=["POST"])
@login_required
def add_upvote(discussion_id):
    response = {}
    discussion = Discussion.get_by_id(discussion_id)
    if discussion is None:
        response["error"] = "Discussione {d} non trovata".format(d=str(discussion_id))
        return response
    
    value = int(request.values.get("upvote_value"))
    upvotes = discussion.manage_upvote(current_user.id, value)
    response = {
        "success": True, 
        "value": upvotes
    }
    
    return response

@bp.route("/title/<title_id>/like")
@login_required
def toggle_like(title_id):
    title = Title.get_by_id(title_id)
    if title is None:
        flash("Titolo non trovato")
        return redirect(url_for("main.list_title"))
    
    like = request.args.get("like") == "1"

    
    current_user.manage_titles(title, like)
    return redirect(url_for("main.view_title", id=title.id))
        
@bp.route("/survey/<unique_key>", methods=["GET", "POST"])
@login_required
def show_survey(unique_key):
    survey = Survey.get_by_unique_key(unique_key)
    if survey is None:
        flash("Sondaggio non disponibile")
        return redirect(url_for("main.homepage"))

    if survey.user_already_compiled(current_user):
        flash("Sondaggio già completato")
        return redirect(url_for("main.homepage"))

    survey_helper = SurveySwitchForm()

    info = survey_helper.get_info(unique_key)
    if info is None:
        flash("Sondaggio non trovato")
        return redirect(url_for("main.homepage"))
    
    form_class, function = info["form"], info["on_submit"]
    
    form = form_class(survey_id=str(survey.id))

    if form.validate_on_submit():
        function(form)
        return redirect(url_for(form.return_url_for))
    
    return render_template(survey.template_path, form=form)


@bp.errorhandler(404)
def handle_notfound(e):
    return "Non trovato"

@bp.errorhandler(403)
def handle_exception(e):
    result = str(e)
    return json.dumps({"Exception: ": result})

@bp.errorhandler(500)
def handle_errors(e):
    result = str(e)
    return result, 500