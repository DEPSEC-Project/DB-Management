from flask import Flask
from app.config import Config
from app.extensions import db, migrate

def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	migrate.init_app(app, db)
	with app.app_context():
		from app.models import User
		db.create_all()

	return app
