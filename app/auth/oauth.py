import os
from flask import Flask, redirect, url_for, current_app
from rauth import OAuth2Service
import json

class FacebookLogin(object):
    def __init__(self, token=None):
        self.service = OAuth2Service(
            client_id=current_app.config["FACEBOOK_OAUTH_CLIENT_ID"],
            client_secret=current_app.config["FACEBOOK_OAUTH_CLIENT_SECRET"],
            name='facebook',
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )

        self.set_token(token)
        self.internal_session = None

    @staticmethod
    def decode_json(payload):
        return json.loads(payload.decode('utf-8'))
    
    def get_authorize_url(self):
        redirect_uri = url_for("auth.fb_callback", _external=True)
        params = {
            'scope': 'email,user_gender',
            'response_type': 'code',
            'redirect_uri': redirect_uri
        }

        return self.service.get_authorize_url(**params)
    
    def set_token(self, token):
        self.token = token
    
    def get_token(self):
        return self.token

    def session(self):
        if self.internal_session is not None:
            return self.internal_session
        
        self.internal_session = self.service.get_auth_session(
            data={
                'code': self.get_token(), 
                'gran_type': 'authorization_code', 
                'redirect_uri': url_for("auth.fb_callback", _external=True)
            },
            decoder=FacebookLogin.decode_json
        )
        #me = oauth_session.get("me?fields=id,name,email,age_range").json()

        return self.internal_session

