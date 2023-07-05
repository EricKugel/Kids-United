from flask_wtf import FlaskForm

from wtforms import PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileField, FileAllowed

class SignupForm(FlaskForm):
    name = StringField("Name", [DataRequired()])
    email = StringField("Email", [Email(message = "Not a valid email"), DataRequired()])
    password = PasswordField("Password", [DataRequired(), Length(min = 6, message = "Make it longer please")])
    confirm = PasswordField("Confirm Password", [DataRequired(), EqualTo("password", message = "Passwords don't match")])
    country = StringField("Country", [DataRequired()])
    pronouns = StringField("Pronouns", [DataRequired()])
    submit = SubmitField("Sign up")

class LoginForm(FlaskForm):
    email = StringField("Email", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField("Log in")

PHOTOS = UploadSet("photos", IMAGES)

class BioForm(FlaskForm):
    title = StringField("Title")
    bio = TextAreaField("Tell us a little bit about yourself!", [DataRequired()])
    photo = FileField("Upload picture, cropped to square (optional)", [FileAllowed(PHOTOS, "File must be an image")])
    phone = StringField("Phone number")
    ig = StringField("Instagram")
    snap = StringField("Snap")
    submit = SubmitField("Update")

class BlogForm(FlaskForm):
    blog = TextAreaField("Write something for the blog!", [DataRequired("Write something")])
    
    photo0 = FileField("Photo 1", [FileAllowed(PHOTOS, "File must be an image")])
    photo1 = FileField("Photo 2", [FileAllowed(PHOTOS, "File must be an image")])
    photo2 = FileField("Photo 3", [FileAllowed(PHOTOS, "File must be an image")])
    
    youtube = StringField("Link to youtube video (optional)")
    submit = SubmitField("Post")

class ElevateForm(FlaskForm):
    password = PasswordField("Secret Code", [DataRequired()])
    submit = SubmitField("Submit")

class RequestForm(FlaskForm):
    time = StringField("Time, date, and timezone", [DataRequired()])
    message = TextAreaField("Message", [DataRequired()])
    submit = SubmitField("Submit Request")