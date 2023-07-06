from flask import current_app as app
from flask import redirect, url_for, render_template, request, flash, make_response, session, send_file

from flask_login import login_required, logout_user, current_user, login_user

from flask_uploads import configure_uploads

from . import login_manager

from .models import db, User, Bio, Blog, Request
from .forms import SignupForm, LoginForm, BioForm, BlogForm, ElevateForm, RequestForm, CodeForm, PHOTOS

import os
from datetime import datetime

UPLOAD_DEST = os.path.abspath(os.path.dirname(__file__))

configure_uploads(app, PHOTOS)

@app.before_first_request
def start_db():
  db.create_all()

@app.route("/")
def get():
  return redirect(url_for("get_index"))

@app.route("/about-us")
def get_index():
  directors = User.query.filter_by(admin = True)
  director_bios = []
  for director in directors:
    director_bios.append(Bio.query.filter_by(user_id = director.id).first())
  return render_template("static/about_us.jinja2", directors = director_bios) 

@app.route("/take-a-breath")
def take_a_breath():
  return render_template("static/take_a_breath.jinja2")

@app.route("/upcoming-projects")
def upcoming_projects():
  return render_template("static/upcoming_projects.jinja2")

@app.route("/success")
def success():
  return render_template("static/success.jinja2")

@app.route("/get-to-know-me/")
@app.route("/get-to-know-me", methods = ["GET", "POST"])
@login_required
def get_to_know_me():
  form = BioForm()
  existing_bio = Bio.query.filter_by(email = current_user.email).first()
  if form.validate_on_submit():
    url = None
    if request.files["photo"].filename != "":
      url = url_for("upload", filename = PHOTOS.save(form.photo.data))
    existing_bio.bio = form.bio.data
    if url:
      existing_bio.photo = url
    existing_bio.phone = form.phone.data
    existing_bio.ig = form.ig.data
    existing_bio.snap = form.snap.data
    existing_bio.title = form.title.data
    db.session.commit()
    return redirect(url_for("get_index"))
  form.bio.data = existing_bio.bio
  form.phone.data = existing_bio.phone
  form.ig.data = existing_bio.ig
  form.snap.data = existing_bio.snap
  form.title.data = existing_bio.title
  return render_template("get_to_know/get_to_know_me.jinja2", form = form, existing_bio = existing_bio, bios = Bio.query.all())


@app.route("/get-to-know-me/admin/<id>")
@app.route("/get-to-know-me/admin/<id>")
def get_to_know_admin(id):
  user = User.query.filter_by(id = id).first()
  if user.admin:
    bio = Bio.query.filter_by(email = user.email).first()
    return render_template("get_to_know/get_to_know_them.jinja2", bio = bio, admin = True)
  return("no")

@app.route("/get-to-know-me/<id>")
@app.route("/get-to-know-me/<id>/")
@login_required
def get_to_know_them(id):
  user = User.query.filter_by(id = id).first()
  bio = Bio.query.filter_by(email = user.email).first()
  return render_template("get_to_know/get_to_know_them.jinja2", bio = bio, admin = user.admin)

@app.route("/get-to-know-me/all")
@login_required
def get_to_know_everybody():
  bios = [r for r in Bio.query.filter_by(email = current_user.email)] + [r for r in Bio.query.filter(Bio.email.isnot(current_user.email))]
  return render_template("get_to_know/get_to_know_everybody.jinja2", bios = bios)

@app.route("/get-to-know-me/<id>/request", methods = ["GET", "POST"])
@login_required
def get_to_know_request(id):
  form = RequestForm()
  name = User.query.filter_by(id=id).first().name
  if form.validate_on_submit():
    email = User.query.filter_by(id = id).first().email
    time = form.time.data
    message = form.message.data
    request = Request(email0 = current_user.email, email1 = email, time = time, message = message)
    db.session.add(request)
    db.session.commit()
    return redirect(url_for("get_index"))
  return render_template("get_to_know/get_to_know_request.jinja2", form = form, id = id, name= name)

@app.route("/blog", methods = ["POST", "GET"])
@login_required
def blog():
  if request.method == "POST" and current_user.admin:
    id = request.json.get("id")
    Blog.query.filter_by(id = id).delete()
    db.session.commit()
    return ""
  blogs = Blog.query.order_by(Blog.id.desc())
  for blog in blogs:
    blog.photo = Bio.query.filter_by(user_id = blog.user_id).first().photo
  return render_template("blog/blog.jinja2", blogs = Blog.query.order_by(Blog.id.desc()))

@app.route("/blog/create", methods = ["GET", "POST"])
@login_required
def create():
  form = BlogForm()
  if form.validate_on_submit():
    url0, url1, url2 = None, None, None
    if request.files["photo0"].filename != "":
      url0 = url_for("upload", filename = PHOTOS.save(form.photo0.data))
    if request.files["photo1"].filename != "":
      url1 = url_for("upload", filename = PHOTOS.save(form.photo1.data))
    if request.files["photo2"].filename != "":
      url2 = url_for("upload", filename = PHOTOS.save(form.photo2.data))
    time = datetime.now()
    blog = Blog(email = current_user.email, name = current_user.name, country = current_user.country, user_id = current_user.id, blog = form.blog.data, photo0 = url0, photo1 = url1, photo2 = url2, youtube = form.youtube.data if form.youtube else None, date = time.strftime("%b. %d, %Y"))
    db.session.add(blog)
    db.session.commit()
    return redirect(url_for("get_index"))
  return render_template("blog/create.jinja2", form = form)

@app.route("/signup", methods = ["GET", "POST"])
def signup():
  form = SignupForm()
  if form.validate_on_submit():
    existing_user = User.query.filter_by(email = form.email.data).first()
    if existing_user is None:
      user = User(name = form.name.data, email = form.email.data, country = form.country.data, pronouns = form.pronouns.data, admin = False)
      user.set_password(form.password.data)
      db.session.add(user)
      db.session.commit()
      bio = Bio(name = user.name, email = user.email, user_id = user.id, country = user.country, pronouns = user.pronouns, photo = "/static/lib/pfp.jpg", bio = "No bio yet!")
      db.session.add(bio)
      db.session.commit()
      login_user(user)
      return redirect(url_for("get_index"))
    flash("That email is taken. Forgot password?")
  return render_template("user/signup.jinja2", form = form)

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
  return render_template("user/login.jinja2", form = form)

@app.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for("login"))

@app.route("/elevate", methods = ["GET", "POST"])
@login_required
def elevate():
  form = ElevateForm()
  if form.validate_on_submit():
    correct = ""
    with open("App/secret.txt") as file:
      correct = file.read().strip()
    if form.password.data == correct:
      current_user.admin = True
      bio = Bio.query.filter_by(user_id = current_user.id)
      bio.title = "Director"
      db.session.commit()
      return redirect(url_for("get_index"))
    flash("Incorrect code")
    return redirect(url_for("elevate"))
  return render_template("user/elevate.jinja2", form = form)

@login_manager.user_loader
def load_user(user_id):
  if user_id is not None:
    return User.query.get(user_id)
  return None

@login_manager.unauthorized_handler
def unauthorized():
  flash("You must be logged in to access that page")
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

@app.route("/admin", methods = ["POST", "GET"])
@login_required
def admin():
  if current_user.admin:
    if request.method == "POST":
      if "email" in request.json.keys():
        email = request.json["email"]
        User.query.filter_by(email = email).delete()
      else:
        id = request.json["id"]
        Request.query.filter_by(id = id).delete()
      db.session.commit()
      return ""
    return render_template("user/admin.jinja2", users = User.query.order_by(User.admin.desc()).all(), requests = Request.query.all())
  else:
    return "You're not an admin 🤨🤨🤨🤨🤨🤨🤨🤨🤨"

@app.route("/code", methods = ["POST", "GET"])
@login_required
def code():
  if current_user.admin:
    form = CodeForm()
    if form.validate_on_submit():
      code = form.code.data
      d = dict(locals(), **globals())
      exec(code, d, d)
      db.session.commit()
      return redirect(url_for("get_index"))
    return render_template("user/code.jinja2", form = form)
  else:
    return("go away")

@app.route("/database")
@login_required
def database():
  if current_user.admin:
    return send_file("database.db")
  return "Okay"  

app.debug = True
app.run(host = "0.0.0.0", port = "8080")