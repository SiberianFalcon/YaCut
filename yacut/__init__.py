from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from settings import Config

app = Flask(__name__, template_folder='../html', static_folder='../html/css')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from . import views, models, forms


# from yacut.__init__ import db