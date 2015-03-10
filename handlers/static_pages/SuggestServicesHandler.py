import os
import jinja2
import webapp2
from handlers import BaseHandler

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/static_pages"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))


class SuggestServicesHandler(BaseHandler.BaseHandler):
  def get(self):
    if not self.legacy:
      self.redirect("/#/suggest_services")
    role = self.session.get('role')
    user_session = self.session.get("user")
    template_values = {
      "role": self.session.get("role"),
      "user_session": user_session,
      "message": self.request.get("message")
    }

    language = None
    if "language" in self.request.cookies:
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    language = language.replace('"', '').replace("'", "")
    if language == "fr":

      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_suggest_services.html')
    else:
      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('en_suggest_services.html')

    self.response.write(LEGACY_TEMPLATE.render(template_values))
