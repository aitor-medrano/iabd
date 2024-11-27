from flask import Flask
from flask import render_template

from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo import ASCENDING

import db

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/listar")
def listado():
    midb = db.get_db()
    coleccion = midb.usuarios
    usuarios = list(coleccion.find({}).sort("nombre", ASCENDING))

    return render_template("listado.html", lista=usuarios)

@app.route("/hola")
def hola():
    frase = "¡Hola IABD desde Flask!"
    return render_template("resultado.html", mensaje=frase)

@app.route("/adios")
def adios():
    frase = "¡Adios IABD desde Flask!"
    return render_template("resultado.html", mensaje=frase)
