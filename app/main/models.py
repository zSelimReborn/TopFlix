from flask import escape, current_app
from app import db

class ReviewPoint(db.Document):
    PROS_ID = 1
    CONS_ID = 0

    content = db.StringField()
    role = db.BooleanField()
    parent = db.ObjectIdField()

class Review(db.Document):
    title = db.StringField()
    content = db.StringField()
    rating = db.DecimalField(min_value=1, max_value=10, precision=1)
    titleparent = db.ObjectIdField()
    author = db.ObjectIdField()
    points = db.ListField(db.ReferenceField(ReviewPoint))

    @staticmethod
    def get_by_id(id):
        return Review.objects.get(id=id)
    
    @staticmethod
    def get_by_title(title):
        reviews = Review.objects.filter(titleparent=title.id)
        return reviews
    
    @staticmethod
    def get_by_title_id(title_id):
        title = Title.get_by_id(title_id)
        return Review.get_by_title(title)