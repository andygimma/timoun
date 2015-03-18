from google.appengine.ext import ndb

class Commune(ndb.Model):
  name = ndb.StringProperty(required=True)
