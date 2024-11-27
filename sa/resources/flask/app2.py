from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hola")
def hola():
    frase = "¡Hola IABD desde Flask!"
    return render_template("resultado.html", mensaje=frase)

@app.route("/adios")
def adios():
    frase = "¡Adios IABD desde Flask!"
    return render_template("resultado.html", mensaje=frase)
