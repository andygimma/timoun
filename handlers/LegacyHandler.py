import webapp2
from webapp2_extras import sessions
import logging

class LegacyHandler(webapp2.RequestHandler):
  def dispatch(self):
    USER_AGENT = self.request.headers['User-Agent']
    legacy_param = self.request.params.get("legacy")
    logging.info(USER_AGENT)
    legacy_param = True
    if legacy_param or "MSIE 6" in USER_AGENT or "MSIE 7" in USER_AGENT:
      self.legacy = True
    else:
      self.legacy = False
      
    try:
      # Dispatch the request.
      webapp2.RequestHandler.dispatch(self)
    finally:
      # Save all sessions.
      #self.session_store.save_sessions(self.response)
      pass