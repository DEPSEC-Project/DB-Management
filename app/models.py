# pylint: disable=R0903
from datetime import datetime

from .extensions import db


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
