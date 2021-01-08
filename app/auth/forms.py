from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_babel import lazy_gettext as _l
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, DataRequired, Length, Email, EqualTo, ValidationError

from app.auth.models import User


class RegistrationForm(FlaskForm):
    username = StringField(_l('Username *'), validators=[
        InputRequired(_l('Input is required.')),
        DataRequired(_l('Data is required.')),
        Length(min=3, max=20, message=_l('Username must be between 3 and 20 characters long.'))
    ])
    email = EmailField(_l('Email *'), validators=[
        InputRequired(_l('Input is required.')),
        DataRequired(_l('Data is required.')),
        Length(min=6, max=30, message=_l('Email must be between 6 and 30 characters long.')),
        Email(_l('You did not enter valid email!'))
    ])
    password = PasswordField(_l('Password *'), validators=[
        InputRequired(_l('Input is required.')),
        DataRequired(_l('Data is required.')),
        Length(min=3, max=20, message=_l('Username must be between 3 and 20 characters long.')),
        EqualTo('password_confirm', message=_l('Password must match.'))
    ])
    password_confirm = PasswordField(_l('Password *'), validators=[
        InputRequired(_l('Input is required.')),
        DataRequired(_l('Data is required.'))
    ])
    submit = SubmitField(_l('Sign up'))

    @staticmethod
    def validate_username(form, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(_l('User name already exists.'))

    @staticmethod
    def validate_email(form, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(_l('User name already exists.'))


class LoginForm(FlaskForm):
    email = EmailField(_l('Your email *'), validators=[
        InputRequired(_l('Input is required.')),
        DataRequired(_l('Data is required.')),
        Length(min=6, max=30, message=_l('Email must be between 6 and 30 characters long.')),
        Email(_l('You did not enter valid email!'))
    ])
    password = PasswordField(_l('Your password *'), validators=[
        InputRequired(_l('Input is required.')),
        DataRequired(_l('Data is required.')),
        Length(min=3, max=20, message=_l('Username must be between 3 and 20 characters long.'))
    ])
    remember_me = BooleanField(_l('Keep me logged in'))
    submit = SubmitField(_l('Login'))