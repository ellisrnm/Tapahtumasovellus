from flask import session
from db import db

def isprivate(event_id):
    try:
        sql = """SELECT isprivate FROM Events WHERE event_id=:event_id"""
        isprivate = db.session.execute(sql, {"event_id": event_id}).fetchone()[0]
    except:
        return False
    return isprivate

def get_public_events():
    query = "SELECT event_id, event_name, event_description, place, event_date FROM Events WHERE isprivate=False"
    events = db.session.execute(query).fetchall()
    return events

def get_events_by_active_user():
    try:
        user_id = session.get("user_id")
        sql = "SELECT event_id, event_name, event_description, place, event_date FROM Events WHERE creator_id=:user_id"
        events = db.session.execute(sql, {"user_id":user_id}).fetchall()
    except:
        return []
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

def delete(event_id, confirmed):
    if not confirmed:
        return False
    try:
        sql = """DELETE FROM Events WHERE event_id=:event_id"""
        db.session.execute(sql, {"event_id":event_id})
        db.session.commit()
    except:
        return False
    return True

def get_event_info(event_id):
    try:
        sql = """SELECT e.event_name, e.creator_id, u.username, e.isprivate, e.event_description, e.place, e.event_date, e.start_time, e.end_time 
                 FROM Events e, Users u WHERE e.event_id=:event_id AND e.creator_id=u.user_id"""
        event_info = db.session.execute(sql, {"event_id": event_id}).fetchone()
    except:
        return []
    return event_info

def update_event_info(event_id, event_name, isprivate, event_description, place, event_date, start_time, end_time):
    try:
        sql = """UPDATE Events SET event_name=:event_name, isprivate=:isprivate, event_description=:event_description, 
        place=:place, event_date=:event_date, start_time=:start_time, end_time=:end_time
        WHERE event_id=:event_id"""
        db.session.execute(sql, {"event_id":event_id, "event_name":event_name, "isprivate":isprivate, 
                                "event_description":event_description, "place":place, "event_date":event_date,
                                "start_time":start_time, "end_time":end_time})
        db.session.commit()
    except:
        return False
    return True

