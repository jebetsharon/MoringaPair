import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend import create_app
from backend.models import db

TEST_DATABASE_URI = "postgresql://moringa_user:moringa123@localhost:5432/moringa_pair_test_db"

@pytest.fixture
def client():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": TEST_DATABASE_URI,
        "JWT_SECRET_KEY": "test-secret",
    })

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()
