from handlers import BaseHandler


class LanguageHandler(BaseHandler.BaseHandler):
  def get(self):
    language = self.request.get("language")
    self.response.set_cookie("language", language)
    redirect = self.request.get("redirect").replace("'", "")
    if redirect == "/":
      self.redirect("/")
      return
    if redirect == "/search":
      self.redirect("/search")
      return
    if redirect == "/services":
      self.redirect("/mental_illness_services")
      return
