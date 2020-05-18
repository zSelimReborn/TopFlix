import requests
import os
import json
from .adapters import TitleFactory, GenreFactory

class ApiError(Exception):
    pass

class Api(object):
    def __init__(self):
        self.api_url = self.retrieve_api_url()
        self.api_key = self.retrieve_api_key()
        self.req = requests.request
    
    def retrieve_api_url(self):
        pass
    def retrieve_api_key(self):
        pass
    def before_get(self, url, **kwargs):
        pass
    def after_get(self, url, result):
        pass
    def build_url(self, path):
        pass
    def build_headers(self, data):
        pass

    def _get(self, path, **kwargs):
        url = self.build_url(path)

        self.before_get(url, **kwargs)
        self.build_headers(kwargs)
        result = self.req("GET", url, **kwargs)
        if (result.status_code != 200):
            raise ApiError(result)

        self.after_get(url, result)
        
        return result
    

class NetflixApi(Api):
    API_URL_PATH = "NETFLIX_API_URL"
    API_KEY_PATH = "NETFLIX_API_KEY"
    TITLE_SEARCH_ENDPOINT = "search"
    GENRE_SEARCH_ENDPOINT = "genres"
    TITLE_GENRE_SEARCH_ENDPOINT = "titlegenres"

    RAPIDAPI_HOST = "unogsng.p.rapidapi.com"

    def retrieve_api_url(self):
        return os.environ.get(self.API_URL_PATH).strip("/")

    def retrieve_api_key(self):
        return os.environ.get(self.API_KEY_PATH).strip("/")
    
    def build_url(self, path):
        path = path.strip("/")
        return self.api_url + "/" + path
    
    def build_headers(self, data):
        headers = {
            'x-rapidapi-host': self.RAPIDAPI_HOST,
            'x-rapidapi-key': self.api_key
        }

        data["headers"] = headers
    
    def title_search(self, **kwargs):
        response = self._get(self.TITLE_SEARCH_ENDPOINT, **kwargs)
        titles = response.json()["results"]
        titles_adapted = []

        for title in titles:
            title_adapted = TitleFactory.make(title)
            titles_adapted.append(title_adapted)
        
        return titles_adapted


    def genre_search(self):
        response = self._get(self.GENRE_SEARCH_ENDPOINT)
        genres = response.json()["results"]
        genres_adapted = []

        for genre in genres:
            genre_adapted = GenreFactory.make(genre)
            genres_adapted.append(genre_adapted)
        
        return genres_adapted
    
    def genre_by_title(self, netflix_id):
        query = {"netflixid": netflix_id}
        response = self._get(self.TITLE_GENRE_SEARCH_ENDPOINT, params=query)
        
        genres = response.json()["results"]
        genres_adapted = []

        for genre in genres:
            genre_adapted = GenreFactory.make(genre)
            genres_adapted.append(genre_adapted)
        
        return genres_adapted
    
