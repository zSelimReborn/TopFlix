from flask import request, escape, render_template, redirect, flash, url_for, jsonify
from app.main import bp 
import json
import html

from app.models import *
from app.main.tasks import process_netflix_api

@bp.route("/")
def homepage():
    #process_netflix_api()   

    return jsonify("json")

@bp.errorhandler(404)
def handle_exception(e):
    result = str(e)
    return json.dumps({"Exception: ": result})

@bp.errorhandler(500)
def handle_errors(e):
    result = str(e)
    return result, 500