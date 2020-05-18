from flask import request, escape, render_template, redirect, flash, url_for, jsonify
from app.main import bp 
import json
import html

from app.models import *
from app.main.tasks import process_netflix_api

@bp.route("/")
def homepage():
    #process_netflix_api()        
    titles = Title.query.all()
    d = []
    for title in titles:
        t = {
            "id": title.netflix_id,
            "name": html.unescape(title.name),
            "description": html.unescape(title.description)
        }

        d.append(t)
    return jsonify(d)

@bp.errorhandler(Exception)
def handle_exception(e):
    result = str(e)
    return json.dumps({"Exception: ": result})