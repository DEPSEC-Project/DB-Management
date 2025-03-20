"""
Fichier qui initialise l'application Flask
"""
from flask import Flask

from app.config import Config
from app.extensions import db, migrate
from app.models import User


def create_app():
	"""
    Initinitalise l'application flask
    """
	app = Flask(__name__)
	app.config.from_object(Config)
	db.init_app(app)
	migrate.init_app(app, db)
	with app.app_context():
		db.create_all()
	return app
