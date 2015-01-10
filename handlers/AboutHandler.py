import os
import jinja2
import webapp2
from LegacyHandler import LegacyHandler

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname( __file__ ), '..', 'templates')))

TEMPLATE = JINJA_ENVIRONMENT.get_template('base.html')
LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('about.html')

class AboutHandler(LegacyHandler):
  def get(self):
    if not self.legacy:
      self.redirect("/#/about")
    template_values = {}
    self.response.write(LEGACY_TEMPLATE.render(template_values))