from flask import session
from db import db

def get_public_events():
    query = "SELECT event_id, event_name, event_description, place, event_date FROM Events WHERE isprivate=False"
    events = db.session.execute(query).fetchall()
    return events

def get_events_by_user(user_id):
    sql = "SELECT event_id, event_name, event_description, place, event_date FROM Events WHERE creator_id=:user_id"
    events = db.session.execute(sql, {"user_id":user_id}).fetchall()
    return events

def create(event_name, isprivate, event_description, place, event_date, start_time, end_time):
    creator_id = session.get("user_id")
    try:
        sql = """INSERT INTO Events (event_name, creator_id, isprivate, event_description, place, event_date, start_time, end_time) 
        VALUES (:event_name, :creator_id, :isprivate, :event_description, :place, :event_date, :start_time, :end_time)"""
        db.session.execute(sql, {"event_name":event_name, "creator_id":creator_id, "isprivate":isprivate, 
                                "event_description":event_description, "place":place, "event_date":event_date,
                                "start_time":start_time, "end_time":end_time})
        db.session.commit()
    except:
        return False
    return True