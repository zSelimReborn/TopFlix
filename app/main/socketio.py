from app import socketio
from flask_socketio import Namespace, emit

from app.models import Title, Genre
from app.main.models import Discussion
from flask import request, escape, render_template, redirect, flash, url_for, jsonify, current_app, g
from flask_login import current_user

import json
import html
from datetime import datetime
from time import time

class DiscussionNamespace(Namespace):
    def on_connect(self):
        print("Client connected")
        pass

    def on_disconnect(self):
        print("Client disconnected")
        pass

    def on_answer_new(self, data):
        discussion_id = data.get("discussion_id")
        discussion = Discussion.get_by_id(discussion_id)
        
        try:
            self.__validate_data(data)
            n_answer = Discussion(
                title="",
                description=data.get("description"),
                created_at=datetime.now,
                parent=data.get("title_parent_id"),
                author=current_user.id,
                is_answer=True
            )

            n_answer.save()
            discussion.answers.append(n_answer)
            discussion.save()

            answer_block = render_template("discussion/answer/_view.html", answer=n_answer)
            response = {"success": True, "message": "Risposta aggiunta correttamente", "new_answer_block": answer_block}
        except Exception as e:
            response = {"success": False, "message": str(e)}
        
        response["discussion_id"] = discussion_id
        response["user_id"] = str(current_user.id)
        emit("answer created", response, broadcast=True)
    
    def __validate_data(self, data):
        title_id = data.get("title_parent_id")
        if title_id is None:
            raise Exception("Titolo non trovato")
        
        discussion_id = data.get("discussion_id")
        discussion = Discussion.get_by_id(discussion_id)
        if discussion is None:
            raise Exception("Discussione non trovata")  

