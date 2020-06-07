import random

from flask import escape, current_app
from app import db
from app.api.adapters import TitleAdapter, GenreAdapter
from datetime import datetime
from time import time
from flask_login import current_user

from app.main.models import Review, Discussion

class Genre(db.Document):
    netflix_id = db.StringField()
    name = db.StringField()
    meta = {'collection': 'Genre'}

    @staticmethod
    def get_by_id(id):
        try:
            return Genre.objects.get(id=id)
        except:
            return None

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
    def get_by_id(id):
        try:
            return Title.objects.get(id=id)
        except:
            return None

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

        t.genres = genres_created
        t.save()
        return t
    
    def genres_as_string(self):
        return '/'.join(str(genre.name) for genre in self.genres)

    def watch_link(self):
        base_url = "https://www.netflix.com/title/{net_id}"

        return base_url.format(net_id=self.netflix_id)

    def reviews(self):
        return Review.get_by_title(self)

    def discussions(self):
        return Discussion.get_by_title(self)
        
    def rating_average(self):
        return Review.get_avg_rating(self)

    @staticmethod
    def recommended_by_genre(limit=8):
        if not current_user.is_authenticated:
            return []
        
        if len(current_user.genres_liked) <= 0:
            return []
        
        genres = current_user.genres_liked
        titles = Title.objects.filter(genres__in=genres)

        if len(titles) > limit:
            skip_random = random.randint(0, limit)
            titles = titles.skip(skip_random).limit(limit)
        
        return titles