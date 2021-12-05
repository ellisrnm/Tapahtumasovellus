from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.secret_key = getenv("SECRET_KEY")

dburl = getenv("DATABASE_URL")
if dburl.startswith("postgres://"):
    dburl = dburl.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = dburl
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #to get rid of warning
db = SQLAlchemy(app)

@app.route("/")
def index():
    query = "SELECT event_name FROM Events WHERE isprivate=False"
    public_events = db.session.execute(query).fetchall()
    count = len(public_events)
    user_id = session.get("user_id")
    query = "SELECT event_name FROM Events WHERE creator_id=:user_id"
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