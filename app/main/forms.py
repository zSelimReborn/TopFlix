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
