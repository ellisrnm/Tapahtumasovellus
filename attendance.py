from flask import session
from db import db

def get_attendance_info(event_id):
    user_id = session.get("user_id")
    try:
        sql = """SELECT attending FROM Attendance WHERE event_id=:event_id AND user_id=:user_id"""
        attending_old = db.session.execute(sql, {"event_id":event_id, "user_id":user_id}).fetchone()[0]
    except:
        return None
    return attending_old

def add_attendance_info(event_id, attending):
    user_id = session.get("user_id")
    attending_old = get_attendance_info(event_id)
    if attending_old in (False, True):
        try:
            sql = """UPDATE Attendance SET attending=:attending WHERE event_id=:event_id AND user_id=:user_id"""
            db.session.execute(sql, {"attending":attending, "event_id":event_id, "user_id":user_id})
            db.session.commit()
        except:
            return False
    else:
        try:
            sql = """INSERT INTO Attendance (event_id, user_id, attending) VALUES (:event_id, :user_id, :attending)"""
            db.session.execute(sql, {"event_id":event_id, "user_id":user_id, "attending":attending})
            db.session.commit()
        except:
            return False
    return True

def get_attendees(event_id):
    try:
        sql = """SELECT a.user_id, u.username FROM Attendance a, Users u 
                 WHERE a.event_id=:event_id AND attending=True AND a.user_id=u.user_id"""
        attendees = db.session.execute(sql, {"event_id":event_id}).fetchall()
    except:
        return []
    return attendees