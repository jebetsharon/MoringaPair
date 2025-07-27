from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, ValidationError
from backend.models import Pairing, Week, User, db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from ..utils.helpers import admin_required
import random
from itertools import combinations
import csv
import io
from ..utils.send_email import send_email

pairing_bp = Blueprint('pairing', __name__)

class PairingSchema(Schema):
    student_a_id = fields.Int(required=True)
    student_b_id = fields.Int(allow_none=True)
    week_id = fields.Int(required=True)

@pairing_bp.route('/new-week', methods=['POST'])
@jwt_required()
@admin_required
def create_new_week_pairings():
    data = request.get_json() or {}
    description = data.get('description', 'Auto generated')

    try:
        from backend.services.pairing_service import create_pairings_for_new_week
        week = create_pairings_for_new_week(description=description)
        return jsonify({
            'success': True,
            'message': f'Pairings created for week {week.week_number}',
            'week': {
                'id': week.id,
                'week_number': week.week_number,
                'description': week.description,
            }
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@pairing_bp.route('/', methods=['POST'])
@jwt_required()
@admin_required
def create_pairing():
    try:
        data = PairingSchema().load(request.json)
    except ValidationError as err:
        return jsonify({'success': False, 'errors': err.messages}), 400

    pairing = Pairing(**data)
    db.session.add(pairing)
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Pairing created successfully',
            'data': {
                'student_a_id': pairing.student_a_id,
                'student_b_id': pairing.student_b_id,
                'week_id': pairing.week_id
            }
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Pair already exists or violates constraints'}), 400

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Database error', 'error': str(e)}), 500

@pairing_bp.route('/my-pairing', methods=['GET'])
@jwt_required()
def my_pairing():
    from backend.services.pairing_service import get_current_pairing_for_user

    user_id = get_jwt_identity()
    pairing, week = get_current_pairing_for_user(user_id)

    if not pairing:
        return jsonify({'success': False, 'message': 'No pairing found for current week'}), 404

    paired_student_id = pairing.student_b_id if pairing.student_a_id == user_id else pairing.student_a_id
    paired_student = None
    if paired_student_id:
        paired_student = User.query.get(paired_student_id)

    return jsonify({
        'success': True,
        'week_number': week.week_number,
        'paired_with': {
            'id': paired_student.id,
            'full_name': paired_student.full_name,
            'email': paired_student.email,
        } if paired_student else None
    })

@pairing_bp.route('/latest-week', methods=['GET'])
@jwt_required()
@admin_required
def latest_week_pairings():
    # Optional query params
    week_number = request.args.get('week_number', type=int)
    student_id = request.args.get('student_id', type=int)
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    # Determine which week to query
    if week_number:
        week = Week.query.filter_by(week_number=week_number).first()
        if not week:
            return jsonify({'success': False, 'message': f'Week {week_number} not found'}), 404
    else:
        week = Week.query.order_by(Week.week_number.desc()).first()
        if not week:
            return jsonify({'success': False, 'message': 'No weeks found'}), 404

    query = Pairing.query.filter_by(week_id=week.id)

    if student_id:
        query = query.filter(
            (Pairing.student_a_id == student_id) | (Pairing.student_b_id == student_id)
        )

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    results = []
    for p in paginated.items:
        student_a = User.query.get(p.student_a_id)
        student_b = User.query.get(p.student_b_id) if p.student_b_id else None
        results.append({
            'pairing_id': p.id,
            'student_a': {'id': student_a.id, 'full_name': student_a.full_name, 'email': student_a.email},
            'student_b': {'id': student_b.id, 'full_name': student_b.full_name, 'email': student_b.email} if student_b else None,
            'week_number': week.week_number
        })

    return jsonify({
        'success': True,
        'week': {
            'id': week.id,
            'week_number': week.week_number,
            'description': week.description,
        },
        'pairings': results,
        'pagination': {
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages,
            'total_items': paginated.total,
        }
    })

@pairing_bp.route('/history', methods=['GET'])
@jwt_required()
def pairing_history():
    """
    Endpoint for:
     - Students: view their past pairings (all weeks)
     - Admins: view all pairings with optional filters (week_number, student_id)
    Supports pagination.
    """
    user_id = get_jwt_identity()
    is_admin = False
    from backend.utils.helpers import admin_required

    # Check if user is admin
    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    if user.role == 'admin':
        is_admin = True

    # Query parameters
    week_number = request.args.get('week_number', type=int)
    filter_student_id = request.args.get('student_id', type=int)
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    query = Pairing.query.join(Week, Pairing.week_id == Week.id)

    if is_admin:
        # Admin can filter by week and student
        if week_number:
            week = Week.query.filter_by(week_number=week_number).first()
            if not week:
                return jsonify({'success': False, 'message': f'Week {week_number} not found'}), 404
            query = query.filter(Pairing.week_id == week.id)
        if filter_student_id:
            query = query.filter(
                (Pairing.student_a_id == filter_student_id) | (Pairing.student_b_id == filter_student_id)
            )
    else:
        # Student sees only their pairings
        query = query.filter(
            (Pairing.student_a_id == user_id) | (Pairing.student_b_id == user_id)
        )

    paginated = query.order_by(Week.week_number.desc()).paginate(page=page, per_page=per_page, error_out=False)

    results = []
    for p in paginated.items:
        student_a = User.query.get(p.student_a_id)
        student_b = User.query.get(p.student_b_id) if p.student_b_id else None
        week = Week.query.get(p.week_id)
        results.append({
            'pairing_id': p.id,
            'student_a': {'id': student_a.id, 'full_name': student_a.full_name, 'email': student_a.email},
            'student_b': {'id': student_b.id, 'full_name': student_b.full_name, 'email': student_b.email} if student_b else None,
            'week': {'id': week.id, 'week_number': week.week_number, 'description': week.description}
        })

    return jsonify({
        'success': True,
        'pairings': results,
        'pagination': {
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages,
            'total_items': paginated.total,
        }
    })

@pairing_bp.route('/export/csv', methods=['GET'])
@jwt_required()
@admin_required
def export_pairings_csv():
    week_number = request.args.get('week_number', type=int)

    if week_number:
        week = Week.query.filter_by(week_number=week_number).first()
        if not week:
            return jsonify({'success': False, 'message': f'Week {week_number} not found'}), 404
    else:
        week = Week.query.order_by(Week.week_number.desc()).first()
        if not week:
            return jsonify({'success': False, 'message': 'No weeks found'}), 404

    pairings = Pairing.query.filter_by(week_id=week.id).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Pairing ID', 'Week Number', 'Student A ID', 'Student A Name', 'Student A Email',
                     'Student B ID', 'Student B Name', 'Student B Email'])

    for p in pairings:
        student_a = User.query.get(p.student_a_id)
        student_b = User.query.get(p.student_b_id) if p.student_b_id else None
        writer.writerow([
            p.id,
            week.week_number,
            student_a.id,
            student_a.full_name,
            student_a.email,
            student_b.id if student_b else '',
            student_b.full_name if student_b else '',
            student_b.email if student_b else '',
        ])

    output.seek(0)
    return Response(output, mimetype="text/csv",headers={"Content-Disposition": f"attachment;filename=pairings_week_{week.week_number}.csv"})



@pairing_bp.route('/create', methods=['POST'])
@jwt_required()
@admin_required
def create_pairing_notify():
    data = request.get_json()
    student_email = data.get('student_email')
    pair_info = data.get('pair_info')

    student_subject = "📢 New Weekly Pairing Published!"
    student_message = f"Hi,\n\nYou've been paired this week. Details: {pair_info}\nCheck your dashboard for more."

    send_email(to=student_email, subject=student_subject, body=student_message)

    admin_email = "mentor@moringapair.com"
    admin_subject = "🛎️ New Pairing Created in MoringaPair"
    admin_message = f"A new pairing has been created for:\n\nStudent: {student_email}\nPair Info: {pair_info}\n\nPlease review."

    send_email(to=admin_email, subject=admin_subject, body=admin_message)

    return jsonify({"message": "Pairing created and notifications sent"}), 201
