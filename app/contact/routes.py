from flask import request, escape, render_template, redirect, flash, url_for, jsonify, current_app, g
from app.contact import bp 
from flask_login import current_user, login_required
from app.contact.forms import ContactForm
from app.contact.email import send_contact_email
from app.auth.forms import LoginForm, RegisterForm, RequestPasswordForm

@bp.before_request
def inject_user_forms():
    g.login_form = LoginForm()
    g.register_form = RegisterForm()
    g.reset_form = RequestPasswordForm()


@bp.route("/", methods=["GET", "POST"])
def new_contact():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        send_contact_email(contact_form)
        flash("Messaggio inviato correttamente")
        return redirect(url_for("main.homepage"))
    
    return render_template("contact/index.html", form=contact_form)