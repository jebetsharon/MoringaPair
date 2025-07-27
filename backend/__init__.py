from flask import Flask
from .models import db, migrate, jwt
from .routes import register_routes
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    register_routes(app)

    return app
