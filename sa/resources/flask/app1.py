from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hola")
def hola():
    return "<p>¡Hola IABD desde Flask!</p>"

@app.route("/adios")
def adios():
    return "<p>¡Adios IABD desde Flask!</p>"