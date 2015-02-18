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

    #raise Exception(len(records))
    #if records.count() == 0:
      #Record.Record(nom_de_lorganisation="First org").put()
    if not page:
      page = 0
    else:
      page = int(page)
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
    self.response.write(LEGACY_TEMPLATE.render(template_values))

def humanize_text(string):
    string = string.replace("_", " ")
    string = string.title()
    return string
