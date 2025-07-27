from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, ValidationError
from backend.models import Feedback, db

feedback_bp = Blueprint('feedback', __name__)


class FeedbackSchema(Schema):
    recipient_id = fields.Int(required=True)
    message = fields.Str(required=True)
    rating = fields.Int(required=True)
    week_id = fields.Int(required=True)
    anonymous = fields.Bool(required=True)

@feedback_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_feedback():
    uid = get_jwt_identity()
    try:
        data = FeedbackSchema().load(request.json)
    except ValidationError as err:
        return jsonify({'success': False, 'errors': err.messages}), 400

    fb = Feedback(user_id=uid, **data)
    db.session.add(fb)
    db.session.commit()
    return jsonify({'message': 'Feedback submitted'}), 201

@feedback_bp.route('/week/<int:week_id>', methods=['GET'])
@jwt_required()
def view_week_feedback(week_id):
    fbs = Feedback.query.filter_by(week_id=week_id).all()
    return jsonify({
        "success": True,
        "message": f"Feedback for week {week_id} retrieved successfully",
        "feedback": [
            {
                'sender_id': f.user_id,
                'recipient_id': f.recipient_id,
                'message': f.message,
                'rating': f.rating,
                'anonymous': f.anonymous
            } for f in fbs
        ]
    }), 200


