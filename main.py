import webapp2
import jinja2
import os

from handlers import MainHandler

app = webapp2.WSGIApplication([
    ('/', MainHandler.MainHandler),
], debug=True)