from google.appengine.ext import ndb
from wtforms import Form, BooleanField, StringField, SelectField, PasswordField, validators
from wtforms.ext.appengine.db import model_form
import hashlib
import datetime
from google.appengine.api import mail
import env
import Audit
import json

class Organization(ndb.Model):
  name = ndb.StringProperty(required=True)

def save(self, form, LEGACY_TEMPLATE):
  organizations = Organization.query(Organization.name == self.request.get("name"))
  if organizations.count() == 0:
    organization = Organization(name=self.request.get("name"))
    if organization.put():
      org_dict = {
        "name": organization.name,
      }
      org_json = json.dumps(org_dict)
      org_audit = Audit.save(initiated_by = self.session.get("user"), organization_affected = self.request.get("name"), security_clearance = "admin", json_data = org_json, model= "Organization", action = "Create Organization")
      self.redirect("/admin/organizations?message=Organization {0} added".format(self.request.get("name")))
    else:
      self.response.write(LEGACY_TEMPLATE.render({"form": form, "message": "Organization not saved, contact administrator"}))
  else:
    self.response.write(LEGACY_TEMPLATE.render({"form": form, "message": "An organization with that name already exists"}))

def update(self, TEMPLATE, form, org_name, org_key=None):
    organizations = Organization.query(Organization.name == org_name)
    org = None
    for org in organizations:
      org = org

    org.name = form.name.data
    if org.put():
      org_dict = {
        "name": org.name,
      }
      org_json = json.dumps(org_dict)
      org_audit = Audit.save(initiated_by = self.session.get("user"), organization_affected = self.request.get("name"), security_clearance = "admin", json_data = org_json, model= "Organization", action = "Edit Organization")
      if org_key:
        self.redirect("/organizations/{0}/edit?message={1}".format(org_key, "Organization updated successfully"))
      else:
        self.redirect("/admin/organizations?message={0}".format("Profile updated successfully"))
    else:
      self.response.write(TEMPLATE.render({"form": form, "message": "Organization update unsuccessful. Please contact administrator."}))

class NewOrganizationForm(Form):
  name = StringField('Name', [validators.Length(min=1, max=35)])
