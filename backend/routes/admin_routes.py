from flask import Blueprint, request, jsonify, Response
from backend.models import User
from backend import db
from flask_jwt_extended import jwt_required
from ..utils.helpers import admin_required
from ..utils.pagination import paginate
import logging
import csv
import io

admin_bp = Blueprint('admin', __name__)
logger = logging.getLogger(__name__)


@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def list_users():
    try:
        try:
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 5))
            if page < 1 or limit < 1:
                raise ValueError
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid pagination parameters'}), 400

        role_filter = request.args.get('role')
        search = request.args.get('search')

        query = User.query

        if role_filter:
            query = query.filter_by(role=role_filter)

        if search:
            like_pattern = f"%{search}%"
            query = query.filter(
                (User.full_name.ilike(like_pattern)) | (User.email.ilike(like_pattern))
            )

        result = paginate(query, page, limit)

        result['items'] = [
            {
                'id': user.id,
                'full_name': user.full_name,
                'email': user.email,
                'role': user.role
            } for user in result['items']
        ]

        return jsonify({
            'success': True,
            'message': 'Users retrieved successfully',
            'data': result
        }), 200

    except Exception as e:
        logger.error(f"Error listing users: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while fetching users',
            'error': str(e)
        }), 500


@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404

        user_data = {
            'id': user.id,
            'full_name': user.full_name,
            'email': user.email,
            'role': user.role
        }
        return jsonify({'success': True, 'user': user_data}), 200

    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {str(e)}")
        return jsonify({'success': False, 'message': 'Error fetching user', 'error': str(e)}), 500


@admin_bp.route('/users/export/csv', methods=['GET'])
@jwt_required()
@admin_required
def export_users_csv():
    try:
        users = User.query.all()

        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(['ID', 'Full Name', 'Email', 'Role'])

        for user in users:
            writer.writerow([user.id, user.full_name, user.email, user.role])

        output.seek(0)

        return Response(
            output,
            mimetype='text/csv',
            headers={
                "Content-Disposition": "attachment;filename=users.csv"
            }
        )
    except Exception as e:
        logger.error(f"Error exporting users CSV: {str(e)}")
        return jsonify({'success': False, 'message': 'Error exporting CSV', 'error': str(e)}), 500


@admin_bp.route('/users', methods=['POST'])
@jwt_required()
@admin_required
def create_user():
    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    password_hash = data.get('password_hash')
    role = data.get('role', 'student')

    if not full_name or not email or not password_hash:
        return jsonify({'success': False, 'message': 'Missing required fields: full_name, email, password_hash'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'message': 'Email already in use'}), 400

    try:
        new_user = User(
            full_name=full_name,
            email=email,
            password_hash=password_hash,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'success': True, 'message': 'User created successfully', 'user_id': new_user.id}), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating user: {str(e)}")
        return jsonify({'success': False, 'message': 'Error creating user', 'error': str(e)}), 500


@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    password_hash = data.get('password_hash')
    role = data.get('role')

    if email and email != user.email:
        if User.query.filter(User.email == email, User.id != user_id).first():
            return jsonify({'success': False, 'message': 'Email already in use'}), 400

    try:
        if full_name:
            user.full_name = full_name
        if email:
            user.email = email
        if password_hash:
            user.password_hash = password_hash
        if role:
            user.role = role

        db.session.commit()
        return jsonify({'success': True, 'message': 'User updated successfully'})

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating user {user_id}: {str(e)}")
        return jsonify({'success': False, 'message': 'Error updating user', 'error': str(e)}), 500


@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True, 'message': 'User deleted successfully'})

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting user {user_id}: {str(e)}")
        return jsonify({'success': False, 'message': 'Error deleting user', 'error': str(e)}), 500
