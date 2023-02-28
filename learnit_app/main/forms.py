from flask_wtf import FlaskForm
from learnit_app import db
from wtforms import TextAreaField, SelectField, StringField, SubmitField, RadioField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, ValidationError
from learnit_app.models import AnswerTypes, Deck

def deck_factory():
    return Deck.query.all()

class CardForm(FlaskForm):
    deck = QuerySelectField('Deck', query_factory=deck_factory, validators=[DataRequired()])
    prompt = TextAreaField('Card Prompt', validators=[DataRequired(), Length(max=1000)])
    answer_type = SelectField('Answer Type', choices=AnswerTypes.enum_choices())
    correct_answer = RadioField('Correct Answer', validators=[DataRequired()], choices=["True", "False"])
    explanation = TextAreaField('Explanation', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')
    

class DeckForm(FlaskForm):
    name = StringField('Deck Name', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Submit')

    def validate_name(form, field):
        result = Deck.query.filter_by(name=field.data).one_or_none()
        if result is not None:
            raise ValidationError('A deck with this name already exists')


class TrueFalseForm(FlaskForm):
    input = RadioField('True or False', choices=['True', 'False'], validators=[DataRequired('')])
    submit = SubmitField('Submit')


class TextForm(FlaskForm):
    input = StringField('Enter the correct answer:', validators=[DataRequired(''), Length(max=100)])
    submit = SubmitField('Submit')

class DeleteDeck(FlaskForm):
    delete = SubmitField('Delete')