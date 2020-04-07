from os import environ
import os


class Config:
    url = 'postgresql://{}:{}@{}:{}/{}'

    #SQLALCHEMY_DATABASE_URI = url.format('postgres', '1', 'localhost', '5432', 'weather_forecast_dev')
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SECRET_KEY = environ.get('SECRET_KEY')
    SECRET_KEY = 'this - really - needs - to - be - changed'
