from flask import escape, current_app
from app import db
from app.api.adapters import TitleAdapter, GenreAdapter
from datetime import datetime
from time import time

class Genre(db.Document):
    netflix_id = db.StringField()
    name = db.StringField()
    meta = {'collection': 'Genre'}

    @staticmethod
    def create_by_adapter(genre):
        genre = Genre(
            netflix_id=genre.get_netflixid(),
            name=genre.get_name()
        )

        genre.save()
        return genre
    
    @staticmethod
    def get_by_netflixid(nid):
        genre = Genre.objects.filter(netflix_id=nid).first()
        return genre
    
    @staticmethod
    def create_if_not_exists(genre):
        g = Genre.get_by_netflixid(genre.get_netflixid())
        if g is None:
            return Genre.create_by_adapter(genre)
        
        return g

class Title(db.Document):
    netflix_id = db.StringField()
    imdb_id = db.StringField()
    name = db.StringField()
    small_img = db.StringField()
    poster = db.StringField()
    description = db.StringField()
    year = db.IntField()
    title_type = db.StringField()
    genres = db.ListField(db.ReferenceField(Genre))
    inserted_at = db.StringField()
    meta = {'collection': 'Title'}

    @staticmethod
    def find_by_netflixid(nid):
        title = Title.objects.filter(netflix_id=nid).first()
        return title
    
    @staticmethod
    def associate_title_genre(title, genre):
        title.genres.append(genre)
        return title

    @staticmethod
    def create_by_adapter(title, genres=None):
        now = datetime.now().strftime('%d/%m/%Y')
        t = Title.find_by_netflixid(title.get_netflixid())
        if (t is None):
            t = Title(
                netflix_id=title.get_netflixid(),
                imdb_id=title.get_imdbid(),
                name=title.get_name(),
                small_img=title.get_small_img(),
                poster=title.get_poster(),
                description=title.get_description(),
                year=title.get_published_year(),
                title_type=title.get_type(),
                inserted_at=now
            )

        genres_created = []
        if genres is not None:
            for genre in genres:
                genre_created = Genre.create_if_not_exists(genre)
                genres_created.append(genre_created)
                #Title.associate_title_genre(t, genre_created)

        t.genres = genres_created
        t.save()
        return t