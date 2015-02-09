import os
import jinja2
import webapp2
from handlers import BaseHandler
from google.appengine.ext import db
from models import Record

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/admin"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('records.html')

class AdminRecordHandler(BaseHandler.BaseHandler):
  def get(self):

    role = self.session.get('role')
    user_session = self.session.get("user")

    #if role != "admin":
      #self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      #return

    record = Record.Record(one=1, two=2, three=3, nom_de_lorganisation="name")
    #record.put()

    if not self.legacy:
      self.redirect("/#/admin")

    #records = Record.Record.query().order(Record.Record.created_at).fetch(projection=[Record.nom_de_lorganisation])
    records = Record.Record.all()
    #records = q.fetch(limit=50)
    #query_string = "SELECT id, nom_de_lorganisation FROM Record"
    #records = db.GqlQuery(query_string)
    template_values = {
      "message": self.request.get("message"),
      "user_session": user_session,
      "records": records
    }
    self.response.write(LEGACY_TEMPLATE.render(template_values))
