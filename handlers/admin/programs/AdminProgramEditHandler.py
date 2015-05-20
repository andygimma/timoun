import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import Program
from helpers import QueryHandler, ProgramHelper

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../../templates/admin"),
         os.path.join(os.path.dirname(__file__),"../../../templates/layouts")]))

TEMPLATE = JINJA_ENVIRONMENT.get_template('edit_program.html')

class AdminProgramEditHandler(BaseHandler.BaseHandler):
  def get(self, program_id):
    role = self.session.get('role')
    user_session = self.session.get("user")

    if role != "admin":
      self.redirect("/programs/login?message={0}".format("You are not authorized to view this page"))
      return

    sql_statement = """
          SELECT * FROM org_prog WHERE id='{0}' LIMIT 1
        """.format(program_id)


    program = QueryHandler.execute_query(sql_statement)

    org_select = """
        SELECT 1_nom FROM organization WHERE id="{0}"
    """.format(program[0][1])

    org = QueryHandler.execute_query(org_select)
    if len(program) == 0:
      self.redirect("/admin?message=That program does not exist")
      return
    template_values = {
      "role": self.session.get("role"),
      "user_session": user_session,
      "message": self.request.get("message"),
      "program": program[0],
      "org": org[0][0]
    }
    language = None
    if "language" in self.request.cookies:
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    language = language.replace('"', '').replace("'", "")
    if language == "fr":

      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_edit_program.html')
    else:
      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('edit_program.html')
    self.response.write(LEGACY_TEMPLATE.render(template_values))

  def post(self, program_id):
    role = self.session.get('role')
    user_session = self.session.get("user")

    program_id = self.request.get("program_id")

    if role != "admin":
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return

    sql_statement = """
      SELECT id FROM org_prog WHERE id="{0}"
      """.format(program_id)
    program = QueryHandler.execute_query(sql_statement)
    if len(program) > 0:
      ProgramHelper.update_record(self)
      self.redirect("/programs/" + program_id + "/edit?message=Update complete")
    else:
      self.redirect("/admin?message=Program does not exist")

    
