from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, ValidationError
from ..services.quiz_service import save_quiz_result, get_quiz_result

quiz_bp = Blueprint('quiz', __name__)

class QuizSchema(Schema):
    score = fields.Int(required=True)
    strength = fields.Str(required=True)
    weakness = fields.Str(required=True)

@quiz_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_quiz():
    uid = get_jwt_identity()

    try:
        data = QuizSchema().load(request.json)
    except ValidationError as err:
        return jsonify({
            'success': False,
            'message': 'Invalid quiz data',
            'errors': err.messages
        }), 400

    try:
        save_quiz_result(uid, data['score'], data['strength'], data['weakness'])
        return jsonify({
            'success': True,
            'message': 'Quiz submitted successfully'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred while saving the quiz result',
            'error': str(e)
        }), 500

@quiz_bp.route('/my-quiz', methods=['GET'])
@jwt_required()
def get_my_quiz():
    uid = get_jwt_identity()
    quiz = get_quiz_result(uid)

    if not quiz:
        return jsonify({"message": "No quiz result found", "quiz": None, "success": True}), 200

    return jsonify({
        "success": True,
        "quiz": {
            "score": quiz.score,
            "strength": quiz.strength_area,
            "weakness": quiz.weakness_area
        }
    }), 200
