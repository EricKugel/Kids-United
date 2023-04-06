from flask import current_app as app
from flask import Flask, redirect, url_for, render_template, request, flash

from flask_login import login_required, logout_user, current_user, login_user

from . import login_manager

from .models import db, User
from.forms import SignupForm, LoginForm

@app.route("/get-to-know-me", methods = ["GET", "POST"])
def get_to_know_me():
#   form = SignupForm()
#   if form.validate_on_submit():
#     username = request.form["username"]
#     email = request.form["email"]
#     if username and email:
#         user_exists = User.query.filter(User.username == username or User.email == email).first()
#         if user_exists:
#           RuntimeError("ruh roh")
#         new_user = User(username = username, email = email, created = dt.now(), admin = False)
#         db.session.add(new_user)
#         db.session.commit()
#     return redirect(url_for("success"))
  return render_template("get_to_know_me.jinja2")
  
@app.route("/", methods=["GET"])
def get_index():
  return redirect(url_for("get_page"))

@app.route("/success")
def success():
  return render_template("success.jinja2", users = User.query.all())

@app.route("/take-a-breath")
@app.route("/scheduling")
@app.route("/blog")
@app.route("/about-us")
def get_page():
  page = request.path.replace("-", "_").replace("/", "")
  return render_template(page + ".jinja2")

@app.route("/upcoming-projects")
@login_required
def upcoming_projects():
  return render_template("upcoming_projects.jinja2")

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
def loadd_user(user_id):
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

app.run(host='0.0.0.0', port=8080)
