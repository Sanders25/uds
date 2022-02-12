import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #SQLALCHEMY_DATABASE_URI = "postgresql://postgres:9384@localhost:5432/flask_uds_db"
    SQLALCHEMY_DATABASE_URI = "postgresql://svchpqbctkxhbe:7423eabbb095005ebe7a1e5d3228b0ee32a49a87f9348ff5ec4b1cb53b11ee61@ec2-54-220-166-184.eu-west-1.compute.amazonaws.com:5432/d1u52q7ae5p3hd"
    SQLALCHEMY_TRACK_MODIFICATIONS = False