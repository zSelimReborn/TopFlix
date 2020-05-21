import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook

facebook_bp = make_facebook_blueprint()

@facebook_bp.route("/")
def fb_login():
    if not facebook.authorized:
        return redirect(url_for("facebook.login"))
    resp = facebook.get("/me/feed")
    return (resp.text, str(resp.ok))
    return "You are {name} on Facebook".format(name=resp.json()["name"])
