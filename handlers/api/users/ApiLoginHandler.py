import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import User

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../../templates/users"),
         os.path.join(os.path.dirname(__file__),"../../../templates/layouts")]))

TEMPLATE = JINJA_ENVIRONMENT.get_template('login.html')

class ApiLoginHandler(BaseHandler.BaseHandler):
  def post(self):
    if self.session.get('user'):
      del self.session['user']

    if self.session.get('role'):
      del self.session['role']

    form = User.UserLoginForm(self.request.POST)
    if form.validate():
      User.authenticate(self, TEMPLATE, form)
    else:
      self.response.write(TEMPLATE.render({"form": form}))
