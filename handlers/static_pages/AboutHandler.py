import os
import jinja2
import webapp2
from handlers import BaseHandler

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/static_pages"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('about.html')

class AboutHandler(BaseHandler.BaseHandler):
  def get(self):
    if not self.legacy:
      self.redirect("/#/about")
      return
    role = self.session.get('role')
    user_session = self.session.get("user")
    template_values = {
      "role": self.session.get("role"),
      "user_session": user_session,
      "message": self.request.get("message")
    }
    self.response.write(LEGACY_TEMPLATE.render(template_values))
