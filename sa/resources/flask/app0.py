from flask import Flask

app = Flask(__name__)

@app.route("/")
def hola():
    return "<p>¡Hola IABD desde Flask!</p>"