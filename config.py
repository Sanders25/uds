import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:9384@localhost:5432/flask_uds_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False