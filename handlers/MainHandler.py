import os
import jinja2
import webapp2
from LegacyHandler import LegacyHandler


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname( __file__ ), '..', 'templates')))

TEMPLATE = JINJA_ENVIRONMENT.get_template('base.html')
LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('index.html')

class MainHandler(LegacyHandler):
  def get(self):
    template_values = {}
    if self.legacy:
      template = LEGACY_TEMPLATE
    else:
      template = TEMPLATE
    self.response.write(template.render(template_values))