import webapp2
from webapp2_extras import sessions
import logging


class BaseHandler(webapp2.RequestHandler):
  def dispatch(self):
    USER_AGENT = self.request.headers['User-Agent']
    legacy_param = self.request.params.get("legacy")
    logging.info(USER_AGENT)
    #legacy_param = False
    self.legacy = True


    # Get a session store for this request.
    self.session_store = sessions.get_store(request=self.request)

    try:
      # Dispatch the request.
      webapp2.RequestHandler.dispatch(self)
    finally:
      # Save all sessions.
      self.session_store.save_sessions(self.response)


  @webapp2.cached_property
  def session(self):
      # Returns a session using the default cookie key.
    return self.session_store.get_session()
