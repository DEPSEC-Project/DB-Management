# pylint: disable=R0903
"""
Gere la configuration de l'application flask (mdp jwt, ect)
"""
import os
from datetime import timedelta

class Config:
	"""
    Template Config
    """
	SECRET_KEY = os.getenv('SECRET_KEY', 'password')
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
									 'postgresql://postgres:bonjour@localhost:9001/test_db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'enormemotdepasse')
	JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
	JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

class DevelopmentConfig(Config):
	"""
    BDD dev
    """
	FLASK_ENV = 'development'
	DEBUG = True
	TWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
	SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL',
									 'postgresql://user:password@db:5432/basededev')

class TestingConfig(Config):
	"""
    BDD test
    """
	FLASK_ENV = 'testing'
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL',
									 'postgresql://user:password@db:5432/basedeprod')

class ProductionConfig(Config):
	"""
    BDD main
    """
	FLASK_ENV = 'production'
	SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DATABASE_URL',
									 'postgresql://user:password@db:5432/basedeprod')

config = { #dictionnaire des confs
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig
}
