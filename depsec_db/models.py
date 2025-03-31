# pylint: disable=R0903
"""
Fichier contenant les models de la bbd
"""
from datetime import datetime

from depsec_db.extensions import db


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
    metadata = db.Column(db.JSON, nullable=True)
    results = db.Column(db.JSON, nullable=True)
