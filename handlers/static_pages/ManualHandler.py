import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import User
from models import Audit
import json

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/static_pages"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

TEMPLATE = JINJA_ENVIRONMENT.get_template('manual.html')

class ManualHandler(BaseHandler.BaseHandler):
  def get(self):
    if not self.legacy:
      self.redirect("/#/manual")
    role = self.session.get('role')
    user_session = self.session.get("user")

    if role != "admin":
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return

    user_session = self.session.get('user')
    role = self.session.get('role')

    template_values = {
      "message": self.request.get("message"),
      "user_session": user_session,
      "role": role
    }
    self.response.write(TEMPLATE.render(template_values))
