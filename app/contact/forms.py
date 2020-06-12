from flask import url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, InputRequired

class ContactForm(FlaskForm):
    fullname = StringField('Nome e Cognome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField("Oggetto", validators=[DataRequired()])
    message = TextAreaField("Messaggio", validators=[DataRequired()])
    submit = SubmitField("Invia Messaggio")

