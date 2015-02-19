import os
import jinja2
import webapp2
from handlers import BaseHandler

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/static_pages"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('en_search.html')

class SearchHandler(BaseHandler.BaseHandler):
  def get(self):
    language = None
    if "language" in self.request.cookies and self.request.cookies["language"] == "fr" or self.request.cookies["language"] == "en":
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    if language == "fr":
      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_search.html')
    else:
      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('en_search.html')

    if not self.legacy:
      self.redirect("/#/search")
    role = self.session.get('role')
    user_session = self.session.get("user")
    template_values = {
      "role": self.session.get("role"),
      "user_session": user_session,
      "message": self.request.get("message")
    }
    self.response.write(LEGACY_TEMPLATE.render(template_values))
