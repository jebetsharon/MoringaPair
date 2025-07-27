from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from marshmallow import Schema, fields, ValidationError, validate
from ..services.auth_service import register_user, login_user
from ..utils.send_email import send_email

auth_bp = Blueprint('auth', __name__)

class RegisterSchema(Schema):
    full_name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    role = fields.Str(load_default='student', validate=validate.OneOf(['student', 'admin']))

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = RegisterSchema().load(request.json)
    except ValidationError as err:
        return jsonify({"success": False, "errors": err.messages}), 400

    user, error = register_user(**data)
    if error:
        return jsonify({"success": False, "message": error}), 400

    # Send welcome email after successful registration
    subject = "Welcome to MoringaPair!"
    message = f"Hello {user.full_name},\n\nWelcome to MoringaPair. You're now registered."
    send_email(to=user.email, subject=subject, body=message)

    return jsonify({"success": True, "user_id": user.id, "message": "User registered successfully"}), 201



@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = LoginSchema().load(request.json)
    except ValidationError as err:
        return jsonify({"success": False, "errors": err.messages}), 400

    token_data, error = login_user(data['email'], data['password'])
    if error:
        return jsonify({"success": False, "message": error}), 401

    return jsonify({"success": True, "data": token_data}), 200

