import webapp2
import AddCommune
from google.appengine.ext import deferred

class UpdateHandler(webapp2.RequestHandler):
    def get(self):
        deferred.defer(AddCommune.AddCommune)
        self.response.out.write('Schema migration successfully initiated.')

app = webapp2.WSGIApplication([('/update_schema', UpdateHandler)])

