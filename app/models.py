#########################################
# project/app/models.py
#########################################
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from app import db
from flask_bcrypt import Bcrypt
import bcrypt

from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for

Base = declarative_base()
metadata = Base.metadata

#db = SQLAlchemy()


class Forecast(Base):
    __tablename__ = 'forecast'
    _id = Column(Integer, primary_key=True)
    date = Column(Date, unique=False, nullable=False)
    city = Column(String(80), unique=False, nullable=False)
    temperature = Column(String(10), unique=False, nullable=False)
    precipitation = Column(Boolean, nullable=True)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class User(db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String, primary_key=True, unique=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    events = db.relationship('Event', backref='author', lazy='dynamic')

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Event(db.Model):
    __tablename__ = 'event'
    _id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.email'))
    start = db.Column(db.DateTime, unique=False, nullable=True)
    end = db.Column(db.DateTime, unique=False, nullable=True)
    title = db.Column(db.String(150), unique=False, nullable=True)
    description = db.Column(db.String(250), unique=False, nullable=True)

    def get_absolute_url(self):
        return url_for('edit_event', _id=self._id)
