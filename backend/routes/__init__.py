from flask import Flask
from .auth_routes import auth_bp
from .profile_routes import profile_bp
from .quiz_routes import quiz_bp
from .partner_routes import partner_bp
from .admin_routes import admin_bp
from .pairing_routes import pairing_bp
from .feedback_routes import feedback_bp
from .week_routes import week_bp
from .test_routes import test_bp


def register_routes(app: Flask):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(quiz_bp, url_prefix='/quiz')
    app.register_blueprint(feedback_bp, url_prefix='/feedback')
    app.register_blueprint(partner_bp, url_prefix='/partner')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(pairing_bp, url_prefix='/pairing')
    app.register_blueprint(week_bp, url_prefix='/week')
    app.register_blueprint(test_bp)
