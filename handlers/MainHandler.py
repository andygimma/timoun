import os
import jinja2
import webapp2
import logging
import re

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname( __file__ ), '..', 'templates')))

TEMPLATE = JINJA_ENVIRONMENT.get_template('base.html')
LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('index.html')

class MainHandler(webapp2.RequestHandler):
  def get(self):
    USER_AGENT = self.request.headers['User-Agent']
    legacy = self.request.params.get("legacy")
    logging.info(USER_AGENT)
    template_values = {}
    legacy = False
    if legacy or "MSIE 6" in USER_AGENT or "MSIE 7" in self.request.headers["User-Agent"] or "MSIE 8" in self.request.headers["User-Agent"]:
      template = LEGACY_TEMPLATE
    else:
      template = TEMPLATE
    self.response.write(template.render(template_values))