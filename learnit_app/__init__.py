import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from learnit_app.config import Config
from flask_migrate import Migrate

# server setup
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)


# database setup
db = SQLAlchemy(app)
migrate = Migrate(app, db)
