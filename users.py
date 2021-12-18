from flask import session, abort, request
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from secrets import token_hex
import events

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

def login(username, password):
    sql = "SELECT user_id, password FROM Users WHERE username=:username"
    user = db.session.execute(sql, {"username":username}).fetchone()
    if not user or not check_password_hash(user[1], password):
        return False
    session["user_id"] = user[0]
    session["user_name"] = username
    session["csrf_token"] = token_hex(16)
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

def is_event_creator(event_id):
    sql = """SELECT creator_id FROM Events WHERE event_id=:event_id"""
    creator_id = db.session.execute(sql, {"event_id":event_id}).fetchone()[0]
    if creator_id==session.get("user_id"):
        return True
    return False

def has_access_to_event(event_id):
    if not events.isprivate(event_id):
        return True
    elif is_event_creator(event_id):
        return True
    return False

def search_users(user):
    sql = "SELECT user_id, username FROM Users WHERE username ILIKE :user"
    result = db.session.execute(sql, {"user":"%"+user+"%"})
    found_users = result.fetchall()
    return found_users