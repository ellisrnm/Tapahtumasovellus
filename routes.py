from flask import redirect, render_template, request, session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from db import db

@app.route("/")
def index():
    query = "SELECT event_id, event_name, event_description, place, event_date FROM Events WHERE isprivate=False"
    public_events = db.session.execute(query).fetchall()
    count = len(public_events)
    user_id = session.get("user_id")
    query = "SELECT event_id, event_name, event_description, place, event_date FROM Events WHERE creator_id=:user_id"
    own_events = db.session.execute(query, {"user_id":user_id}).fetchall()
    return render_template("index.html", count=count, public_events=public_events, own_events=own_events)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        query = "SELECT user_id, password FROM Users WHERE username=:username"
        user = db.session.execute(query, {"username":username}).fetchone()
        if not user or not check_password_hash(user[1], password):
            return render_template("error.html", message="Kirjautuminen epäonnistui")
        else:
            session["user_id"] = user[0]
            session["user_name"] = username
            #token
        return redirect("/")

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["user_name"]
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hash_password = generate_password_hash(password)
        try:
            sql = "INSERT INTO Users (username, password) VALUES (:username, :password)"
            db.session.execute(sql, {"username":username, "password":hash_password})
            db.session.commit()
        except:
            return render_template("error.html", message="Rekisteröinti epäonnistui")
        return redirect("/login")

@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "GET":
        return render_template("new.html")
    if request.method == "POST":
        event_name = request.form["event_name"]
        creator_id = session.get("user_id")
        isprivate = request.form.get("isprivate") or "0"
        event_description = request.form["event_description"]
        place = request.form["place"]
        event_date = request.form["event_date"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        try:
            sql = """INSERT INTO Events (event_name, creator_id, isprivate, event_description, place, event_date, start_time, end_time) 
            VALUES (:event_name, :creator_id, :isprivate, :event_description, :place, :event_date, :start_time, :end_time)"""
            db.session.execute(sql, {"event_name":event_name, "creator_id":creator_id, "isprivate":isprivate, 
                                    "event_description":event_description, "place":place, "event_date":event_date,
                                    "start_time":start_time, "end_time":end_time})
            db.session.commit()
        except:
            return render_template("error.html", message="Tapahtuman luonti epäonnistui")
        return redirect("/")

@app.route("/event/<int:event_id>")
def show_event(event_id):

    has_access = False
    iscreator = False
    sql = """SELECT creator_id FROM Events WHERE event_id=:event_id"""
    creator_id = db.session.execute(sql, {"event_id":event_id}).fetchone()[0]
    if creator_id==session.get("user_id"):
        iscreator = True

    sql = """SELECT event_name, creator_id, isprivate, event_description, place, event_date, start_time, end_time 
             FROM Events WHERE event_id=:event_id"""
    event_info = db.session.execute(sql, {"event_id": event_id}).fetchone()
    event_name = event_info[0]
    creator_id = event_info[1]
    isprivate = event_info[2]
    description = event_info[3]
    place = event_info[4]
    date = event_info[5]
    start_time = event_info[6]
    end_time = event_info[7]
    sql = """SELECT username FROM Users WHERE user_id=:creator_id"""
    creator_name = db.session.execute(sql, {"creator_id": creator_id}).fetchone()[0]
    if iscreator or not isprivate:
            has_access = True
    return render_template("event.html", event_id=event_id, name=event_name, creator_name=creator_name, description=description,
                            place=place, date=date, start_time=start_time, end_time=end_time, iscreator=iscreator, has_access=has_access)

@app.route("/edit/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):

    iscreator = False
    sql = """SELECT creator_id FROM Events WHERE event_id=:event_id"""
    creator_id = db.session.execute(sql, {"event_id":event_id}).fetchone()[0]
    if creator_id!=session.get("user_id"):
        abort(403)
    else:
        iscreator = True

    if request.method == "GET":
        user_id = session.get("user_id")
        sql = """SELECT event_name, creator_id, isprivate, event_description, place, event_date, start_time, end_time 
                FROM Events WHERE event_id=:event_id"""
        event_info = db.session.execute(sql, {"event_id":event_id}).fetchone()
        event_name = event_info[0]
        creator_id = event_info[1]
        isprivate = event_info[2]
        event_description = event_info[3]
        place = event_info[4]
        event_date = event_info[5]
        start_time = event_info[6]
        end_time = event_info[7]

        return render_template("edit.html", event_id=event_id, event_name=event_name, isprivate=isprivate, event_description=event_description,
                                place=place, event_date=event_date, start_time=start_time, end_time=end_time, iscreator=iscreator)
    if request.method == "POST":
        event_name = request.form["event_name"]
        isprivate = request.form.get("isprivate") or "0"
        event_description = request.form["event_description"]
        place = request.form["place"]
        event_date = request.form["event_date"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        try:
            sql = """UPDATE Events SET event_name=:event_name, isprivate=:isprivate, event_description=:event_description, 
            place=:place, event_date=:event_date, start_time=:start_time, end_time=:end_time
            WHERE event_id=:event_id"""
            db.session.execute(sql, {"event_id":event_id, "event_name":event_name, "isprivate":isprivate, 
                                    "event_description":event_description, "place":place, "event_date":event_date,
                                    "start_time":start_time, "end_time":end_time})
            db.session.commit()
        except:
            return render_template("error.html", message="Tapahtuman muokkaus epäonnistui")
        return redirect("/event/"+str(event_id))

@app.route("/delete", methods=["POST"])
def delete_event():
    confirmed = request.form["confirm"]
    event_id = request.form["event_id"]
    if confirmed:
        try:
            sql = """DELETE FROM Events WHERE event_id=:event_id"""
            db.session.execute(sql, {"event_id":event_id})
            db.session.commit()
        except:
            return render_template("error.html", message="Tapahtuman poistaminen epäonnistui")
    return redirect("/")