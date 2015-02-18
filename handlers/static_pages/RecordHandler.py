import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import Record

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/static_pages"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))


TEMPLATE = JINJA_ENVIRONMENT.get_template('base.html')
LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('view_record.html')

class RecordHandler(BaseHandler.BaseHandler):
  def get(self, record_name):
    if self.legacy:
      template = LEGACY_TEMPLATE
    else:
      template = TEMPLATE
    role = self.session.get('role')
    user_session = self.session.get("user")
    record = Record.Record.query(Record.Record.nom_de_lorganisation == record_name).get()
    #raise Exception(record.nom_de_lorganisation)
    #raise Exception(records.count())
    #raise Exception(record.count())
    template_values = {
      "role": self.session.get("role"),
      "user_session": user_session,
      "message": self.request.get("message"),
      "record": record
    }
    self.response.write(template.render(template_values))
