from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo

class AddReviewForm(FlaskForm):
    title_parent_id = HiddenField("Titolo di riferimento")
    title = StringField('Titolo', validators=[DataRequired()])
    content = TextAreaField('Contenuto Recensione', validators=[DataRequired()])
    rating = StringField("Valutazione", validators=[DataRequired()])
    submit = SubmitField('Scrivi Recensione')
