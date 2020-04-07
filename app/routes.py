from datetime import datetime, timedelta
from random import randint
from flask import jsonify, make_response, render_template, request, redirect
from flask_login import login_user, current_user

from app import app, db
from .models import Forecast, User, Event
from .forms import ForecastForm, LoginForm, CreateUserForm, CreateEventForm
from . import login_manager
import flask_bcrypt


CITY = 'Amsterdam'


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.email.data)
        if user:
            if flask_bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect("/")
    return render_template("login2.html", form=form)


@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        user = User(email=email, password=flask_bcrypt.generate_password_hash(password).decode('utf8'))
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect("/")
    return render_template("login.html", form=form)


def get_weather_for_date(day):
    return randint(5, 15)


@app.route('/error')
def home():
    raise
    return None, 200


@app.route('/forecast', methods=['POST', 'GET'])
def forecast():
    forecast_form = ForecastForm()
    if request.method == 'POST':
        if forecast_form.validate_on_submit():
            city = request.form.get('city')
            date = request.form.get('date')
            #date_format = datetime.strptime(date, '%d-%m-%y')
            forecast = Forecast(city=city, date=date, temperature=get_weather_for_date(date))
            db.session.add(forecast)
            db.session.commit()
            return redirect('/')
        error = "Form was not validated"
        return render_template('error.html', form=forecast_form, error=error)

    return render_template('add_forecast.html', form=forecast_form)


@app.route('/forecast/<_id>', methods=['GET', 'PATCH'])
def forecast_for_id(_id):
    if request.method == 'PATCH':
        temperature = request.args.get('temperature')

        forecast = Forecast.query.get_or_404(_id)
        forecast.temperature = temperature
        db.session.commit()

        return jsonify({'id': forecast._id}), 203
    elif request.method == 'GET':
        forecast = Forecast.query.get_or_404(_id)
        return jsonify(
            {'id': forecast._id, 'city': forecast.city, 'temperature': forecast.temperature, 'date': forecast.date})


@app.route('/delete_forecast/<_id>', methods=['DELETE'])
def delete_forecast(_id):
    forecast = Forecast.query.get_or_404(_id)
    db.session.delete(forecast)
    db.commit()
    return jsonify({'result': True})


@app.route('/')
@app.route('/hello')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events, current_user=current_user)


@app.route("/create_event", methods=["GET", "POST"])
def create_event():
    form = CreateEventForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            start = request.form.get('start')
            end = request.form.get('end')
            title = request.form.get('title')
            description = request.form.get('description')
            event = Event(user_id=current_user.email, start=start, end=end, title=title, description=description)
            db.session.add(event)
            db.session.commit()
            return redirect("/")
        else:
            error = "Form was not validated"
            return render_template('error.html', form=form, error=form.errors)

    return render_template("event.html", form=form)


@app.route('/edit_event/<_id>', methods=['GET', 'POST'])
def edit_event(_id):
    event = Event.query.get_or_404(_id)
    form = CreateEventForm(author=event.author, start=event.start, end=event.end, title=event.title, description=event.description)
    if request.method == 'POST':
        event.start = request.form.get('start')
        event.end = request.form.get('end')
        event.title = request.form.get('title')
        event.description = request.form.get('description')
        db.session.commit()
        return redirect("/")
    elif request.method == 'GET':
        if current_user.email == event.user_id:
            return render_template("event2.html", form=form, event_id=_id, event=event)
        else:
            return "Это не твое событие. Редактировать нельзя"


@app.route('/time')
def current_time():
    return make_response(jsonify(time=datetime.now()), 201)


class Week:
    def __init__(self, start):
        self.start = start.strftime('%d-%m-%y')
        self.end = (start + timedelta(days=7)).strftime('%d-%m-%y')


@app.route('/')
@app.route('/week')
def weather_week():
    week = Week(datetime.today())
    return render_template('week_overview.html', week=week, city=CITY)
