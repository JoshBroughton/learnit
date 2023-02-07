from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from learnit_app.config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

from learnit_app.main.routes import main

db = SQLAlchemy(app)

app.register_blueprint(main)

with app.app_context():
    db.create_all()