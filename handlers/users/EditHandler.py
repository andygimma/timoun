import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import User

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/users"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

TEMPLATE = JINJA_ENVIRONMENT.get_template('edit_user.html')

class EditHandler(BaseHandler.BaseHandler):
  def get(self, user_key):
    role = self.session.get('role')
    user_session = self.session.get("user")

    if role != "admin":
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return

    if not self.legacy:
      self.redirect("/#/users/{0}/edit".format(user_key))

    user = User.User.get_by_id(int(user_key))
    if not user:
      self.response.write(TEMPLATE.render({"form": form, "message": "Unable to confirm user. Please contact administrator."}))

    form = User.UserForm()
    form.name.data = user.name
    form.organization.data = user.organization
    form.phone.data = user.phone
    form.email.data = user.email
    form.role.data = user.role


    template_values = {
      "role": self.session.get("role"),
      "user_session": user_session,
      "message": self.request.get("message"),
      "form": form,
      "user_key": user_key,
      "user_email": user.email,
    }
    language = None
    if "language" in self.request.cookies:
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    language = language.replace('"', '').replace("'", "")
    if language == "fr":

      TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_edit_user.html')
    else:
      TEMPLATE = JINJA_ENVIRONMENT.get_template('edit_user.html')
    self.response.write(TEMPLATE.render(template_values))

  def post(self, user_key):
    role = self.session.get('role')
    user_session = self.session.get("user")

    if role != "admin":
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return

    user = User.User.get_by_id(int(user_key))
    if not user:
      self.response.write(TEMPLATE.render({"form": form, "message": "Unable to confirm user. Please contact administrator."}))

    form = User.UserProfileForm(self.request.POST)
    if form.validate():
      User.update(self, TEMPLATE, form, user.email, user_key)
    else:
      self.response.write(TEMPLATE.render({"form": form}))
