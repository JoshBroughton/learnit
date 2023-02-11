import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from learnit_app.config import Config

# server setup
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)


# database setup
db = SQLAlchemy(app)
