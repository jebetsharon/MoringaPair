from flask import Blueprint, jsonify
from backend.utils.send_email import send_email

test_bp = Blueprint('test', __name__)

@test_bp.route("/send-test-mail", methods=["GET"])
def send_test_mail():
    result = send_email(
        to="recipient@example.com",
        subject="Test Email from MoringaPair App",
        body="This is a test email using SMTP and Flask-Mail."
    )
    return jsonify({"success": result})
