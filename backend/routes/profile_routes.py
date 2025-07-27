from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import User, QuizResult, Pairing, Profile
from backend import db

profile_bp = Blueprint("profile", __name__)

# GET Profile
@profile_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    # Access the profile model
    profile = Profile.query.filter_by(user_id=user.id).first()

    profile_data = {
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role,
        "preferences": profile.preferences if profile else None,
        "skills": profile.skills if profile else None,
    }

    # Include quiz result if available
    quiz_result = QuizResult.query.filter_by(user_id=user.id).first()
    if quiz_result:
        profile_data["quiz_result"] = {
            "score": quiz_result.score,
            "strength_area": quiz_result.strength_area,
            "weakness_area": quiz_result.weakness_area,
        }
    else:
        profile_data["quiz_result"] = None

    # Include paired partner info if paired
    pairing = Pairing.query.filter(
        (Pairing.student_a_id == user.id) | (Pairing.student_b_id == user.id)
    ).first()

    if pairing:
        partner_id = pairing.student_b_id if pairing.student_a_id == user.id else pairing.student_a_id
        partner = User.query.get(partner_id)
        partner_profile = Profile.query.filter_by(user_id=partner.id).first() if partner else None

        if partner:
            profile_data["paired_partner"] = {
                "id": partner.id,
                "full_name": partner.full_name,
                "email": partner.email,
                "skills": partner_profile.skills if partner_profile else None,
                "preferences": partner_profile.preferences if partner_profile else None,
            }
        else:
            profile_data["paired_partner"] = None
    else:
        profile_data["paired_partner"] = None

    return jsonify({
        "success": True,
        "message": "Profile retrieved successfully",
        "profile": profile_data
    })


# POST /profile: update user preferences/skills
@profile_bp.route("/profile", methods=["POST"])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json()

    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    # Get or create profile
    profile = Profile.query.filter_by(user_id=user.id).first()
    if not profile:
        profile = Profile(user_id=user.id)
        db.session.add(profile)

    # Update profile fields
    profile.preferences = data.get("preferences", profile.preferences)
    profile.skills = data.get("skills", profile.skills)

    try:
        db.session.commit()
        return jsonify({"success": True, "message": "Profile updated successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Error updating profile: {str(e)}"}), 500
