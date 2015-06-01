import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import Service
from models import Audit
import json


class AdminServiceDeleteHandler(BaseHandler.BaseHandler):
  def get(self, service_key):
    user_session = self.session.get('user')

    role = self.session.get('role')

    if role != "admin" and role != "staff":
      self.redirect("/users/login?message=Unauthorized action")
      return
    else:
      service = Service.Service.get_by_id(int(service_key))
      name = service.name
      service_dict = {
        "service": "Delete service '{0}'".format(name)
      }
      service_json = json.dumps(service_dict)

      user_audit = Audit.save(initiated_by = self.session.get("user"), organization_affected = self.request.get("name"), security_clearance = "admin", json_data = service_json, model= "Service", action = "Delete Service")
      service.key.delete()
      self.redirect("/admin/services?message={0} {1}".format(name, " deleted"))
