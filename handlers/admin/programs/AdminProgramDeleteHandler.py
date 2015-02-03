import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import Program
from models import Audit
import json


class AdminProgramDeleteHandler(BaseHandler.BaseHandler):
  def get(self, org_key):
    user_session = self.session.get('user')

    role = self.session.get('role')

    if role != "admin":
      self.redirect("/users/login?message=Unauthorized action")
      return
    else:
      program = Program.Program.get_by_id(int(org_key))
      name = program.name
      program_dict = {
        "program": "Delete program '{0}'".format(name)
      }
      program_json = json.dumps(program_dict)

      user_audit = Audit.save(initiated_by = self.session.get("user"), organization_affected = self.request.get("name"), security_clearance = "admin", json_data = program_json, model= "Program", action = "Delete Program")
      program.key.delete()
      self.redirect("/admin/programs?message={0} {1}".format(name, " deleted"))
