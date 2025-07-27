from backend.models  import Week,db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta
import random
from itertools import combinations

def create_week(number, start_date, end_date, description, published=False):
    """
    Creates and saves a new Week.
    Returns the created Week object.
    Raises Exception on DB failure.
    """
    week = Week(week_number=number, start_date=start_date, end_date=end_date, description=description, published=published)
    try:
        db.session.add(week)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Failed to create week: {str(e)}")

    return week

def list_weeks():
    """
    Returns a list of all weeks ordered descending by week_number.
    """
    return Week.query.order_by(Week.week_number.desc()).all()