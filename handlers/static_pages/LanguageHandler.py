from handlers import BaseHandler


class LanguageHandler(BaseHandler.BaseHandler):
  def get(self):
    language = self.request.get("language")
    self.response.set_cookie("language", language)
    self.redirect("/")
