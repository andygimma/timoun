from google.appengine.ext import webapp
#import model
from google.appengine.api import memcache
import logging
#from controllers.datastore_results import datastore_results
from gaesessions import get_current_session
register = webapp.template.create_template_register()

#@register.simple_tag


@register.filter(name="humanize_text")
def humanize_text(string):
    string = string.replace("_", " ")
    string = string.title()
    return string
