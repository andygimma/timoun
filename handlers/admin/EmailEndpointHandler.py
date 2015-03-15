import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import User

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/admin"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

TEMPLATE = JINJA_ENVIRONMENT.get_template('email_endpoint.html')

class EmailEndpointHandler(BaseHandler.BaseHandler):
  def get(self, email_endpoint):
    if not self.legacy:
      self.redirect("/#/admin/users/{0}".format(email_endpoint))

    users = User.User.query(User.User.email_endpoint == email_endpoint).order(User.User.email).fetch(1)
    user = None
    for user in users:
      user = user

    if not user:
      self.redirect("/")
      return

    template_values = {
      "message": self.request.get("message"),
      "user": user,
      "form": User.UserConfirmationForm(),
      "email_endpoint": email_endpoint,
    }
    language = None
    if "language" in self.request.cookies:
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    language = language.replace('"', '').replace("'", "")
    if language == "fr":

      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_email_endpoint.html')
    else:
      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('email_endpoint.html')
    self.response.write(TEMPLATE.render(template_values))

  def post(self, email_endpoint):
    form = User.UserConfirmationForm(self.request.POST)
    if form.validate():
      user = User.confirm_email(self, form, TEMPLATE, email_endpoint)
    else:
      self.response.write(TEMPLATE.render({"form": form, "email_endpoint": email_endpoint}))
