from os import getenv
from flask_sqlalchemy import SQLAlchemy
from app import app

dburl = getenv("DATABASE_URL")
if dburl.startswith("postgres://"):
    dburl = dburl.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = dburl
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #to get rid of warning
db = SQLAlchemy(app)