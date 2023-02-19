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

class Card(db.Model):
    __tablename__ = "card_table"
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
    name = db.Column(db.String(50), nullable=False)
    cards = db.relationship("Card")
    subscribers = db.relationship('User', secondary='subscriptions', back_populates='subscribed_to')

    def __str__(self):
        return f'{self.name}'

class User(UserMixin, db.Model):
    __tablename__ = "user_table"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(1024), nullable=False)
    cards_created = db.relationship("Card")

    subscribed_to = db.relationship('Deck', secondary='subscriptions', back_populates='subscribers')
    studied = db.relationship('StudiedCards')

    def __repr__(self):
        return f'<User: {self.username}>'
    
class StudiedCards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user_table.id'))
    card_id = db.Column(db.ForeignKey('card_table.id'))
    date_studied = db.Column(db.Date)
    isCorrect = db.Column(db.Boolean)
    card = db.relationship('Card')

    
subscriptions_table = db.Table('subscriptions',
    db.Column('user_id', db.Integer, db.ForeignKey('user_table.id')),
    db.Column('deck_id', db.Integer, db.ForeignKey('deck_table.id'))
)
