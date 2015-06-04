import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import Program
from models import Audit
import json
from helpers import QueryHandler


class AdminProgramDeleteHandler(BaseHandler.BaseHandler):
  def get(self, org_key):
    user_session = self.session.get('user')

    role = self.session.get('role')
    if role != "admin":
      self.redirect("/users/login?message=Unauthorized action")
      return
    else:
      sql_statement = "SELECT id FROM org_prog WHERE id={0}".format(org_key)
      programs = QueryHandler.execute_query(sql_statement)
      sql_statement = "DELETE FROM org_prog WHERE id={0}".format(org_key)
      # raise Exception(sql_statement)
      update = QueryHandler.execute_query(sql_statement, True)


      program_dict = {
        "program": "Delete program '{0}'".format(org_key)
      }
      program_json = json.dumps(program_dict)

      user_audit = Audit.save(initiated_by = self.session.get("user"), organization_affected = self.request.get("name"), security_clearance = "admin", json_data = program_json, model= "Program", action = "Delete Program")
      self.redirect("/admin?message={0}".format("program deleted"))
