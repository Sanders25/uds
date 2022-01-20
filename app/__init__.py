import imp
from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_admin import Admin

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
loginManager = LoginManager(app)
loginManager.login_view = 'login'
adminManager = Admin(app, url='/db_admin_main', name='db_admin')


from app import routes, models, errors

