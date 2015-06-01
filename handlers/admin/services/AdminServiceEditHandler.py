import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import Service
from helpers import QueryHandler, ServiceHelper

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../../templates/admin"),
         os.path.join(os.path.dirname(__file__),"../../../templates/layouts")]))

TEMPLATE = JINJA_ENVIRONMENT.get_template('edit_service.html')

class AdminServiceEditHandler(BaseHandler.BaseHandler):
  def get(self, service_id):
    role = self.session.get('role')
    user_session = self.session.get("user")

    if role != "admin" and role != "staff":
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return

    if not self.legacy:
      self.redirect("/#/services/{0}/edit".format(service_key))

    sql_statement = "SELECT * FROM service WHERE id={0}".format(service_id)

    service = QueryHandler.execute_query(sql_statement)
    if len(service) == 0:
      self.redirect("/admin?message=That service does not exist")
      return
    # raise Exception(service)
    

    template_values = {
      "role": self.session.get("role"),
      "user_session": user_session,
      "message": self.request.get("message"),
      "service": service[0]
    }
    language = None
    if "language" in self.request.cookies:
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    language = language.replace('"', '').replace("'", "")
    if language == "fr":

      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_edit_service.html')
    else:
      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('edit_service.html')
    
    self.response.write(LEGACY_TEMPLATE.render(template_values))

  def post(self, service_id):
    role = self.session.get('role')
    user_session = self.session.get("user")

    if role != "admin":
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return

    sql_statement = """
      SELECT id FROM service WHERE id="{0}"
      """.format(service_id)
    service = QueryHandler.execute_query(sql_statement)
    if len(service) > 0:
      ServiceHelper.update_record(self, service_id)
      self.redirect("/admin/services/" + service_id + "?message=Update complete")
    else:
      self.redirect("/admin?message=Service does not exist")
