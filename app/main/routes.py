from flask import request, escape, render_template, redirect, flash, url_for, jsonify
from app.main import bp 
from flask_login import current_user, login_required
import json
import html

from app.models import *
from app.main.tasks import process_netflix_api
from app.main.models import Review
from app.main.forms import AddReviewForm

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
    return render_template("title/view.html", title=title.name, t=title, reviews=reviews, review_form=review_form)

@bp.route("/title/add", methods=["POST"])
@login_required
def add_review():
    review_form = AddReviewForm()
    if not review_form.validate_on_submit():
        flash("Richiesta non valida")
        return redirect(url_for("main.list_title"))
    
    title_parent_id = review_form.title_parent_id.data
    title_parent = Title.get_by_id(title_parent_id)
    if title_parent is None:
        flash("Titolo non trovato")
        return redirect(url_for("main.list_title"))
    
    n_review = Review(
        title=review_form.title.data,
        content=review_form.content.data,
        rating=review_form.rating.data,
        titleparent=title_parent.id,
        author=current_user.id
    )

    n_review.save()
    flash("Recensione aggiunta correttamente")
    return redirect(url_for("main.view_title", id=title_parent_id))
    

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