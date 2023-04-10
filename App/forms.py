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
    country = StringField("Country")
    submit = SubmitField("Sign up")

class LoginForm(FlaskForm):
    email = StringField("Email", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField("Log in")

PHOTOS = UploadSet("photos", IMAGES)

class BioForm(FlaskForm):
    bio = TextAreaField("Tell us a little bit about yourself!", [DataRequired()])
    photo = FileField("Upload picture (optional)", [FileAllowed(PHOTOS, "File must be an image")])
    phone = StringField("Phone number")
    ig = StringField("Instagram handle")
    snap = StringField("Snap")
    submit = SubmitField("Submit")