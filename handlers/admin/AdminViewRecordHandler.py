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

LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('view_records.html')

class AdminViewRecordHandler(BaseHandler.BaseHandler):
  def get(self, record_id):

    role = self.session.get('role')
    user_session = self.session.get("user")

    #if role != "admin":
      #self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      #return

    if not self.legacy:
      self.redirect("/#/admin")

    record = Record.Record.get_by_id(int(record_id))

    template_values = {
      "message": self.request.get("message"),
      "user_session": user_session,
      "record": record
    }
    self.response.write(LEGACY_TEMPLATE.render(template_values))