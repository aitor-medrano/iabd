from pymongo import MongoClient
from flask import g

def get_db():

    db = getattr(g, "_database", None)

    MONGODB_URI = "mongodb://prelara:pr3l4r4m3c@27.0.172.67/"
    MONGODB_DB_NAME = "prelara"

    if db is None:
        db = g._database = MongoClient(
            MONGODB_URI,
            maxPoolSize=50,
            timeoutMS=2500
       )[MONGODB_DB_NAME]
        
    return db