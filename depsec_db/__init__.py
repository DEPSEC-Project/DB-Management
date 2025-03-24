from flask import Flask

from depsec_db.config import Config
from depsec_db.extensions import db, migrate
from depsec_db.models import User

def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	migrate.init_app(app, db)
	with app.app_context():
		from app.models import User
		db.create_all()

	return app
