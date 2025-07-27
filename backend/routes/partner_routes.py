from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, ValidationError
from backend.models import PreferredPartner, FlaggedPartner, User, db
from sqlalchemy.exc import SQLAlchemyError
from ..utils.helpers import admin_required  

partner_bp = Blueprint('partners', __name__)


class PreferredPartnerSchema(Schema):
    partner_id = fields.Int(required=True)

class FlaggedPartnerSchema(Schema):
    partner_id = fields.Int(required=True)
    reason = fields.Str(required=True, validate=lambda r: len(r.strip()) > 0)


def get_user_info(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"id": user_id, "full_name": "Unknown", "email": "N/A"}
    return {"id": user.id, "full_name": user.full_name, "email": user.email}




@partner_bp.route('/preferred', methods=['POST'])
@jwt_required()
def add_preferred():
    uid = get_jwt_identity()
    try:
        data = PreferredPartnerSchema().load(request.json)
    except ValidationError as err:
        return jsonify({'success': False, 'errors': err.messages}), 400

    if data['partner_id'] == uid:
        return jsonify({'success': False, 'message': 'You cannot prefer yourself.'}), 400

    if PreferredPartner.query.filter_by(user_id=uid, partner_id=data['partner_id']).first():
        return jsonify({'success': False, 'message': 'Already preferred.'}), 400

    try:
        pp = PreferredPartner(user_id=uid, partner_id=data['partner_id'])
        db.session.add(pp)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Preferred partner added.'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Database error.', 'error': str(e)}), 500


@partner_bp.route('/flagged', methods=['POST'])
@jwt_required()
def add_flagged():
    uid = get_jwt_identity()
    try:
        data = FlaggedPartnerSchema().load(request.json)
    except ValidationError as err:
        return jsonify({'success': False, 'errors': err.messages}), 400

    if data['partner_id'] == uid:
        return jsonify({'success': False, 'message': 'You cannot flag yourself.'}), 400

    if FlaggedPartner.query.filter_by(user_id=uid, partner_id=data['partner_id']).first():
        return jsonify({'success': False, 'message': 'Already flagged.'}), 400

    try:
        fp = FlaggedPartner(user_id=uid, partner_id=data['partner_id'], reason=data['reason'].strip())
        db.session.add(fp)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Flagged partner added.'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Database error.', 'error': str(e)}), 500


@partner_bp.route('/preferred', methods=['GET'])
@jwt_required()
def list_preferred():
    uid = get_jwt_identity()
    preferred = PreferredPartner.query.filter_by(user_id=uid).all()
    result = [get_user_info(p.partner_id) for p in preferred]

    return jsonify({'success': True, 'preferred_partners': result}), 200


@partner_bp.route('/flagged', methods=['GET'])
@jwt_required()
def list_flagged():
    uid = get_jwt_identity()
    flagged = FlaggedPartner.query.filter_by(user_id=uid).all()
    result = []
    for f in flagged:
        info = get_user_info(f.partner_id)
        info["reason"] = f.reason
        result.append(info)

    return jsonify({'success': True, 'flagged_partners': result}), 200




@partner_bp.route('/admin/flagged', methods=['GET'])
@jwt_required()
@admin_required
def admin_view_all_flags():
    flagged = FlaggedPartner.query.all()
    result = []
    for f in flagged:
        user_info = get_user_info(f.user_id)
        partner_info = get_user_info(f.partner_id)
        result.append({
            "user": user_info,
            "partner": partner_info,
            "reason": f.reason
        })

    return jsonify({'success': True, 'flagged_records': result}), 200
