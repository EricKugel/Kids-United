from flask import current_app as app
from flask import redirect, url_for, render_template, request, flash, make_response

from flask_login import login_required, logout_user, current_user, login_user

from flask_uploads import UploadSet, configure_uploads, IMAGES

from . import login_manager

from .models import db, User, Bio, render_picture
from .forms import SignupForm, LoginForm, BioForm, PHOTOS

from .zoom import generate_meeting
from .gmail import send_email

import os

UPLOAD_DEST = os.path.abspath(os.path.dirname(__file__))

configure_uploads(app, PHOTOS)

@app.before_first_request
def start_db():
  db.create_all()

@app.route("/", methods=["GET"])
def get_index():
  return redirect(url_for("get_page"))

@app.route("/scheduling")
@app.route("/scheduling/")
def scheduling():
  meeting = generate_meeting()
  send_email("erickugel713@gmail.com")
  return render_template("scheduling.jinja2", url = meeting[0], password = meeting[1])

@app.route("/take-a-breath")
@app.route("/blog")
@app.route("/about-us")
def get_page():
  page = request.path.replace("-", "_").replace("/", "")
  return render_template(page + ".jinja2")

@app.route("/upcoming-projects")
@login_required
def upcoming_projects():
  return render_template("upcoming_projects.jinja2", users = User.query.all())

@app.route("/success")
def success():
  return render_template("success.jinja2", users = User.query.all())

@app.route("/get-to-know-me", methods = ["GET", "POST"])
@login_required
def get_to_know_me():
  form = BioForm()
  existing_bio = Bio.query.filter_by(email = current_user.email).first()
  if form.validate_on_submit():
    url = url_for("upload", filename = PHOTOS.save(form.photo.data)) if form.photo else None
    if existing_bio:
      existing_bio.bio = form.bio.data
      existing_bio.photo = url
      existing_bio.phone = form.phone.data
      existing_bio.ig = form.ig.data
      existing_bio.snap = form.snap.data
    else:
      bio = Bio(email = current_user.email, name = current_user.name, country = current_user.country, bio = form.bio.data, photo = url, ig = form.ig.data, snap = form.snap.data)
      db.session.add(bio)
    db.session.commit()
    return redirect(url_for("get_index"))
  return render_template("get_to_know_me.jinja2", form = form, existing_bio = existing_bio, bios = Bio.query.all())

@app.route("/get-to-know-me/<email>")
@app.route("/get-to-know-me/<email>/")
def get_to_know_them(email):
  bio = Bio.query.filter_by(email = email).first()
  return render_template("get_to_know_them.jinja2", bio = bio)

@app.route("/get-to-know-me/all")
@app.route("/get-to-know-me/all/")
def get_to_know_everybody():
  bios = Bio.query.all()
  return render_template("get_to_know_everybody.jinja2", bios = bios)

@app.route("/signup", methods = ["GET", "POST"])
def signup():
  form = SignupForm()
  if form.validate_on_submit():
    existing_user = User.query.filter_by(email = form.email.data).first()
    if existing_user is None:
      user = User(name = form.name.data, email = form.email.data, country = form.country.data, admin = False)
      user.set_password(form.password.data)
      db.session.add(user)
      db.session.commit()
      login_user(user)
      return redirect(url_for("get_index"))
    flash("That email is taken. Forgot password?")
  return render_template("signup.jinja2", form = form)

@app.route("/login", methods = ["GET", "POST"])
def login():
  if current_user.is_authenticated:
    return redirect(url_for("get_index"))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email = form.email.data).first()
    if user and user.check_password(password = form.password.data):
      login_user(user)
      next_page = request.args.get("next")
      return redirect(next_page or url_for("get_index"))
    flash("Password incorrect")
    return redirect(url_for("login"))
  return render_template("login.jinja2", form = form)

@login_manager.user_loader
def load_user(user_id):
  if user_id is not None:
    return User.query.get(user_id)
  return None

@login_manager.unauthorized_handler
def unauthorized():
  flash("You must be logged in to access that page")
  return redirect(url_for("login"))

@app.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for("login"))

@app.route("/upload/<filename>")
@app.route("/upload/<filename>/")
def upload(filename):
  if "/" in filename or "\\" in filename:
    return "Please stop trying to do a file traversal attack. Not cool."
  fullpath = "App/upload/" + filename
  resp = make_response(open(fullpath, "rb").read())
  resp.content_type = "image/" + fullpath.split(".")[-1]
  return resp

app.debug = True
app.run(host = "0.0.0.0", port = "8080")