import os
import unittest
import app

from learnit_app import app, db
from learnit_app.extensions import bcrypt
from learnit_app.models import Deck, Card, User, AnswerTypes

def create_user():
    password_hash = bcrypt.generate_password_hash('#Password1').decode('utf-8')
    user = User(username='tester', password=password_hash)

    db.session.add(user)
    db.session.commit()

def login_user(app):
    post_data = {
        'username': 'tester',
        'password': '#Password1'
    }

    app.post('/login', data=post_data, follow_redirects=True)

def create_deck():
    deck = Deck(name = 'deck')

    db.session.add(deck)
    db.session.commit()

def create_card():
    create_user()
    create_deck()
    card = Card(
        deck_id = 1,
        author_id = 1,
        prompt = 'prompt',
        answer_type = AnswerTypes.TRUEFALSE,
        correct_answer = 'True',
        explanation = 'explanation'
    )

    db.session.add(card)
    db.session.commit()


class RouteTests(unittest.TestCase):
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_card(self):
        create_user()
        login_user(self.app)

        response = self.app.get('/create_card', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_card_details(self):
        create_card()
        login_user(self.app)

        response = self.app.get('/cards/1')
        self.assertEqual(response.status_code, 200)

    def test_create_deck(self):
        create_user()
        login_user(self.app)

        response = self.app.get('/create_deck')
        self.assertEqual(response.status_code, 200)

    def test_deck_details(self):
        create_card()
        login_user(self.app)

        response = self.app.get('/decks/1')
        self.assertEqual(response.status_code, 200)
        
    def test_deck_card_index(self):
        create_card()
        login_user(self.app)

        response = self.app.get('/decks/1/cards')
        self.assertEqual(response.status_code, 200)

    def test_deck_reset(self):
        create_card()
        login_user(self.app)

        response = self.app.post('/decks/1/reset', follow_redirects=True)
        self.assertEqual(response.status_code, 200)




