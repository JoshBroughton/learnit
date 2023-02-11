import enum
from learnit_app import db
from sqlalchemy.orm import backref
from flask_login import UserMixin

class FormEnum(enum.Enum):
    @classmethod
    def enum_choices(cls):
        choices = []
        for choice in cls:
            choices.append((choice.name, choice.value))
        return choices

class AnswerTypes(FormEnum):
    TRUEFALSE = 'True or False'
    TEXTINPUT = 'Text Input'

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user_table.id"))
    deck_id = db.Column(db.Integer, db.ForeignKey("deck_table.id"), nullable=True)

    prompt = db.Column(db.String(1000), nullable=False)
    answer_type = db.Column(db.Enum(AnswerTypes))
    correct_answer = db.Column(db.String(100), nullable=False)
    explanation = db.Column(db.String(1000), nullable=True)

class Deck(db.Model):
    __tablename__ = "deck_table"
    id = db.Column(db.Integer, primary_key=True)
    cards = db.relationship("Card")

class User(UserMixin, db.Model):
    __tablename__ = "user_table"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(1024), nullable=False)
    cards_created = db.relationship("Card")

    def __repr__(self):
        return f'<User: {self.username}>'