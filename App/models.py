from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

import os
import base64
from io import BytesIO

class User(UserMixin, db.Model):
    __tablename__ = "flasklogin-users"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = False, unique = False, nullable = False)
    email = db.Column(db.String(80), index = True, unique = True, nullable = False)
    password = db.Column(db.String(200), primary_key = False, unique = False, nullable = False)
    country = db.Column(db.String(100), index = False, unique = False, nullable = False)
    pronouns = db.Column(db.String(64), index = False, unique = False, nullable = False)
    admin = db.Column(db.Boolean, index = False, unique = False, nullable = False)

    def set_password(self, password):
        self.password = generate_password_hash(password, method = "sha256")
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def __repr__(self):
        return "User " + str(self.name)
    
class Bio(db.Model):
    __tablename__ = "bios"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, index = False, unique = False, nullable = False)
    email = db.Column(db.String(80), index = True, unique = True, nullable = False)
    name = db.Column(db.String(64), index = False, unique = False, nullable = False)
    country = db.Column(db.String(100), index = False, unique = False, nullable = False)
    bio = db.Column(db.Text, index = False, unique = False, nullable = True)
    photo = db.Column(db.String(100), index = False, unique = False, nullable = True)
    pronouns = db.Column(db.String(64), index = False, unique = False, nullable = False)
    title = db.Column(db.String(32), index = False, unique = False, nullable = True)

    phone = db.Column(db.String(20), index = False, unique = False, nullable = True)
    ig = db.Column(db.String(20), index = False, unique = False, nullable = True)
    snap = db.Column(db.String(20), index = False, unique = False, nullable = True)

class Blog(db.Model):
    __tablename__ = "blogs"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, index = False, unique = False, nullable = False)
    name = db.Column(db.String(64), index = False, unique = False, nullable = False)
    email = db.Column(db.String(80), index = False, unique = False, nullable = False)
    country = db.Column(db.String(100), index = False, unique = False, nullable = True)
    blog = db.Column(db.Text, index = False, unique = False, nullable = False)
    
    photo0 = db.Column(db.String(100), index = False, unique = False, nullable = True)
    photo1 = db.Column(db.String(100), index = False, unique = False, nullable = True)
    photo2 = db.Column(db.String(100), index = False, unique = False, nullable = True)
    youtube = db.Column(db.String(100), index = False, unique = False, nullable = True)
    date = db.Column(db.String(100), index = False, unique = False, nullable = False)

class Request(db.Model):
    __tablename__ = "requests"
    id = db.Column(db.Integer, primary_key = True, unique = True, nullable = False)
    email0 = db.Column(db.String(80), index = False, unique = False, nullable = False)
    email1 = db.Column(db.String(80), index = False, unique = False, nullable = False)
    time = db.Column(db.String(80), index = False, unique = False, nullable = False)
    message = db.Column(db.Text, index = False, unique = False, nullable = False)