import os
import jinja2
import webapp2
from handlers import BaseHandler
from google.appengine.ext import db
from models import Record
import MySQLdb
from helpers import QueryHandler

_INSTANCE_NAME = 'timoun-production:surveydata'

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/admin"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('records.html')

class AdminRecordHandler(BaseHandler.BaseHandler):
  def get(self):


    role = self.session.get('role')
    user_session = self.session.get("user")
    page = self.request.get("page")

    if role != "admin":
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return

    if not self.legacy:
      self.redirect("/#/admin")

    query = Record.Record.query()
    records = None
    if page:
      offset = int(page) * 100
      records = query.fetch(100, offset = offset)
    else:
      records = query.fetch(100)

    if not page:
      page = 0
    else:
      page = int(page)

    records = QueryHandler.execute_query('SELECT 1_nom, id FROM organization LIMIT 100')

    #raise Exception(len(guestlist))
    next_page = page + 1
    last_page = page - 1
    template_values = {
      "message": self.request.get("message"),
      "user_session": user_session,
      "records": records,
      "records_length": len(records),
      "next_page": next_page,
      "last_page": last_page
    }

    language = None
    if "language" in self.request.cookies:
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    language = language.replace('"', '').replace("'", "")
    if language == "fr":

      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_records.html')
    else:
      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('records.html')
    self.response.write(LEGACY_TEMPLATE.render(template_values))

def humanize_text(string):
    string = string.replace("_", " ")
    string = string.title()
    return string
