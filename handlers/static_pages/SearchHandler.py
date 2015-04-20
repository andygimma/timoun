from google.appengine.ext import ndb
import os
import jinja2
import webapp2
from handlers import BaseHandler
from helpers import QueryHandler

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/static_pages"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('en_search.html')

class SearchHandler(BaseHandler.BaseHandler):
  def get(self):
    keywords = self.request.get("keywords")
    service = self.request.get("service")
    department = self.request.get("department")
    age_start = self.request.get("age_start")
    age_end = self.request.get("age_end")
    gender = self.request.get("gender")
    records = []

    if False:
      pass

    else: 
      page = self.request.get("page")
      if page == None:
        page = 0

      sql_statement = """SELECT `name_french` AS `service_name_fr`, `name_english`  AS `service_name_en`, `org_id`, `org_nom`, `org_email`, `org_phone`, `program_id`, `latitude`, `longitude`, COUNT(DISTINCT(`name_french`)) AS `service_count`
        FROM `service`
        GROUP BY `org_id`
        LIMIT 25
        """
      if search(self):
        records = QueryHandler.form_query_builder(self)
      
      language = None
      if "language" in self.request.cookies:
        language = self.request.cookies["language"]
      else:
        language = "fr"
        self.response.set_cookie("language", "fr")

      language = language.replace('"', '').replace("'", "")
      if language == "fr":
        LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_search.html')
      else:
        LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('en_search.html')

      if not self.legacy:
        self.redirect("/#/search")

      role = self.session.get('role')
      user_session = self.session.get("user")
      template_values = {
        "role": self.session.get("role"),
        "user_session": user_session,
        "message": self.request.get("message"),
        "records": records
      }

      self.response.write(LEGACY_TEMPLATE.render(template_values))

def search(self):
  keywords = self.request.get("keywords")
  service = self.request.get("service")
  department = self.request.get("department")
  age_start = self.request.get("age_start")
  age_end = self.request.get("age_end")
  gender = self.request.get("gender")

  if keywords or service or department or age_start or age_end or gender:
    return True
  else:
    return False

