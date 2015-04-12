import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import User

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/users"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

TEMPLATE = JINJA_ENVIRONMENT.get_template('set_password.html')

class SetPasswordHandler(BaseHandler.BaseHandler):
  def get(self, email_endpoint):
    if not self.legacy:
      self.redirect("/#/users/set_password")

    if self.session.get('user'):
      del self.session['user']

    if self.session.get('role'):
      del self.session['role']

    template_values = {
      "message": self.request.get("message"),
      "form": User.UserConfirmationForm(),
      "email_endpoint": email_endpoint
    }
    language = None
    if "language" in self.request.cookies:
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    language = language.replace('"', '').replace("'", "")
    if language == "fr":

      TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_set_password.html')
    else:
      TEMPLATE = JINJA_ENVIRONMENT.get_template('set_password.html')
    self.response.write(TEMPLATE.render(template_values))

  def post(self, email_endpoint):
    form = User.UserConfirmationForm(self.request.POST)
    if form.validate():
      User.reset_password(self, form, TEMPLATE, email_endpoint)
    else:
      self.response.write(TEMPLATE.render({"form": form}))
