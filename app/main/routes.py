from flask import request, escape, render_template, redirect, flash, url_for, jsonify
from app.main import bp 
from flask_login import current_user
import json
import html
import os

from app.models import *
from app.main.tasks import process_netflix_api

@bp.route("/")
def homepage():
    #process_netflix_api()   

    return render_template("homepage.html", user=current_user)

@bp.errorhandler(404)
def handle_exception(e):
    result = str(e)
    return json.dumps({"Exception: ": result})

@bp.errorhandler(500)
def handle_errors(e):
    result = str(e)
    return result, 500