import json

class TitleFactory(object):
    @staticmethod
    def make(obj):
        if "vtype" in obj and obj["vtype"] == "movie":
            return MovieAdapter(obj)
        elif obj["vtype"] == "series" or obj["vtype"] == "show":
            return SeriesAdapter(obj)
        
        return None

class TitleAdapter(object):
    def __init__(self, json_object):
        self.object = json_object
    
    def get_type(self):
        return str(self.object["vtype"])
    
    def get_small_img(self):
        return str(self.object["img"])
    
    def get_netflixid(self):
        return str(self.object["nfid"])
    
    def get_imdbid(self):
        return str(self.object["imdbid"])

    def get_name(self):
        return str(self.object["title"])
    
    def get_poster(self):
        return str(self.object["poster"])
    
    def get_description(self):
        return str(self.object["synopsis"])
    
    def get_published_year(self):
        return int(self.object["year"])

class MovieAdapter(TitleAdapter):
    def get_type(self):
        return "movie"
    
class SeriesAdapter(TitleAdapter):
    def get_type(self):
        return "series"

class GenreFactory(object):
    @staticmethod
    def make(obj):
        return GenreAdapter(obj)

class GenreAdapter(object):
    def __init__(self, obj):
        self.object = obj
    
    def get_name(self):
        return str(self.object["genre"])
    
    def get_netflixid(self):
        if "netflixid" in self.object:
            nid = self.object["netflixid"]
        if "nfid" in self.object:
            nid = self.object["nfid"]
        else:
            nid = -1
            
        return str(nid)