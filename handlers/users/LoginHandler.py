import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import User

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/users"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

TEMPLATE = JINJA_ENVIRONMENT.get_template('login.html')

class LoginHandler(BaseHandler.BaseHandler):
  def get(self):
    if self.session.get('user'):
      del self.session['user']

    if self.session.get('role'):
      del self.session['role']

    if not self.legacy:
      self.redirect("/#/users/login")
      return

    user = self.session.get('user')
    template_values = {
      'form': User.UserLoginForm(self.request.POST),
      'message': self.request.get("message")
    }

    users = User.User.query(User.User.email == "admin@example.com")
    language = None
    if "language" in self.request.cookies:
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    language = language.replace('"', '').replace("'", "")
    if language == "fr":

      TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_login.html')
    else:
      TEMPLATE = JINJA_ENVIRONMENT.get_template('login.html')
    if users.count() == 0:
      user = User.User(name = "admin", email = "admin@example.com", organization = "org", phone = "phone", role = "admin", password_digest = User.hash_password("secret"), email_authorized = True)
      user.put()

    self.response.write(TEMPLATE.render(template_values))

  def post(self):
    form = User.UserLoginForm(self.request.POST)
    if form.validate():
      User.authenticate(self, TEMPLATE, form)
    else:
      self.response.write(TEMPLATE.render({"form": form}))

