import os
class Config:
	SECRET_KEY = os.getenv('SECRET_KEY', 'password')
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:bonjour@localhost:9001/test_db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'enormemotdepasse')
