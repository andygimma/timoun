from handlers import BaseHandler


class LanguageHandler(BaseHandler.BaseHandler):
  def get(self):
    # raise Exception(self.request)
    language = self.request.get("language")
    self.response.set_cookie("language", language)
    redirect = self.request.get("redirect").replace("'", "")
    self.redirect(self.request.referer)
    return
