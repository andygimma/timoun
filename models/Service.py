from google.appengine.ext import ndb
from wtforms import Form, BooleanField, StringField, SelectField, PasswordField, validators
from wtforms.ext.appengine.db import model_form
import Audit
import json

class Service(ndb.Model):
  name = ndb.StringProperty(required=True)


def save(self, form, LEGACY_TEMPLATE):
  services = Service.query(Service.name == self.request.get("name"))
  if services.count() == 0:
    service = Service(name=self.request.get("name"))
    if service.put():
      service_dict = {
        "name": service.name,
      }
      service_json = json.dumps(service_dict)
      service_audit = Audit.save(initiated_by = self.session.get("user"), organization_affected = self.request.get("name"), security_clearance = "admin", json_data = service_json, model= "Service", action = "Create Service")
      self.redirect("/admin/programs?message=Service {0} added".format(self.request.get("name")))
    else:
      self.response.write(LEGACY_TEMPLATE.render({"form": form, "message": "Service not saved, contact administrator"}))
  else:
    self.response.write(LEGACY_TEMPLATE.render({"form": form, "message": "A service with that name already exists"}))


def update(self, TEMPLATE, form, service_name, service_key=None):
    services = Service.query(Service.name == service_name)
    service = None
    for service in services:
      service = service

    service.name = form.name.data
    if service.put():
      service_dict = {
        "name": service.name,
      }
      service_json = json.dumps(service_dict)
      service_audit = Audit.save(initiated_by = self.session.get("user"), organization_affected = self.request.get("name"), security_clearance = "admin", json_data = service_json, model= "Service", action = "Edit Service")
      if service:
        self.redirect("/services/{0}/edit?message={1}".format(service_key, "Service updated successfully"))
      else:
        self.redirect("/admin/services?message={0}".format("Service updated successfully"))
    else:
      self.response.write(TEMPLATE.render({"form": form, "message": "Service update unsuccessful. Please contact administrator."}))


class NewServiceForm(Form):
  name = StringField('Name', [validators.Length(min=1, max=35)])
