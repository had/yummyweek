from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from app.users.models import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    nickname = StringField("Nickname", validators=[
        DataRequired(), Length(1, 64),
        Regexp("^[A-Za-z][A-Za-z0-9_.]*$",
               message="Please use only letters, numbers, dots or underscores")])
    password = PasswordField("Password",
                             validators=[DataRequired(), EqualTo("password2", message="Passwords are different")])
    password2 = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered")

    def validate_nickname(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Nickname already in use")
