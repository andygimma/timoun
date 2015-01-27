import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import User
from models import Audit
import json

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/users"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

TEMPLATE = JINJA_ENVIRONMENT.get_template('login.html')

class DeleteHandler(BaseHandler.BaseHandler):
  def get(self, user_key):
    user_session = self.session.get('user')

    role = self.session.get('role')

    if role != "admin":
      self.redirect("/users/login?message=Unauthorized action")
      return
    else:
      user = User.User.get_by_id(int(user_key))
      email = user.email
      user_dict = {
        "user": "Delete user {0}".format(email)
      }
      user_json = json.dumps(user_dict)
      user_audit = Audit.save(initiated_by = user_session, user_affected = email, security_clearance = "admin", json_data = user_json, model= "User", action = "Delete User")
      user.key.delete()
      self.redirect("/admin/users?message={0} {1}".format(email, " deleted"))
