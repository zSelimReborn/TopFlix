import random

from flask import escape, current_app, url_for
from app import db
from app.api.adapters import TitleAdapter, GenreAdapter
from datetime import datetime
from time import time
from flask_login import current_user

from app.main.models import Review, Discussion
from app.auth.models import User

class Genre(db.Document):
    netflix_id = db.StringField()
    name = db.StringField()
    meta = {'collection': 'Genre'}

    def get_image(self):
        titles = Title.objects.filter(genres__contains=self)
        skip_random = random.randint(0, titles.count())

        title_sample = titles.skip(skip_random).first()

        if title_sample is not None:
            return title_sample.title_poster()
        return url_for('static', filename='images/movie_default.png')

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
        return '/'.join(str(genre.name) for genre in self.genres[0:3])

    def watch_link(self):
        base_url = "https://www.netflix.com/title/{net_id}"

        return base_url.format(net_id=self.netflix_id)

    def title_poster(self):
        if self.poster is None or self.poster.strip() == "N/A" or self.poster.strip() == "None":
            return url_for('static', filename='images/movie_default.png')

        return self.poster
        
    def detail_link(self):
        return url_for("main.view_title", id=self.id, _external=True)

    def reviews(self):
        return Review.get_by_title(self)
    
    def get_reviews_count(self):
        return self.reviews().count()

    def discussions(self):
        return Discussion.get_by_title(self)
        
    def rating_average(self):
        return Review.get_avg_rating(self)
    
    def rating_average_stars(self):
        rating_avg = self.rating_average()
        return (rating_avg * 5) / 10
    
    def build_rating_stars(self):
        rating_avg = self.rating_average_stars()
        stars_count = 0
        content_html = ""

        for i in range(0, int(rating_avg)):
            content_html += "<i class='fa fa-star'></i>"
            stars_count += 1
        
        limit_stars = 5
        if int(rating_avg) != rating_avg:
            content_html += "<i class='fa fa-star-half-o'></i>"
            limit_stars = 4
        
        for i in range(stars_count, limit_stars):
            content_html += "<i class='fa fa-star-o'></i>"
        
        return content_html
    

    @staticmethod
    def get_random_collection(limit=8):
        total_count = Title.objects.count()
        skip = random.randint(0, total_count)

        return Title.objects.skip(skip).limit(limit)

    @staticmethod
    def get_last_movies(limit=8):
        return Title.objects.filter(title_type="movie").order_by('-year').limit(limit)
    
    @staticmethod
    def get_last_series(limit=8):
        return Title.objects.filter(title_type="series").order_by('-year').limit(limit)
    
    @staticmethod
    def get_last_titles_imported(limit=3):
        return Title.objects.order_by('inserted_at').limit(limit)

    @staticmethod
    def get_genres_by_titles(titles_id):
        titles = Title.objects.filter(id__in=titles_id).only("genres").as_pymongo()
        genres_id = {}
        for title in titles:
            for genre in title["genres"]:
                genres_id[genre] = 1
        
        return [*genres_id]

    @staticmethod
    def recommended_by_genre(limit=8):
        if not current_user.is_authenticated:
            return []
        
        if len(current_user.genres_liked) <= 0:
            return []
        
        genres = current_user.genres_liked
        titles_disliked = current_user.titles_disliked_as_id()

        titles = Title.objects.filter(id__nin=titles_disliked, genres__in=genres)

        if len(titles) > limit:
            skip_random = random.randint(0, limit)
            titles = titles.skip(skip_random).limit(limit)
        
        return titles
    
    @staticmethod
    def recommended_by_title(limit=8):
        if not current_user.is_authenticated:
            return []
        
        if len(current_user.titles_liked) <= 0:
            return []
        
        # Prendo id titoli piaciuti e non piaciuti dall'utente
        titles_liked_id = current_user.titles_liked_as_id()
        titles_disliked_id = current_user.titles_disliked_as_id()

        # Prendo gli id dei generi dei titoli piaciuti all'utente
        all_genres = Title.get_genres_by_titles(titles_liked_id)

        # Filtro
        titles = Title.objects.filter(id__nin=titles_liked_id + titles_disliked_id, genres__in=all_genres)

        if len(titles) > limit:
            skip_random = random.randint(0, limit)
            titles = titles.skip(skip_random).limit(limit)
            
        return titles
    
    @staticmethod
    def get_all_movies():
        return Title.objects.filter(title_type="movie")
    
    @staticmethod
    def get_all_series():
        return Title.objects.filter(title_type="series")