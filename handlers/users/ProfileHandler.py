import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import User
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/users"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

TEMPLATE = JINJA_ENVIRONMENT.get_template('profile.html')

class ProfileHandler(BaseHandler.BaseHandler):
  def get(self):
    if not self.legacy:
      self.redirect("/#/users/profile")

    user_session = self.session.get("user")

    if not user_session:
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return

    role = self.session.get('role')
    users = User.User.query(User.User.email == user_session)
    user = None
    for user in users:
      user = user
    user_dict = user.to_dict()
    form = User.UserProfileForm()

    for obj in user_dict:
      try:
        form[obj].data = user_dict[obj]
      except:
        pass

    template_values = {
      "role": self.session.get("role"),
      "user_session": user_session,
      "message": self.request.get("message"),
      "form": form,
      "role": user.role
    }
    language = None
    if "language" in self.request.cookies:
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    language = language.replace('"', '').replace("'", "")
    if language == "fr":

      TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_profile.html')
    else:
      TEMPLATE = JINJA_ENVIRONMENT.get_template('profile.html')
    self.response.write(TEMPLATE.render(template_values))
    self.response.write(TEMPLATE.render(template_values))

  def post(self):
    user_session = self.session.get("user")
    if not user_session:
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return

    form = User.UserProfileForm(self.request.POST)
    if form.validate():
      User.update(self, TEMPLATE, form, user_session)
    else:
      self.response.write(TEMPLATE.render({"form": form}))
