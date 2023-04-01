from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")


@app.route("/secret-url")
def secret():
  return "Nice! You found the secret url!"


@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")


app.run(host='0.0.0.0', port=8080)
