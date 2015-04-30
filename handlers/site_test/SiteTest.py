import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import User

class SiteTest(BaseHandler.BaseHandler):
  def get(self):
    users = User.User.query()
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('Site is live')  
