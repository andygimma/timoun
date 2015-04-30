# -*- coding: utf-8 -*- 
import os
import jinja2
import webapp2
from handlers import BaseHandler
from google.appengine.api import mail

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/static_pages"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))


class SuggestServicesHandler(BaseHandler.BaseHandler):
  def get(self):
    if not self.legacy:
      self.redirect("/#/suggest_services")
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

      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_suggest_services.html')
    else:
      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('en_suggest_services.html')

    self.response.write(LEGACY_TEMPLATE.render(template_values))

  def post(self):
    data = { 
      "organization": self.request.get("organization"),
      "category": self.request.get("category"),
      "service": self.request.get("service"),
      "age": self.request.get("age"),
      "age_end": self.request.get("age_end"),
      "gender": self.request.get("gender"),
      "department": self.request.get("department"),
      "address": self.request.get("address"),
      "details": self.request.get("details"),
      "monday": self.request.get("monday"),
      "tuesday": self.request.get("tuesday"),
      "wednesday": self.request.get("wednesday"),
      "thursday": self.request.get("thursday"),
      "friday": self.request.get("friday"),
      "saturday": self.request.get("saturday"),
      "sunday": self.request.get("sunday")
    }

    confirmation_email(data)
    self.redirect("/?message='Email sent. Thank you!'")

def confirmation_email(data):
  # this will be changed
  user_email = "andy.n.gimma@gmail.com"
  message = mail.EmailMessage(sender="IBESR <ibesr@bscht.org>",
                            subject="Suggest Services Email Sent")

  message.to = "<%s>" % user_email
  message.body = """
  Votre demande d’ajouter un service a été autorisée. Voici les informations suivantes.
  A service suggestion has been sent. Here is the information.

  Organisation / Organisation: {0}

  Category / Catégorie: {1}

  Service / Service: {2}

  Tranche d'age / Start Age: {3}

  Age max / End Age: {4}

  Sexe / Gender: {5}

  Département / Department: {6}

  Adresse ou coordonnées / Address: {7}

  Details / Détails: {8}

  Jour de fontionnement / Day: {9}, {10}, {11}, {12}, {13}, {14}, {15}


  """.decode("utf-8").format(data["organization"], data["category"], data["service"], data["age"], data["age_end"], data["gender"], data["department"], data["address"], data["details"], data["monday"], data["tuesday"], data["wednesday"], data["thursday"], data["friday"], data["saturday"], data["sunday"])
  # raise Exception(message.body)
  message.send()