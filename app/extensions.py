from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

"""
Gere les extensions
"""
db = SQLAlchemy()
migrate = Migrate()
