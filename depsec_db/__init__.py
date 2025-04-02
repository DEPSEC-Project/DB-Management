"""
Fichier qui initialise l'application Flask
"""
from flask import Flask
from depsec_db.models import * 
from depsec_db.config import Config
from depsec_db.extensions import db, migrate

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
