from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

import os
import base64
from io import BytesIO

class User(UserMixin, db.Model):
    __tablename__ = "flasklogin-users"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = False, unique = True, nullable = False)
    email = db.Column(db.String(80), index = True, unique = True, nullable = False)
    password = db.Column(db.String(200), primary_key = False, unique = False, nullable = False)
    country = db.Column(db.String(100), index = False, unique = False, nullable = True)
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
    email = db.Column(db.String(80), index = True, unique = True, nullable = False)
    bio = db.Column(db.Text, index = False, unique = False, nullable = False)
    photo = db.Column(db.String(100), index = False, unique = False, nullable = True)

    phone = db.Column(db.String(20), index = False, unique = False, nullable = True)
    ig = db.Column(db.String(20), index = False, unique = False, nullable = True)
    snap = db.Column(db.String(20), index = False, unique = False, nullable = True)

def render_picture(data):
    render_pic = base64.b64encode(data).decode("ascii")