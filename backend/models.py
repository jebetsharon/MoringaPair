from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(db.Model, TimestampMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="student")

    # Relationships
    profile = db.relationship('Profile', back_populates='user', uselist=False, cascade="all, delete-orphan")
    quiz_result = db.relationship('QuizResult', back_populates='user', uselist=False, cascade="all, delete-orphan")
    pairings_a = db.relationship('Pairing', back_populates='student_a', foreign_keys='Pairing.student_a_id', cascade="all, delete-orphan", passive_deletes=True)
    pairings_b = db.relationship('Pairing', back_populates='student_b', foreign_keys='Pairing.student_b_id', passive_deletes=True)
    feedbacks_sent = db.relationship('Feedback', back_populates='sender', foreign_keys='Feedback.user_id', cascade="all, delete-orphan", passive_deletes=True)
    feedbacks_received = db.relationship('Feedback', back_populates='recipient', foreign_keys='Feedback.recipient_id', cascade="all, delete-orphan", passive_deletes=True)
    preferred_partners = db.relationship('PreferredPartner', back_populates='user', foreign_keys='PreferredPartner.user_id', cascade="all, delete-orphan", passive_deletes=True)
    flagged_partners = db.relationship('FlaggedPartner', back_populates='user', foreign_keys='FlaggedPartner.user_id', cascade="all, delete-orphan", passive_deletes=True)

    @property
    def all_pairings(self):
        return self.pairings_a + self.pairings_b

    # Password hashing helpers
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Profile(db.Model, TimestampMixin):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    preferences = db.Column(db.JSON, default={})
    skills = db.Column(db.JSON, default={})

    user = db.relationship('User', back_populates='profile')

class QuizResult(db.Model, TimestampMixin):
    __tablename__ = 'quiz_results'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    score = db.Column(db.Integer)
    strength_area = db.Column(db.String(100))
    weakness_area = db.Column(db.String(100))

    user = db.relationship('User', back_populates='quiz_result')

class Week(db.Model, TimestampMixin):
    __tablename__ = 'weeks'

    id = db.Column(db.Integer, primary_key=True)
    week_number = db.Column(db.Integer, unique=True, nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    description = db.Column(db.String(255))
    published = db.Column(db.Boolean, default=False)

    pairings = db.relationship('Pairing', back_populates='week', cascade="all, delete-orphan")
    feedbacks = db.relationship('Feedback', back_populates='week', cascade="all, delete-orphan")

class Pairing(db.Model, TimestampMixin):
    __tablename__ = 'pairings'

    id = db.Column(db.Integer, primary_key=True)
    student_a_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    student_b_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    week_id = db.Column(db.Integer, db.ForeignKey('weeks.id', ondelete='CASCADE'), nullable=False)

    student_a = db.relationship('User', back_populates='pairings_a', foreign_keys=[student_a_id])
    student_b = db.relationship('User', back_populates='pairings_b', foreign_keys=[student_b_id])
    week = db.relationship('Week', back_populates='pairings')

    __table_args__ = (
        db.UniqueConstraint('student_a_id', 'student_b_id', 'week_id', name='unique_weekly_pair'),
    )

class Feedback(db.Model, TimestampMixin):
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)  # sender
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)  # receiver
    week_id = db.Column(db.Integer, db.ForeignKey('weeks.id', ondelete='CASCADE'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)
    anonymous = db.Column(db.Boolean, default=False)

    sender = db.relationship('User', back_populates='feedbacks_sent', foreign_keys=[user_id])
    recipient = db.relationship('User', back_populates='feedbacks_received', foreign_keys=[recipient_id])
    week = db.relationship('Week', back_populates='feedbacks')

class PreferredPartner(db.Model, TimestampMixin):
    __tablename__ = 'preferred_partners'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    partner_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    user = db.relationship('User', back_populates='preferred_partners', foreign_keys=[user_id])
    partner = db.relationship('User', foreign_keys=[partner_id])

class FlaggedPartner(db.Model, TimestampMixin):
    __tablename__ = 'flagged_partners'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    partner_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    reason = db.Column(db.String(255))

    user = db.relationship('User', back_populates='flagged_partners', foreign_keys=[user_id])
    partner = db.relationship('User', foreign_keys=[partner_id])
