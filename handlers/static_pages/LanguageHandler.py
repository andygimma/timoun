from handlers import BaseHandler


class LanguageHandler(BaseHandler.BaseHandler):
  def get(self):
    language = self.request.get("language")
    self.response.set_cookie("language", language)
    redirect = self.request.get("redirect")
    if redirect == "/":
      raise Exception(1)
      self.redirect("/")
    if redirect == "/search":
      raise Exception(2)
      self.redirect("/search")
    raise Exception(redirect)
