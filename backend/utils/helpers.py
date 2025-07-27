from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import jsonify
from backend.models import User


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        uid = get_jwt_identity()
        user = User.query.get(uid)
        if not user or user.role != 'admin':
            return jsonify({"msg": "Admins only"}), 403
        return fn(*args, **kwargs)
    return wrapper
