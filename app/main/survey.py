from flask import request, flash
from .forms import SurveyGenreForm
from app.models import Genre
from app.auth.models import User
from app.main.models import Survey
from flask_login import current_user

class SurveyGenreManager(object):
    @staticmethod
    def on_submit_form(form):
        survey = Survey.get_by_id(form.survey_id.data)
        if survey is None:
            flash("Sondaggio non trovato")
            return False
        
        genres_liked = form.genres_liked.data

        user = User.get_by_id(current_user.id)
        for genre_id in genres_liked:
            genre = Genre.get_by_id(genre_id)
            if genre is None:
                continue
            
            user.genres_liked.append(genre)

        survey.users_done.append(user)
        survey.save()

        user.save()
        flash("Sondaggio completato correttamente. Grazie per la tua attenzione!")
        return True

class SurveySwitchForm(object):
    def __init__(self):
        self.switch = {
            "genre_liked_survey": {"form": SurveyGenreForm, "on_submit": SurveyGenreManager.on_submit_form}
        }
    
    def get_info(self, unique_key):
        return self.switch.get(unique_key)
