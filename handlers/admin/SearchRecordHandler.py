import os
import jinja2
import webapp2
from models import SearchRecord
from handlers import BaseHandler
import json

_INSTANCE_NAME = 'timoun-production:surveydata'
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/admin"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('searches.html')

class SearchRecordHandler(BaseHandler.BaseHandler):
  def get(self):
  	role = self.session.get('role')
  	user_session = self.session.get("user")

  	if role != "admin":
  	  self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
  	  return

  	if not self.legacy:
  	  self.redirect("/#/admin/users/new")
  	searches = SearchRecord.SearchRecord.query()
  	template_values = {
	  	"searches": searches,
	  	"message": self.request.get("message"),
	  	"user_session": user_session,
  	}
  	language = None
  	if "language" in self.request.cookies:
  	  language = self.request.cookies["language"]
  	else:
  	  language = "fr"
  	  self.response.set_cookie("language", "fr")

  	language = language.replace('"', '').replace("'", "")
  	if language == "fr":

  	  LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_searches.html')
  	else:
  	  LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('searches.html')
  	self.response.write(LEGACY_TEMPLATE.render(template_values))
