from app.auth import bp
from flask import request, escape, render_template, redirect, flash, url_for, jsonify
from app.auth.forms import LoginForm, RegisterForm, EditProfileForm, RequestPasswordForm, ResetPasswordForm
from app.auth.models import User
from flask_login import current_user, login_user, logout_user, login_required
from app.auth.email import send_request_password_email

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        try:
            user = User.login(email, password)
        except:
            flash('Invalid Username or Password')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.homepage'))

    return render_template('auth/user/login.html', title="Login", form=form)

@bp.route("/register", methods=["GET", "POST"])
def register():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('main.homepage'))
        form = RegisterForm()
        if form.validate_on_submit():
            nUser = User.register(form)
            flash('Register confirmed for user {}'.format(
                nUser.email))
            return redirect(url_for('main.homepage'))
        return render_template('auth/user/register.html', title="Register", form=form)
    except Exception as e:
        print("Sono qui in exception")
        return jsonify({"error": str(e)})

@bp.route("/logout")
def logout():
    logout_user()
    flash('Logout effettuato')
    return redirect(url_for('main.homepage'))

@bp.route("/user/<id>")
@login_required
def view_user(id):
    user = User.get_by_id(id)
    if user is None:
        flash("User not exists")
        return redirect(url_for("main.homepage"))

    return render_template("auth/user/view.html", user=user)

@bp.route("/user/edit", methods=['GET', 'POST'])
@login_required
def edit_user():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        current_user.save()
        flash("Information saved correctly")
        return redirect(url_for("auth.view_user", username=current_user.username))
    elif request.method == 'GET':
        form.email.data = current_user.email if current_user.email else ''
        form.about_me.data = current_user.about_me if current_user.about_me else ''
        
    return render_template("auth/user/edit.html", title="Edit Profile", form=form)

@bp.route("/user/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("auth.view_user", id=current_user.id))
    form = RequestPasswordForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user:
            send_request_password_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for("auth.login"))
    return render_template("auth/user/reset_password_request.html", title="Reset Password", form=form)

@bp.route("/user/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.homepage'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.save()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/user/reset_password.html', form=form)
