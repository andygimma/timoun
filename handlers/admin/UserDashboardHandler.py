import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import Audit

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/admin"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('user_dashboard.html')

class UserDashboardHandler(BaseHandler.BaseHandler):
  def get(self):

    role = self.session.get('role')
    user_session = self.session.get("user")
    if role != "admin" and role != "staff":
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return

    if not self.legacy:
      self.redirect("/#/admin")

    audits = Audit.Audit.query(Audit.Audit.model_affected == "User").order(Audit.Audit.created_at)


    template_values = {
      "message": self.request.get("message"),
      "user_session": user_session,
      "audits": audits
    }
    language = None
    if "language" in self.request.cookies:
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    language = language.replace('"', '').replace("'", "")
    if language == "fr":

      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_user_dashboard.html')
    else:
      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('user_dashboard.html')
    self.response.write(LEGACY_TEMPLATE.render(template_values))
