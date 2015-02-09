import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import Service

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../../templates/admin"),
         os.path.join(os.path.dirname(__file__),"../../../templates/layouts")]))

LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('services_index.html')

class AdminServiceIndexHandler(BaseHandler.BaseHandler):
  def get(self):
    role = self.session.get('role')
    user_session = self.session.get("user")
    if role != "admin":
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return

    if not self.legacy:
      self.redirect("/#/admin/services")

    #o = Organization.Organization(name = "first org")
    #o.put()

    services = Service.Service.query().order(Service.Service.name)

    template_values = {
      "services": services,
      "message": self.request.get("message"),
      "user_session": user_session
    }
    self.response.write(LEGACY_TEMPLATE.render(template_values))