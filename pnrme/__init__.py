from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from pymongo import MongoClient

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

toolbar = DebugToolbarExtension(app)
Bootstrap(app)

db = MongoClient(app.config['DB_URL'])[app.config['DB']]

from . import views