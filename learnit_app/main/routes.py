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
    decks = Deck.query.all()
    return render_template('home.html', decks=decks)

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
    user = current_user

    for card in cards:
        if card.answer_type == AnswerTypes.TRUEFALSE:
            forms[f'{card.id}'] = TrueFalseForm(prefix=f'{card.id}')
        else:
            forms[f'{card.id}'] = TextForm(prefix=f'{card.id}')

    for card, form in forms.items():
        if form.validate_on_submit() and form.submit.data:
            print(form.input.data)
            print(card)
            this_card = Card.query.get(int(card))
            print(this_card.correct_answer)
            if this_card.correct_answer == form.input.data:
                studied = StudiedCards(
                    card_id = this_card.id,
                    user_id = user.id,
                    date_studied = date.today(),
                    card = this_card
                )
                user.studied.append(studied)
                db.session.add(user)
                db.session.commit()
                print('Correct!')
            else:
                print("Incorrect")
                flash("Incorrect answer, try again!")
    
    studied_cards = [card.card_id for card in user.studied]
    print(studied_cards)
    return render_template('deck.html', deck=deck, forms=forms, studied_cards=studied_cards)

@main.route('/decks/<deck_id>/cards', methods=['GET', 'POST'])
@login_required
def deck_list_all_cards(deck_id):
    deck = Deck.query.get(deck_id)
    cards = deck.cards
    return render_template('deck_all_cards.html', cards=cards)

@main.route('/decks/<deck_id>/reset', methods=['POST'])
@login_required
def reset_deck(deck_id):
    deck = Deck.query.get(deck_id)
    user = current_user
    studied_cards = [card.card_id for card in user.studied]
    for card in deck.cards:
        if card.id in studied_cards:
            StudiedCards.query.filter_by(card_id=card.id).delete()
            db.session.commit()
            
    return redirect(url_for('main.homepage'))