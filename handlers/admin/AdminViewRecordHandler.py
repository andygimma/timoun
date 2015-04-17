import os
import jinja2
import webapp2
from handlers import BaseHandler
from google.appengine.ext import db
from models import Record
from helpers import QueryHandler

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


    record = QueryHandler.get_organization_by_id(record_id)

    template_values = {
      "message": self.request.get("message"),
      "user_session": user_session,
      "record": record
    }
    language = None
    if "language" in self.request.cookies:
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    language = language.replace('"', '').replace("'", "")
    if language == "fr":

      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_view_records.html')
    else:
      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('view_records.html')
    self.response.write(LEGACY_TEMPLATE.render(template_values))
