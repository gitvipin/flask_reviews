#!/usr/bin/env python

# from flask_login import LoginManager
# from flask_session import Session
from flask_jwt_extended import JWTManager
from sql30 import db

# Create JSON WEB TOKEN app
jwt = JWTManager()

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {
        # 'username': '',
        'guest': identity['guest'],
        'uid': identity['uid']
    }

class ReviewsDB(db.Model):
    TABLE = 'reviews'
    PKEY = 'rid'
    DB_SCHEMA = {
        'db_name': './reviews.db',
        'tables': [
            {
                'name': TABLE,
                'fields': {
                    'rid': 'uuid',
                    'header': 'text',
                    'rating': 'int',
                    'desc': 'text'
                    },
                'primary_key': PKEY
            }]
        }
    VALIDATE_BEFORE_WRITE = True

class Reviews(ReviewsDB):

    def create_all(self):
        with Reviews() as _db:
            pass

reviews_db = Reviews()