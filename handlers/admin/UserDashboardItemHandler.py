import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import Audit
import json

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/admin"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('dashboard_item.html')

class UserDashboardItemHandler(BaseHandler.BaseHandler):
  def get(self, audit_id):

    role = self.session.get('role')
    user_session = self.session.get("user")

    if role != "admin":
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return

    if not self.legacy:
      self.redirect("/#/admin")

    audit = Audit.Audit.get_by_id(int(audit_id))
    json_obj = json.loads(audit.json_data)

    template_values = {
      "message": self.request.get("message"),
      "user_session": user_session,
      "audit": audit,
      "json_obj": json_obj
    }
    language = None
    if "language" in self.request.cookies:
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    language = language.replace('"', '').replace("'", "")
    if language == "fr":

      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_dashboard_item.html')
    else:
      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('dashboard_item.html')
    self.response.write(LEGACY_TEMPLATE.render(template_values))
