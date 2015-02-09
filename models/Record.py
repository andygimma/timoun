import datetime

from google.appengine.ext import db

class Record(db.Expando):
    record_source = db.StringProperty(required=True, default="CRS IFormBuilder")
