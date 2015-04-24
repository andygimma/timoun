from google.appengine.ext import ndb

class SearchRecord(ndb.Model):
  keywords = ndb.StringProperty(required=True)
  department = ndb.StringProperty(required=True)
  service = ndb.StringProperty(required=True)
  age_start = ndb.StringProperty(required=True)
  age_end = ndb.StringProperty(required=True)
  gender = ndb.StringProperty(required=True)
  ip_address = ndb.StringProperty(required=True)
  created_at = ndb.DateTimeProperty(auto_now_add=True, required=True)