import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import User

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/users"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

TEMPLATE = JINJA_ENVIRONMENT.get_template('reset_password.html')

class ResetPasswordHandler(BaseHandler.BaseHandler):
  def get(self):
    if not self.legacy:
      self.redirect("/#/users/reset_password")

    if self.session.get('user'):
      del self.session['user']

    if self.session.get('role'):
      del self.session['role']

    template_values = {
      "message": self.request.get("message"),
      "form": User.UserResetPasswordForm()
    }
    self.response.write(TEMPLATE.render(template_values))

  def post(self):
    form = User.UserResetPasswordForm(self.request.POST)
    if form.validate():
      User.send_reset_password_email(self, form, TEMPLATE)
    else:
      self.response.write(TEMPLATE.render({"form": form}))
