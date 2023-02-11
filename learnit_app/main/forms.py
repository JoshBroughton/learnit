from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from learnit_app.models import AnswerTypes

class CardForm(FlaskForm):
    prompt = TextAreaField('Card Prompt', validators=[DataRequired(), Length(max=1000)])
    answer_type = SelectField('Answer Type', choices=AnswerTypes.enum_choices())
    correct_answer = StringField('Correct Answer', validators=[DataRequired(), Length(max=100)])
    explanation = TextAreaField('Explanation', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Submit')