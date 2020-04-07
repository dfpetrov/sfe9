from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField, DateTimeField
from wtforms import StringField
from wtforms.validators import DataRequired
from datetime import date


class ForecastForm(FlaskForm):
    city = StringField('city')
    date = DateField('date', validators=[DataRequired()])
    temperature = StringField('temperature')


class LoginForm(FlaskForm):
    email = StringField("Email")
    password = StringField("Password")


class CreateUserForm(FlaskForm):
    email = StringField("Email")
    password = StringField("Password")


class CreateEventForm(FlaskForm):
    author = StringField('Email')
    start = DateTimeField("Start", default=date.today(), format='%Y-%m-%d %H:%M:%S', validators=[DataRequired(message="Не правильный формат поля start")],)
    end = DateTimeField("End", default=date.today(), format='%Y-%m-%d %H:%M:%S', validators=[DataRequired(message="Не правильный формат поля end")],)
    title = StringField('title')
    description = StringField('description')
