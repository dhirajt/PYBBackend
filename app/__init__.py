# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])


bs = Bootstrap(app) #flask-bootstrap
db = SQLAlchemy(app) #flask-sqlalchemy

lm = LoginManager()
lm.setup_app(app)
lm.login_view = 'login'

from app import views, models
