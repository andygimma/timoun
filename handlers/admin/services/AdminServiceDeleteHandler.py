import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import Service
from models import Audit
import json
from helpers import QueryHandler


class AdminServiceDeleteHandler(BaseHandler.BaseHandler):
  def get(self, service_key):
    user_session = self.session.get('user')

    role = self.session.get('role')

    if role != "admin":
      self.redirect("/users/login?message=Unauthorized action")
      return
    else:
      sql_statement = "SELECT name_french, id FROM service WHERE id={0}".format(service_key)
      services = QueryHandler.execute_query(sql_statement)
      sql_statement = "DELETE FROM service WHERE id={0}".format(service_key)
      update = QueryHandler.execute_query(sql_statement, True)
      service_dict = {
        "service": "Delete service '{0}'".format(services[0][0].encode("utf-8"))
      }
      service_json = json.dumps(service_dict)

      user_audit = Audit.save(initiated_by = self.session.get("user"), organization_affected = self.request.get("name"), security_clearance = "admin", json_data = service_json, model= "Service", action = "Delete Service")
      self.redirect("/admin?message={0} {1}".format(services[0][0].encode("utf-8"), " deleted"))
