from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from learnit_app.models import User
from learnit_app.extensions import bcrypt
import re

def password_creation_checker(form, field):
    if re.search("^([a-zA-Z0-9]*|[^A-Z]*|[^a-z]*|[^0-9]*)$", field.data):
            raise ValidationError('Password must contain at least one each of uppercase letter, lowercase letter, number, and symbol')
# TODO: Personalize these a bit more
class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=100), password_creation_checker])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).one_or_none()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

        
class LoginForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No user with that username. Please try again.')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again.')