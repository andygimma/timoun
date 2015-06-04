import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import Organization
from models import Audit
import json
from helpers import QueryHandler


class AdminOrgDeleteHandler(BaseHandler.BaseHandler):
  def get(self, org_key):
    user_session = self.session.get('user')

    role = self.session.get('role')

    if role != "admin":
      self.redirect("/users/login?message=Unauthorized action")
      return
    else:
      sql_statement = "SELECT 1_nom, id FROM organization WHERE id={0}".format(org_key)
      records = QueryHandler.execute_query(sql_statement)
      org_dict = {
        "org": "Delete organization '{0}'".format(records[0][0])
      }
      org_json = json.dumps(org_dict)
      sql_statement = """
        UPDATE `organization` SET
        `is_deleted` = 1
        WHERE `id` = "{0}"
        LIMIT 1;
      """.format(records[0][1])
      update = QueryHandler.execute_query(sql_statement, True)
      user_audit = Audit.save(initiated_by = self.session.get("user"), organization_affected = self.request.get("name"), security_clearance = "admin", json_data = org_json, model= "Organization", action = "Delete Organization")
      self.redirect("/admin/records?message={0} {1}".format(records[0][0], " deleted"))
