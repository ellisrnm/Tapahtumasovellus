from flask import redirect, render_template, request, abort
from app import app
import events
import users
import attendance

@app.route("/")
def index():
    public_events, count = events.get_public_events()
    own_events = events.get_events_by_active_user() 
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
        users.check_csrf()
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
        has_access = users.has_access_to_event(event_id)
        iscreator = users.is_event_creator(event_id)
        event_name, _, creator_name, _, description, place, date, start_time, end_time = events.get_event_info(event_id)
        attending = attendance.get_attendance_info(event_id)
        attendees = attendance.get_attendees(event_id)
        has_attendees = 0 if len(attendees)==0 else 1
        return render_template("event.html", event_id=event_id, name=event_name, creator_name=creator_name, description=description,
                                place=place, date=date, start_time=start_time, end_time=end_time, iscreator=iscreator, 
                                attending=attending, has_access=has_access, attendees=attendees, has_attendees=has_attendees)
    if request.method == "POST":
        users.check_csrf()
        attending = request.form["attendance"]
        if not attendance.add_attendance_info(event_id, attending):
            return render_template("error.html", message="Osallistumisen päivittäminen epäonnistui")
        return redirect("/event/"+str(event_id))

@app.route("/edit/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    if not users.is_event_creator(event_id):
        abort(403)
    if request.method == "GET":
        event_name, _, creator_name, isprivate, event_description, place, event_date, start_time, end_time = events.get_event_info(event_id)
        return render_template("edit.html", event_id=event_id, event_name=event_name, isprivate=isprivate, event_description=event_description,
                                place=place, event_date=event_date, start_time=start_time, end_time=end_time)
    if request.method == "POST":
        users.check_csrf()
        event_name = request.form["event_name"]
        isprivate = request.form.get("isprivate") or "0"
        event_description = request.form["event_description"]
        place = request.form["place"]
        event_date = request.form["event_date"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        if not events.update_event_info(event_id, event_name, isprivate, event_description, place, event_date, start_time, end_time):
            return render_template("error.html", message="Tapahtuman muokkaus epäonnistui")
        return redirect("/event/"+str(event_id))

@app.route("/delete", methods=["POST"])
def delete_event():
    users.check_csrf()
    confirmed = request.form["confirm"]
    event_id = request.form["event_id"]
    if not events.delete(event_id, confirmed):
        return render_template("error.html", message="Tapahtuman poistaminen epäonnistui")
    return redirect("/")