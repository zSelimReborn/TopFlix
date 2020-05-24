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
    recommended = db.BooleanField()

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
        
    def put_pros(self, pros):
        pros_object = []
        for pro in pros:
            pro_obj = ReviewPoint(
                content=escape(pro),
                role=ReviewPoint.PROS_ID,
                parent=self.id
            )

            pro_obj.save()
            pros_object.append(pro_obj)
        
        self.points = pros_object
    
    def add_pros(self, pros):
        for pro in pros:
            pro_obj = ReviewPoint(
                content=escape(pro),
                role=ReviewPoint.PROS_ID,
                parent=self.id
            )

            pro_obj.save()
            self.points.append(pro_obj)
    
    def put_cons(self, cons):
        cons_object = []
        for con in cons:
            con_obj = ReviewPoint(
                content=escape(con),
                role=ReviewPoint.CONS_ID,
                parent=self.id
            )

            con_obj.save()
            cons_object.append(con_obj)
        
        self.points = cons_object
    
    def add_cons(self, cons):
        for con in cons:
            con_obj = ReviewPoint(
                content=escape(con),
                role=ReviewPoint.CONS_ID,
                parent=self.id
            )

            con_obj.save()
            self.points.append(con_obj)