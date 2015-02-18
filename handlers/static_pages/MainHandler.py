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
LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_index.html')

class MainHandler(BaseHandler.BaseHandler):
  def get(self):
    if self.legacy:
      template = LEGACY_TEMPLATE
    else:
      template = TEMPLATE
    role = self.session.get('role')
    user_session = self.session.get("user")
    records = Record.Record.query(Record.Record.latitude != "empty")
    #raise Exception(records.count())
    records = records.fetch(50, projection=[Record.Record.gps_, Record.Record.latitude, Record.Record.longitude, Record.Record.nom_de_lorganisation])
    #raise Exception(len(records))
    template_values = {
      "role": self.session.get("role"),
      "user_session": user_session,
      "message": self.request.get("message"),
      "records": records
    }
    self.response.write(template.render(template_values))
