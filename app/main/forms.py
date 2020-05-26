from flask import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, HiddenField, FieldList, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, InputRequired

class AddReviewForm(FlaskForm):
    title_parent_id = HiddenField("Titolo di riferimento")
    title = StringField('Titolo', validators=[DataRequired()])
    content = TextAreaField('Contenuto Recensione', validators=[DataRequired()])
    rating = StringField("Valutazione", validators=[DataRequired()])
    pros = FieldList(StringField("Pro"))
    cons = FieldList(StringField("Contro"))
    recommended = SelectField('Consigliato', coerce=int, choices=[(0,"No"), (1,"Sì")])
    submit = SubmitField('Scrivi Recensione')

    def get_custom_action(self):
        return getattr(self, "custom_action", "")


class EditReviewForm(AddReviewForm):
    submit = SubmitField("Modifica recensione")
    

class AddDiscussionForm(FlaskForm):
    title_parent_id = HiddenField("Titolo di riferimento")
    title = StringField('Titolo', validators=[DataRequired()])
    description = TextAreaField('Contenuto discussione', validators=[DataRequired()])
    submit = SubmitField('Inizia discussione')

    def get_custom_action(self):
        return getattr(self, "custom_action", "")

class EditDiscussionForm(AddDiscussionForm):
    submit = SubmitField("Modifica discussione")

class AnswerDiscussionForm(FlaskForm):
    title_parent_id = HiddenField("Titolo di riferimento")
    description = TextAreaField('La tua risposta', validators=[DataRequired()])
    submit = SubmitField('Invia')

    def get_custom_action(self, discussion=None):
        custom_action = getattr(self, "custom_action", "")
        if custom_action == "":
            if discussion is not None:
                return url_for("main.add_answer", discussion_id=discussion.id)
        
        return custom_action

class EditAnswerDiscussionForm(AnswerDiscussionForm):
    submit = SubmitField("Modifica")
