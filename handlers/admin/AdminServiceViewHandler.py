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

LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_view_service.html')

class AdminServiceViewHandler(BaseHandler.BaseHandler):
  def get(self, record_id):

    role = self.session.get('role')  
    user_session = self.session.get("user")

    if role != "admin" and role != "staff":
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return

    sql_statement = """
      SELECT * FROM service WHERE id='{0}' LIMIT 1
    """.format(record_id)

    service = QueryHandler.execute_query(sql_statement)

    program_name = QueryHandler.execute_query("SELECT name_french FROM program WHERE id={0}".format(service[0][11]))
    
    template_values = {
      "message": self.request.get("message"),
      "user_session": user_session,
      "service": service[0],
      "program": program_name[0][0],
      "role": role
    }
    language = None
    if "language" in self.request.cookies:
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    language = language.replace('"', '').replace("'", "")
    if language == "fr":

      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_view_service.html')
    else:
      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('view_service.html')
    self.response.write(LEGACY_TEMPLATE.render(template_values))

