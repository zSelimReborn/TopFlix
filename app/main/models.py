from flask import escape, current_app
from app import db

from app.auth.models import User

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
    recommended = db.BooleanField()

    @staticmethod
    def get_by_id(id):
        try:
            return Review.objects.get(id=id)
        except:
            return None
    
    @staticmethod
    def get_by_title(title):
        reviews = Review.objects.filter(titleparent=title.id)
        return reviews
        
    @staticmethod
    def get_avg_rating(title):
        reviews = Review.get_by_title(title)

        avg = 0
        review_count = reviews.count()
        if review_count <= 0:
            return 0
        
        for review in reviews:
            avg += review.rating
        
        return avg / review_count

    def get_author(self):
        try:
            return User.get_by_id(self.author)
        except:
            return None
    
    def is_author(self, user):
        author = self.get_author()
        return author.id == getattr(user, "id", "")
    
    def __query_points(self, point_type):
        p = []
        for point in self.points:
            if point.role == point_type:
                p.append(point)
        return p
    
    def pros(self):
        return self.__query_points(ReviewPoint.PROS_ID)
    
    def cons(self):
        return self.__query_points(ReviewPoint.CONS_ID)
    
    def pros_as_string(self):
        pros = self.pros()
        pros_string = []
        for pro in pros:
            pros_string.append(pro.content)
        
        return pros_string
    
    def cons_as_string(self):
        cons = self.cons()
        cons_string = []
        for con in cons:
            cons_string.append(con.content)
        
        return cons_string

    def remove_all_points(self):
        for point in self.points:
            point.delete
        
        self.points = []
        
    def put_pros(self, pros):
        pros_object = []
        for pro in pros:
            pro_obj = ReviewPoint(
                content=pro,
                role=ReviewPoint.PROS_ID,
                parent=self.id
            )

            pro_obj.save()
            pros_object.append(pro_obj)
        
        self.points = pros_object
    
    def add_pros(self, pros):
        for pro in pros:
            pro_obj = ReviewPoint(
                content=pro,
                role=ReviewPoint.PROS_ID,
                parent=self.id
            )

            pro_obj.save()
            self.points.append(pro_obj)
    
    def put_cons(self, cons):
        cons_object = []
        for con in cons:
            con_obj = ReviewPoint(
                content=con,
                role=ReviewPoint.CONS_ID,
                parent=self.id
            )

            con_obj.save()
            cons_object.append(con_obj)
        
        self.points = cons_object
    
    def add_cons(self, cons):
        for con in cons:
            con_obj = ReviewPoint(
                content=con,
                role=ReviewPoint.CONS_ID,
                parent=self.id
            )

            con_obj.save()
            self.points.append(con_obj)

class Upvote(db.Document):
    user_id = db.ObjectIdField()
    value = db.IntField()
    parent = db.ObjectIdField()

class Discussion(db.Document):
    title = db.StringField()
    description = db.StringField()
    created_at = db.DateTimeField()
    answers = db.ListField(db.ReferenceField('Discussion', reverse_delete_rule=db.PULL))
    parent = db.ObjectIdField()

    upvotes = db.ListField(db.ReferenceField('Upvote'))

    author = db.ObjectIdField()
    is_answer = db.BooleanField()

    @staticmethod
    def get_by_id(id):
        try:
            return Discussion.objects.get(id=id)
        except:
            return None

    @staticmethod
    def get_by_title(title):
        discussions = Discussion.objects.filter(parent=title.id)
        return discussions
    
    def get_author(self):
        return User.objects.get(id=self.author)

    def is_author(self, user):
        author = self.get_author()
        return author.id == getattr(user, "id", "")

    def delete_all_answers(self):
        if not self.is_answer:
            for answer in self.answers:
                answer.delete()
    
    def delete_all_upvotes(self):
        for upvote in self.upvotes:
            upvote.delete()

    def upvotes_count(self):
        return Upvote.objects.filter(parent=self.id).count()
    
    def upvotes_value(self):
        return Upvote.objects.filter(parent=self.id).sum("value")
    
    def has_upvoted(self, user_id):
        for upvote in self.upvotes:
            if upvote.user_id == user_id:
                if (upvote.value == 1):
                    return True, "upvote", upvote
                else:
                    return True, "downvote", upvote
        
        return False, "", None
    
    def manage_upvote(self, user_id, value):
        has_upvoted, upvote_type, upvote = self.has_upvoted(user_id)

        if not has_upvoted:
            upvote = Upvote(
                user_id=user_id,
                value=value,
                parent=self.id
            )

            upvote.save()            
            self.upvotes.append(upvote)

            self.save()
            return self.upvotes_value()
        
        if upvote.value != value:
            upvote.value = value
            upvote.save()
            self.save()
        else:
            self.update(pull__upvotes=upvote)
            upvote.delete()
        
        return self.upvotes_value()
        
class Survey(db.Document):
    unique_key      = db.StringField(unique=True)
    template_path   = db.StringField()
    users_done      = db.ListField(db.ReferenceField(User))
    mandatory       = db.BooleanField()

    @staticmethod
    def get_by_id(id):
        try:
            survey = Survey.objects.get(id=id)
            return survey
        except:
            return None

    @staticmethod
    def get_by_unique_key(unique_key):
        try:
            survey = Survey.objects.filter(unique_key=unique_key).first()
            return survey
        except:
            return None
    
    def user_already_compiled(self, user):
        survey = Survey.objects.filter(id=self.id, users_done__contains=user.id)
        return survey.count() >= 1
    
    def user_not_compiled(self, user):
        return not self.user_already_compiled(user)