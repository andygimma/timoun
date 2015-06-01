import os
import jinja2
import webapp2
from handlers import BaseHandler
from google.appengine.ext import db
from models import Record
from helpers import QueryHandler

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/static_pages"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('view_public_records.html')

class PublicRecordHandler(BaseHandler.BaseHandler):
  def get(self, record_id):

    role = self.session.get('role')  
    user_session = self.session.get("user")


    sql_statement = """
      SELECT * FROM organization WHERE id='{0}' LIMIT 1
    """.format(record_id)


    record = QueryHandler.execute_query(sql_statement)
    sql_services = "SELECT name_french, id  FROM service WHERE org_id = {0};".format(record_id)
    services = QueryHandler.execute_query(sql_services)


    sql_programs = """SELECT DISTINCT(`program_id`), `program`.`name_french`, `program`.`name_english`
      FROM `service`
      LEFT JOIN `program`
      ON `service`.`program_id` = `program`.`id`
      WHERE `service`.`org_id` = {0};
    """.format(record_id)
    programs = QueryHandler.execute_query(sql_programs)

    template_values = {
      "message": self.request.get("message"),
      "user_session": user_session,
      "record": record[0],
      "services": services,
      "programs": programs
    }
    language = None
    if "language" in self.request.cookies:
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    language = language.replace('"', '').replace("'", "")
    if language == "fr":

      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_view_public_records.html')
    else:
      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('view_public_records.html')
    self.response.write(LEGACY_TEMPLATE.render(template_values))
