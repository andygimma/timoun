from google.appengine.ext import ndb
from wtforms import Form, BooleanField, StringField, SelectField, PasswordField, validators
from wtforms.ext.appengine.db import model_form
import Audit
import json

class Program(ndb.Model):
  name = ndb.StringProperty(required=True)

def save(self, form, LEGACY_TEMPLATE):
  programs = Program.query(Program.name == self.request.get("name"))
  if programs.count() == 0:
    program = Program(name=self.request.get("name"))
    if program.put():
      program_dict = {
        "name": program.name,
      }
      program_json = json.dumps(program_dict)
      program_audit = Audit.save(initiated_by = self.session.get("user"), organization_affected = self.request.get("name"), security_clearance = "admin", json_data = program_json, model= "Program", action = "Create Program")
      self.redirect("/admin/programs?message=Program {0} added".format(self.request.get("name")))
    else:
      self.response.write(LEGACY_TEMPLATE.render({"form": form, "message": "Program not saved, contact administrator"}))
  else:
    self.response.write(LEGACY_TEMPLATE.render({"form": form, "message": "A program with that name already exists"}))

def update(self, TEMPLATE, form, program_name, program_key=None):
    programs = Program.query(Program.name == program_name)
    program = None
    for program in programs:
      program = program

    program.name = form.name.data
    if program.put():
      program_dict = {
        "name": program.name,
      }
      program_json = json.dumps(program_dict)
      program_audit = Audit.save(initiated_by = self.session.get("user"), organization_affected = self.request.get("name"), security_clearance = "admin", json_data = program_json, model= "Program", action = "Edit Program")
      if program_key:
        self.redirect("/programs/{0}/edit?message={1}".format(program_key, "Program updated successfully"))
      else:
        self.redirect("/admin/programs?message={0}".format("Program updated successfully"))
    else:
      self.response.write(TEMPLATE.render({"form": form, "message": "Program update unsuccessful. Please contact administrator."}))


class NewProgramForm(Form):
  name = StringField('Name', [validators.Length(min=1, max=35)])
