from app.api.client import NetflixApi, ApiError
from app.models import Title, Genre

import os

def create_file_not_exists(filename):
    if not os.path.exists(filename):
        with open(filename, 'w'): 
            pass


def write_offset(offset):
    file_location = os.environ.get("FILE_OFFSET_LOCATION") or None
    if file_location is not None:
        with open(file_location, mode="w") as writer:
            writer.write(offset)

def read_offset():
    file_location = os.environ.get("FILE_OFFSET_LOCATION") or None
    if file_location is not None:
        create_file_not_exists(file_location)
        with open(file_location, mode="r") as reader:
            offset = reader.read()
            if offset.strip() == "" or offset is None:
                return 0
            return int(offset)
    
    return 0


def process_netflix_api():
    api = NetflixApi()
    
    offset = read_offset()
    querystring = {
        "country_andorunique":"unique",
        "start_year":"1972",
        "orderby":"rating",
        "limit":"10",
        #"countrylist":"269",
        #"audio":"italian",
        "offset": offset,
        "end_year":"2020",
        "type": "series"
    }

    try: 
        titles = api.title_search(params=querystring)
    except ApiError as e:
        print(str(e))
        return False

    for title in titles:
        genres = api.genre_by_title(title.get_netflixid())

        t = Title.create_by_adapter(title, genres)
        print("MongoId: %s - Name: %s" % (t.id, t.name))
        for genre in t.genres:
            print("GenreID: %s - Name: %s" % (genre.id, genre.name))
    

    write_offset(str(offset + 10))

