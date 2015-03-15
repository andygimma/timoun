import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import Organization

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../../templates/admin"),
         os.path.join(os.path.dirname(__file__),"../../../templates/layouts")]))

TEMPLATE = JINJA_ENVIRONMENT.get_template('edit_organization.html')

class AdminOrgEditHandler(BaseHandler.BaseHandler):
  def get(self, org_key):
    role = self.session.get('role')
    user_session = self.session.get("user")

    if role != "admin":
      self.redirect("/organizations/login?message={0}".format("You are not authorized to view this page"))
      return

    if not self.legacy:
      self.redirect("/#/organizations/{0}/edit".format(org_key))

    organization = Organization.Organization.get_by_id(int(org_key))
    if not organization:
      self.response.write(TEMPLATE.render({"form": form, "message": "Unable to find organization. Please contact administrator."}))

    form = Organization.NewOrganizationForm()
    form.name.data = organization.name

    template_values = {
      "role": self.session.get("role"),
      "user_session": user_session,
      "message": self.request.get("message"),
      "form": form,
      "org_key": org_key,
      "org_name": organization.name
    }
    language = None
    if "language" in self.request.cookies:
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    language = language.replace('"', '').replace("'", "")
    if language == "fr":

      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_edit_organization.html')
    else:
      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('edit_organization.html')
    self.response.write(TEMPLATE.render(template_values))

  def post(self, org_key):
    role = self.session.get('role')
    user_session = self.session.get("user")

    if role != "admin":
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return

    organization = Organization.Organization.get_by_id(int(org_key))
    if not organization:
      self.response.write(TEMPLATE.render({"form": form, "message": "Unable to find organization. Please contact administrator."}))

    form = Organization.NewOrganizationForm(self.request.POST)
    if form.validate():
      Organization.update(self, TEMPLATE, form, organization.name, org_key)
    else:
      self.response.write(TEMPLATE.render({"form": form}))
