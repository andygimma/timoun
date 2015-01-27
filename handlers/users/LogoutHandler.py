from handlers import BaseHandler


class LogoutHandler(BaseHandler.BaseHandler):
  def get(self):
    if self.session.get('user'):
      del self.session['user']

    if self.session.get('role'):
      del self.session['role']
    self.redirect("/")
