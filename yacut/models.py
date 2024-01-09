from datetime import datetime

from . import db
from .constants import MAX_MODEL_ORIGINAL_LENGTH, MAX_MODEL_SORT_LENGTH


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_MODEL_ORIGINAL_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_MODEL_SORT_LENGTH), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
