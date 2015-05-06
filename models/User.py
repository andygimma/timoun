# -*- coding: utf-8 -*- 

from google.appengine.ext import ndb
from wtforms import Form, BooleanField, StringField, SelectField, PasswordField, validators
from wtforms.ext.appengine.db import model_form
import hashlib
import datetime
from google.appengine.api import mail

import Audit
import json

ORIGIN_EMAIL = "ibesr@bscht.org"

ROLES = ["admin", "staff","public"]
class User(ndb.Model):
  """Models an User."""
  name = ndb.StringProperty(required=True)
  email = ndb.StringProperty(required=True)
  organization = ndb.StringProperty()
  phone = ndb.StringProperty(indexed=False)
  role = ndb.StringProperty(choices=ROLES, required=True)
  password_digest = ndb.StringProperty()
  email_endpoint = ndb.StringProperty()
  email_sent_at = ndb.DateTimeProperty(auto_now_add=True)
  email_authorized = ndb.BooleanProperty(default=False, required=True)
  created_at = ndb.DateTimeProperty(auto_now_add=True, required=True)
  modified_at = ndb.DateTimeProperty(auto_now_add=True, required=True)


  CSV_FIELDS = [
        'name',
        'email',
        'organization',
        'phone',
        'email',
        'role',
        'email_authorized',
        'created_at'
  ]
  
  def ToCsvLine(self):
    """Returns the site as a list of string values, one per field in
    CSV_FIELDS."""
    csv_row = []
    for field in self.CSV_FIELDS:
      value = getattr(self, field)
      if value is None:
        csv_row.append('')
      else:
        try:
          csv_row.append(unicode(value).encode("utf-8"))
        except:
          logging.critical("Failed to parse: " + value + " " + str(self.key().id()))
    return csv_row



def save(self, form, LEGACY_TEMPLATE):
  users = User.query(User.email == self.request.get("email"))
  if users.count() == 0:
    email_endpoint = create_email_endpoint()
    user = User(name = self.request.get("name"), email = self.request.get("email"), organization = self.request.get("organization"), phone = self.request.get("phone"), role = self.request.get("role"), password_digest = None, email_endpoint = email_endpoint)
    if user.put():
      user_dict = {
        "email": user.email,
        "name": user.name,
        "organization": user.organization,
        "phone": user.phone,
        "role": user.role
      }
      user_json = json.dumps(user_dict)
      user_audit = Audit.save(initiated_by = self.session.get("user"), user_affected = self.request.get("email"), security_clearance = "admin", json_data = user_json, model= "User", action = "Create User")
      confirmation_email(user.email, email_endpoint, user.name)
      self.redirect("/admin/users?message=%s added to Timoun" % user.email)
    else:
      self.response.write(LEGACY_TEMPLATE.render({"form": form, "message": "User not saved, contact administrator"}))
  else:
    self.response.write(LEGACY_TEMPLATE.render({"form": form, "message": "A user with that email already exists"}))

def update(self, TEMPLATE, form, user_session, user_key=None):
    users = User.query(User.email == user_session)
    user = None
    for user in users:
      user = user
    user.name = form.name.data
    user.organization = form.organization.data
    user.phone = form.phone.data
    user.role = form.role.data
    if user.put():
      user_dict = {
        "name": user.name,
        "organization": user.organization,
        "phone": user.phone,
      }
      user_json = json.dumps(user_dict)
      user_audit = Audit.save(initiated_by = self.session.get("user"), user_affected = user.email, security_clearance = user.role, json_data = user_json, model= "User", action = "Update User")
      profile_update_email(user.email)

      if user_key:
        self.redirect("/users/{0}/edit?message={1}".format(user_key, "Profile updated successfully"))
      else:
        self.redirect("/users/profile?message={0}".format("Profile updated successfully"))
    else:
      self.response.write(TEMPLATE.render({"form": form, "message": "Profile unsuccessful. Please contact administrator."}))

def confirm_email(self, form, TEMPLATE, email_endpoint):
  users = User.query(User.email == self.request.get("email"), User.email_endpoint == email_endpoint)
  if users:
    for user in users:
      user.email_authorized = True
      user.email_sent_at = None
      user.email_endpoint = None
      user.password_digest = hash_password(self.request.get("password"))
      user.put()

      self.redirect("/users/login?message={0}".format("Email confirmed. You may log in using your password."))
  else:
    self.response.write(TEMPLATE.render({"form": form, "message": "Unable to confirm email. Please contact administrator."}))

def authenticate(self, TEMPLATE, form):
  email = self.request.get("email")
  password = self.request.get("password")

  users = User.query(User.email == self.request.get("email"), User.password_digest == hash_password(password))
  user = None
  for user in users:
    user = user

  if user:
    self.session['user'] = user.email
    self.session['role'] = user.role
    if user.role == "admin":
      self.redirect("/admin?message={0} logged in successfully".format(user.email))
    else:
      self.redirect("/users/profile?message={0} logged in successfully".format(user.email))
  else:
    self.response.write(TEMPLATE.render({"form": form, "message": "Nom d'utilisateur et de mot de passe ne combinaison existe pas."}))





def create_email_endpoint():
  return hashlib.sha224(str(datetime.datetime.now()) + "1").hexdigest()


def hash_password(password):
  return hashlib.sha224(password).hexdigest()

def profile_update_email(user_email):
  message = mail.EmailMessage(sender=ORIGIN_EMAIL,
                            subject="Actualisation de votre profil / Your account has been updated")

  message.to = "<%s>" % user_email
  message.body = """

  Votre compte Timoun a été mis à jour par quelqu'un connecté à votre compte.
  Your Timoun account has been updated by someone logged into your account.

  Si vous pensez que quelqu'un d'autre utilise votre compte, veuillez contacter directement Timoun.
  If you think someone else updated your account, please contact Timoun directly.

  """.decode("utf-8")

  message.send()

def confirmation_email(user_email, email_endpoint, user_name):
  message = mail.EmailMessage(sender=ORIGIN_EMAIL,
                            subject="Confirmation de votre courrier / Your account requires confirmation")

  message.to = "<%s>" % user_email
  message.body = """
  {0}

  Vous etes invité à utiliser ce site
  You have been invited to use Timoun.

  Veuillez suivre le lien pour créer votre mot de passe et confirmer votre compte.
  Please follow the email below to set your password and confirm your account.

  http://timoun-production.appspot.com/admin/users/{1}

  """.decode("utf-8").format(user_name, email_endpoint)

  message.send()

def send_reset_password_email(self, form, TEMPLATE):
  user = None
  users = User.query(User.email == form.email.data)
  for user in users:
    user = user


  if user:
    email_endpoint = create_email_endpoint()

    user.email_endpoint = email_endpoint
    user.email_sent_at = datetime.datetime.now()
    user.put()

    message = mail.EmailMessage(sender=ORIGIN_EMAIL,
                              subject="Changez votre code secret / Your account requires confirmation")

    message.to = "<%s>" % form.email.data
    message.body = """
    Objet: votre compte nécessite une confirmation
    Someone is trying to reset your password.

    Veuillez le signaler, si ce n’est pas vous
    If that wasn't you, please contact Timoun.

    Veuillez suivre le lien ci-dessous pour créer un autre mot de passe secret.
    Otherwise, Please follow the link below to reset your password

    http://timoun-production.appspot.com/users/set_password/{1}

    """.decode("utf-8").format(form.email.data, email_endpoint)

    message.send()
    self.redirect("/?message={0}".format("Password reset email sent"))

  else:
    self.response.write(TEMPLATE.render({"form": form, "message": "Email does not exist"}))


def reset_password(self, form, TEMPLATE, email_endpoint):
  users = User.query(User.email == form.email.data, User.email_endpoint == email_endpoint)
  if users.count() > 0:
    for user in users:
      user.email_authorized = True
      user.email_sent_at = None
      user.email_endpoint = None
      user.password_digest = hash_password(form.password.data)
      user.put()
      user_dict = {
        "user": "Set password"
      }
      user_json = json.dumps(user_dict)
      user_audit = Audit.save(initiated_by = "Visitor", user_affected = user.email, security_clearance = "visitor", json_data = user_json, model= "User", action = "User Set Password")
      self.redirect("/users/login?message={0}".format("Email confirmed. You may log in using your password."))
  else:
    self.response.write(TEMPLATE.render({"form": form, "message": "Unable to confirm email. Please contact administrator."}))

class UserForm(Form):
  name = StringField('Name', [validators.Length(min=1, max=35)])
  email = StringField('Email Address', [validators.Length(min=1, max=35)])
  organization = StringField('Organization', [validators.Length(min=1, max=35)])
  phone = StringField('Phone', [validators.Length(min=1, max=35)])
  role = SelectField('Role', choices= [(role, role) for role in ROLES])
  #password = StringField('Password', [validators.Length(min=6, max=35)])
  #password_confirmation = StringField('Repeat Password', [validators.Length(min=6, max=35), validators.EqualTo('password', message='Passwords must match')])

class UserConfirmationForm(Form):
  email = StringField('Email Address', [validators.Length(min=1, max=35)])
  password = PasswordField('Password', [validators.Length(min=6, max=35)])
  password_confirmation = PasswordField('Repeat Password', [validators.Length(min=6, max=35), validators.EqualTo('password', message='Passwords must match')])

class UserLoginForm(Form):
  email = StringField('Email Address', [validators.Length(min=1, max=35)])
  password = PasswordField('Password', [validators.Length(min=6, max=35)])

class UserProfileForm(Form):
  name = StringField('Name', [validators.Length(min=1, max=35)])
  organization = StringField('Organization', [validators.Length(min=1, max=35)])
  phone = StringField('Phone', [validators.Length(min=1, max=35)])

class UserResetPasswordForm(Form):
  email = StringField('Email Address', [validators.Length(min=1, max=35)])
  email_confirmation = StringField('Confirm Email', [validators.EqualTo('email', message='Emails must match')])
