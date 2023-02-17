"""Import packages and modules."""
from datetime import date
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from learnit_app import db
from learnit_app.main.forms import CardForm, DeckForm, TrueFalseForm, TextForm
from learnit_app.models import Card, Deck, AnswerTypes, StudiedCards

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    return render_template('home.html')

@main.route('/create_card', methods=['GET', 'POST'])
@login_required
def create_card():
    form = CardForm()

    if form.validate_on_submit():
        new_card = Card(
            deck_id = form.deck.data.id,
            author_id = current_user.id,
            prompt = form.prompt.data,
            answer_type = form.answer_type.data,
            correct_answer = form.correct_answer.data,
            explanation = form.explanation.data
        )
        db.session.add(new_card)
        db.session.commit()

        flash('New Card Created')
        return redirect(f'/cards/{new_card.id}')
    
    return render_template('create_card.html', form=form)

@main.route('/cards/<card_id>', methods=['GET', 'POST'])
@login_required
def card_detail(card_id):
    card = Card.query.get(card_id)
    form = CardForm(obj=card)

    if form.validate_on_submit():
        new_card = Card(
            deck_id = form.deck.data.id,
            author_id = current_user.id,
            prompt = form.prompt.data,
            answer_type = form.answer_type.data,
            correct_answer = form.correct_answer.data,
            explanation = form.explanation.data
        )
        db.session.add(new_card)
        db.session.commit()

        flash('Card Updated')

    return render_template('card.html', card=card, form=form)

@main.route('/create_deck', methods=['GET', 'POST'])
@login_required
def create_deck():
    form = DeckForm()

    if form.validate_on_submit():
        new_deck = Deck(
            name = form.name.data
        )
        db.session.add(new_deck)
        db.session.commit()

        flash('Deck created')
        return redirect(f'/decks/{new_deck.id}')
    
    return render_template('create_deck.html', form=form)

@main.route('/decks/<deck_id>', methods=['GET', 'POST'])
@login_required
def deck_detail(deck_id):
    deck = Deck.query.get(deck_id)
    cards = deck.cards
    forms = {}
    for card in cards:
        if card.answer_type == AnswerTypes.TRUEFALSE:
            forms[card.id] = TrueFalseForm()
        else:
            forms[card.id] = TextForm()

    for card, form in forms.items():
        if form.validate_on_submit():
            this_card = Card.query.get(card)
            if this_card.correct_answer == form.input.data:
                studied = StudiedCards()
                studied.date_sutdied = date.today()
                studied.card = this_card
                user = current_user
                user.studied.append(studied)
                db.session.add(user)
                db.session.commit()
                print('Correct!')

            else:
                print("Incorrect")
                flash("Incorrect answer, try again!")

    return render_template('deck.html', deck=deck, forms=forms)

