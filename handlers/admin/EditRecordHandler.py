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
    if role != "admin":
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return

    record = Record.Record.get_by_id(int(record_id))
    if not record:
      self.response.write(TEMPLATE.render({"form": form, "message": "Unable to find Record. Please contact administrator."}))

    form = Record.RecordForm()
    template_values = {
      "message": self.request.get("message"),
      "user_session": user_session,
      "form": form,
      "record": record,
      
    }
    self.response.write(LEGACY_TEMPLATE.render(template_values))
