import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from learnit_app.config import Config
from learnit_app.models import User

# server setup
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

# database setup
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

# Authentication setup
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

bcrypt = Bcrypt(app)