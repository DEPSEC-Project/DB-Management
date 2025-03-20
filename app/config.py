import os


class Config:
	SECRET_KEY = os.getenv('SECRET_KEY', 'password')
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:bonjour@localhost:9001/test_db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'enormemotdepasse')

class DevelopmentConfig(Config): 
	FLASK_ENV = 'development'
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', 'postgresql://user:password@db:5432/basededev')

class TestingConfig(Config):
	FLASK_ENV = 'testing'
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'postgresql://user:password@db:5432/basedeprod')

class ProductionConfig(Config):
	FLASK_ENV = 'production'
	SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DATABASE_URL', 'postgresql://user:password@db:5432/basedeprod')

config = { #dictionnaire des confs
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig
}