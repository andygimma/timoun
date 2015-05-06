# -*- coding: utf-8 -*- 

import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import Record
from helpers import QueryHandler, ProgramHelper

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/admin"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('new_record.html')

class NewProgramHandler(BaseHandler.BaseHandler):
  def post(self):
    ProgramHelper.save_record(self)

  def get(self):
    role = self.session.get('role')
    user_session = self.session.get("user")

    if role != "admin":
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return

    org_id = self.request.get("record")

    sql_statement = "SELECT 1_nom FROM organization WHERE id={0} LIMIT 1".format(org_id)
    org = QueryHandler.execute_query(sql_statement)
    form = Record.RecordForm()
    template_values = {
      "form": form,
      "user_session": user_session,
      "org_id": self.request.get("record"),
      "org_name": org[0][0]
    }
    language = None
    if "language" in self.request.cookies:
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    language = language.replace('"', '').replace("'", "")
    if language == "fr":

      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_new_programs.html')
    else:
      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('new_programs.html')
    self.response.write(LEGACY_TEMPLATE.render(template_values))
