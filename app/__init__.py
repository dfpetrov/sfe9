from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import os
from flask_openid import OpenID

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

from app.models import *


db.create_all()


from app import routes, models


