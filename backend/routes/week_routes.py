from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, ValidationError
from backend.models import User, Week, db
from sqlalchemy.exc import SQLAlchemyError

week_bp = Blueprint('week', __name__)


class WeekSchema(Schema):
    week_number = fields.Int(required=True)
    start_date = fields.Str(required=True)
    end_date = fields.Str(required=True)
    description = fields.Str(required=True)
    published = fields.Bool(missing=False)


@week_bp.route('/weeks', methods=['GET'])
def get_weeks():
    try:
        weeks = Week.query.all()
        schema = WeekSchema(many=True)  
        weeks_data = schema.dump(weeks)
        
        return jsonify({
            'success': True,
            'message': 'Weeks retrieved successfully',
            'data': weeks_data
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error retrieving weeks',
            'error': str(e)
        }), 500



@week_bp.route('/weeks', methods=['POST'])
@jwt_required()
def create_week():
    uid = get_jwt_identity()
    user = User.query.get(uid)

    if not user or user.role != 'admin':
        return jsonify({
            'success': False,
            'message': 'Unauthorized. Admin access required.'
        }), 403

    try:
        data = WeekSchema().load(request.json)
    except ValidationError as err:
        return jsonify({
            'success': False,
            'message': 'Invalid input data',
            'errors': err.messages
        }), 400

    try:
        week = Week(**data)
        db.session.add(week)
        db.session.commit()

        schema = WeekSchema()
        week_data = schema.dump(week)

        return jsonify({
            'success': True,
            'message': 'Week created successfully',
            'data': week_data
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Database error',
            'error': str(e)
        }), 500

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Unexpected server error',
            'error': str(e)
        }), 500
