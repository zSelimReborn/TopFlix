from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.auth.models import User

from flask import url_for

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def get_action(self):
        return url_for("auth.login")

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name')
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Registrati")

    def get_action(self):
        return url_for("auth.register")

    def validate_email(self, email):
        u = User.get_by_email(email.data)
        if u is not None:
            raise ValidationError("Email already taken")

class EditProfileForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    about_me = TextAreaField("About Me")
    submit = SubmitField("Send")

class RequestPasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Invia")
    def get_action(self):
        return url_for("auth.reset_password_request")

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')