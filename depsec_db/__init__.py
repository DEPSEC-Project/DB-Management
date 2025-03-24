from flask import Flask
<<<<<<< Updated upstream:app/__init__.py
from app.config import Config
from app.extensions import db, migrate
=======

from depsec_db.config import Config
from depsec_db.extensions import db, migrate
from depsec_db.models import User

>>>>>>> Stashed changes:depsec_db/__init__.py

def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	migrate.init_app(app, db)
	with app.app_context():
		from app.models import User
		db.create_all()

	return app
