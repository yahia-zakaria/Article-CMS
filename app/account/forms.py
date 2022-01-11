from flask_wtf import FlaskForm
from wtforms import  BooleanField, StringField, PasswordField
from wtforms.fields.simple import SubmitField
from wtforms.validators import Required, Email, EqualTo, Length


class RegistrationForm(FlaskForm):
    email = StringField('Email Address', [Email(), Required()])
    password = PasswordField('Password', [Required(),
    EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Repeat Password', [Required()])
    submit = SubmitField("Register")



class LoginForm(FlaskForm):
    username = StringField('Username', [Required(), Email()])
    password = PasswordField('Password', [Required()])
    submit = SubmitField("Login")
