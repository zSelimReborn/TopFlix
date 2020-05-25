from flask import request, escape, render_template, redirect, flash, url_for, jsonify
from app.main import bp 
from flask_login import current_user, login_required

import json
import html
from datetime import datetime
from time import time

from app.models import *
from app.main.tasks import process_netflix_api
from app.main.models import Review
from app.main.forms import AddReviewForm, AddDiscussionForm, AnswerDiscussionForm


@bp.route("/")
def homepage():
    #process_netflix_api()   

    return render_template("homepage.html", user=current_user)

@bp.route("/title")
def list_title():
    titles = Title.objects
    return render_template("title/list.html", titles=titles)

@bp.route("/title/<id>")
def view_title(id):
    title = Title.get_by_id(id)
    if title is None:
        abort(404)

    reviews = Review.get_by_title(title)
    review_form = AddReviewForm(request.values, title_parent_id=str(title.id))
    review_avg = Review.get_avg_rating(title)

    discussion_form = AddDiscussionForm(request.values, title_parent_id=str(title.id))
    answer_form = AnswerDiscussionForm(request.values, title_parent_id=str(title.id))

    return render_template("title/view.html", title=title.name, t=title, reviews=reviews, review_form=review_form, review_avg=review_avg, discussion_form=discussion_form, answer_form=answer_form)

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