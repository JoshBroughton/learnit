from learnit_app import db
from sqlalchemy.orm import backref
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(1024), nullable=False)

    def __repr__(self):
        return f'<User: {self.username}>'