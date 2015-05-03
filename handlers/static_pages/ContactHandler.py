import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import User
from google.appengine.api import mail
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/static_pages"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

class ContactHandler(BaseHandler.BaseHandler):
  def get(self):
    role = self.session.get('role')
    user_session = self.session.get("user")
    template_values = {
      "role": self.session.get("role"),
      "user_session": user_session,
      "message": self.request.get("message")
    }

    language = None
    if "language" in self.request.cookies:
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    language = language.replace('"', '').replace("'", "")
    if language == "fr":

      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_contact.html')
    else:
      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('en_contact.html')
    self.response.write(LEGACY_TEMPLATE.render(template_values))

  def post(self):
    contact_email(self.request.get("name"), self.request.get("email"), self.request.get("subject"), self.request.get("contact_message"))
    # raise Exception(self.request.get("contact_message"))
    self.redirect("/contact?message=Success")


def contact_email(name, email, subject, my_message):
  user_email = ""
  users = User.User.query(User.User.role == "admin")
  users = users.fetch(1000)
  # raise Exce/ption(len(users))
  for user in users:
    user_email = user.email
    message = mail.EmailMessage(sender="IBESR <ibesr@bscht.org>",
                              subject="Contact Information Sent")

    message.to = "<%s>" % user_email
    message.body = """
    Nom/Name: {0}
    Email: {1}
    Sujet/Subject: {2}
    Message: {3}

    """.decode("utf-8").format(name, email, subject, my_message)
    # raise Exception(message.body)
    # raise Exception(my_message)
    message.send()

    logging.info("contact email sent to " + user.email)