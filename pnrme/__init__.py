from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

toolbar = DebugToolbarExtension(app)
Bootstrap(app)

from . import views