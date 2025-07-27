from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta
from backend.models import User, Pairing, Week, QuizResult, db


def register_user(full_name, email, password, role="student"):
    """
    Registers a new user if the email is not taken.
    Returns (User, None) if successful, else (None, error message).
    """
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return None, "Email already exists"

    hashed_password = generate_password_hash(password)

    user = User(
        full_name=full_name,
        email=email,
        password_hash=hashed_password,
        role=role
    )

    try:
        db.session.add(user)
        db.session.commit()
        return user, None
    except Exception as e:
        db.session.rollback()
        return None, f"Database error: {str(e)}"


def login_user(email, password):
    """
    Authenticates user credentials and generates a JWT token.
    Returns (token data, None) if successful, else (None, error message).
    """
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return None, "Invalid credentials"

    # Token expires in 24 hours
    token = create_access_token(identity=user.id, expires_delta=timedelta(hours=24))

    return {
        "access_token": token,
        "user_id": user.id,
        "full_name": user.full_name,
        "role": user.role
    }, None
