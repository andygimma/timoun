import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import Program

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../../templates/admin"),
         os.path.join(os.path.dirname(__file__),"../../../templates/layouts")]))

TEMPLATE = JINJA_ENVIRONMENT.get_template('edit_program.html')

class AdminProgramEditHandler(BaseHandler.BaseHandler):
  def get(self, program_key):
    role = self.session.get('role')
    user_session = self.session.get("user")

    if role != "admin":
      self.redirect("/programs/login?message={0}".format("You are not authorized to view this page"))
      return

    if not self.legacy:
      self.redirect("/#/programs/{0}/edit".format(program_key))

    program = Program.Program.get_by_id(int(program_key))
    if not program:
      self.response.write(TEMPLATE.render({"form": form, "message": "Unable to find program. Please contact administrator."}))

    form = Program.NewProgramForm()
    form.name.data = program.name

    template_values = {
      "role": self.session.get("role"),
      "user_session": user_session,
      "message": self.request.get("message"),
      "form": form,
      "program_key": program_key,
      "program_name": program.name
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
    self.response.write(TEMPLATE.render(template_values))

  def post(self, program_key):
    role = self.session.get('role')
    user_session = self.session.get("user")

    if role != "admin":
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return

    program = Program.Program.get_by_id(int(program_key))
    if not program:
      self.response.write(TEMPLATE.render({"form": form, "message": "Unable to find program. Please contact administrator."}))

    form = Program.NewProgramForm(self.request.POST)
    if form.validate():
      Program.update(self, TEMPLATE, form, program.name, program_key)
    else:
      self.response.write(TEMPLATE.render({"form": form}))
