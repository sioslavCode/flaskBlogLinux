from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()  # Ako postoji vratiti ce nesto sto nije NONE

        if user:
            raise ValidationError('Username already exist. Please chosee a differend one!')

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()  # Ako postoji vratiti ce nesto sto nije NONE

        if user:
            raise ValidationError('Email already exist. Please chosee a differend one!')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()  # Ako postoji vratiti ce nesto sto nije NONE
            if user:
                raise ValidationError('Username already exist. Please chosee a differend one!')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()  # Ako postoji vratiti ce nesto sto nije NONE
            if user:
                raise ValidationError('Email already exist. Please chosee a differend one!')


class RequestResetForm(FlaskForm):
    """Forma koju će ispuniti kako bi poslali zahtjev za reset lozinke. Prije toga potrebno provjeriti postoji li email u bazi"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request password reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()  # Ako postoji vratiti ce nesto sto nije NONE

        if user is None:
            raise ValidationError('No account with that email. Register first!')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset password')
