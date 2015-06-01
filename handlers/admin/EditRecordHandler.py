import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import Record

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/admin"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('edit_record.html')

class EditRecordHandler(BaseHandler.BaseHandler):
  def get(self, record_id):
    role = self.session.get('role')
    user_session = self.session.get("user")
    if role != "admin" and role != "staff":
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return

    record = Record.Record.get_by_id(int(record_id))
    if not record:
      self.response.write(TEMPLATE.render({"form": form, "message": "Unable to find Record. Please contact administrator."}))

    form = Record.RecordForm()
    record_dict = record.to_dict()
    for obj in record_dict:
      try:
        form[obj].data = record_dict[obj]
      except:
        pass

    template_values = {
      "message": self.request.get("message"),
      "user_session": user_session,
      "form": form,
      "record": record,

    }
    language = None
    if "language" in self.request.cookies:
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    language = language.replace('"', '').replace("'", "")
    if language == "fr":

      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_edit_record.html')
    else:
      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('edit_record.html')
    self.response.write(LEGACY_TEMPLATE.render(template_values))

  def post(self, record_id):
    role = self.session.get('role')
    user_session = self.session.get("user")

    if role != "admin":
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return

    record = Record.Record.get_by_id(int(record_id))
    if not record:
      self.response.write(LEGACY_TEMPLATE.render({"form": form, "message": "Unable to find program. Please contact administrator."}))

    form = Record.RecordForm(self.request.POST)
    if form.validate():
      Record.update(self, LEGACY_TEMPLATE, form, record_id)
    else:
      self.response.write(LEGACY_TEMPLATE.render({"form": form}))
