import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import Organization
from models import Audit
import json


class AdminOrgDeleteHandler(BaseHandler.BaseHandler):
  def get(self, org_key):
    user_session = self.session.get('user')

    role = self.session.get('role')

    if role != "admin":
      self.redirect("/users/login?message=Unauthorized action")
      return
    else:
      organization = Organization.Organization.get_by_id(int(org_key))
      name = organization.name
      org_dict = {
        "org": "Delete organization '{0}'".format(name)
      }
      org_json = json.dumps(org_dict)

      user_audit = Audit.save(initiated_by = self.session.get("user"), organization_affected = self.request.get("name"), security_clearance = "admin", json_data = org_json, model= "Organization", action = "Delete Organization")
      organization.key.delete()
      self.redirect("/admin/organizations?message={0} {1}".format(name, " deleted"))
