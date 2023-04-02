from flask import Flask, redirect, url_for, render_template, request
import json

app = Flask(__name__)
users = []


@app.route("/get-to-know-me", methods=["POST"])
def post_get_to_know_me():
  global users
  name = request.form.get('username')
  users.append(name)
  with open("static/users.json", "w") as file:
    file.write(json.dumps(users))
  return render_template("success.html")


@app.route("/", methods=["GET"])
def get_index():
  return render_template("about_us.html")


@app.route("/take-a-breath")
@app.route("/scheduling")
@app.route("/blog")
@app.route("/get-to-know-me")
@app.route("/about-us")
@app.route("/upcoming-projects")
def get_page():
  page = request.path.replace("-", "_").replace("/", "")
  return render_template(page + ".html")


@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")


app.run(host='0.0.0.0', port=8080)
