from flask import redirect, render_template, request, session, abort
from app import app
from db import db
import events
import users

@app.route("/")
def index():
    public_events = events.get_public_events()
    count = len(public_events)
    user_id = session.get("user_id")
    own_events = events.get_events_by_user(user_id)
    return render_template("index.html", count=count, public_events=public_events, own_events=own_events)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.login(username, password):
            return render_template("error.html", message="Kirjautuminen epäonnistui")
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.register(username, password):
            return render_template("error.html", message="Rekisteröinti epäonnistui")
        return redirect("/login")

@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "GET":
        return render_template("new.html")
    if request.method == "POST":
        event_name = request.form["event_name"]
        isprivate = request.form.get("isprivate") or "0"
        event_description = request.form["event_description"]
        place = request.form["place"]
        event_date = request.form["event_date"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        if not events.create(event_name, isprivate, event_description, place, event_date, start_time, end_time):
            return render_template("error.html", message="Tapahtuman luonti epäonnistui")
        return redirect("/")

@app.route("/event/<int:event_id>", methods=["GET", "POST"])
def show_event(event_id):
    if request.method == "GET":
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
        attending = events.get_attendance_info(event_id)
        return render_template("event.html", event_id=event_id, name=event_name, creator_name=creator_name, description=description,
                                place=place, date=date, start_time=start_time, end_time=end_time, iscreator=iscreator, 
                                attending=attending, has_access=has_access)
    if request.method == "POST":
        attending = request.form["attendance"]
        if not events.add_attendance_info(event_id, attending):
            return render_template("error.html", message="Osallistumisen päivittäminen epäonnistui")
        return redirect("/event/"+str(event_id))

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