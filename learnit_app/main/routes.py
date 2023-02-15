"""Import packages and modules."""
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from learnit_app import db
from learnit_app.main.forms import CardForm, DeckForm
from learnit_app.models import Card, Deck

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
    form = DeckForm(obj=deck)

    if form.validate_on_submit():
        new_deck = Deck(
            name = form.name.data
        )
        db.session.add(new_deck)
        db.session.commit()

        flash('Deck updated')

    return render_template('deck.html', deck=deck, form=form)

