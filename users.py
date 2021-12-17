from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def user_id():
    return session.get("user_id", False)

def login(username, password):
    sql = "SELECT user_id, password FROM Users WHERE username=:username"
    user = db.session.execute(sql, {"username":username}).fetchone()
    if not user or not check_password_hash(user[1], password):
        return False
    session["user_id"] = user[0]
    session["user_name"] = username
    return True

def logout():
    del session["user_id"]
    del session["user_name"]

def register(username, password):
    hash_password = generate_password_hash(password)
    try:
        sql = "INSERT INTO Users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_password})
        db.session.commit()
    except:
        return False
    return True