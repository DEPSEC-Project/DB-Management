# pylint: disable=R0903
"""
Modèles SQLAlchemy pour l'application, compatibles avec Flask-SQLAlchemy.
Ces modèles sont conçus pour être utilisés dans une application Flask externe.
"""

import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func

from depsec_db.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime(), server_default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(), onupdate=func.now(), server_default=func.now(), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class TokenBlacklist(db.Model):
    __tablename__ = 'token_blacklist'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), unique=True, nullable=False)  # JWT ID
    created_at = db.Column(db.DateTime(), server_default=func.now(), nullable=False)

    @classmethod
    def is_token_blacklisted(cls, jti, session):
        session = session 
        return session.query(cls).filter_by(jti=jti).first() is not None
      
# User model
class User(db.Model):
	"""
	Model de User
	"""
	__tablename__ = 'users'

	id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
	username = db.Column(db.String(255), nullable=False, unique=True)
	email = db.Column(db.String(255), nullable=False, unique=True)
	password_hash = db.Column(db.String(255), nullable=False)
	full_name = db.Column(db.String(255), nullable=True)
	name = db.Column(db.String(255), nullable=True)

class TrivyReport(db.Model):
    """
	Model du Rapport Trivy
	"""
    __tablename__ = 'trivy_reports'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    schema_version = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    artifact_name = db.Column(db.String, nullable=False)
    artifact_type = db.Column(db.String, nullable=False)
    report_metadata = db.Column(db.JSON, nullable=True)
    results = db.Column(db.JSON, nullable=True)
