import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import Organization

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../../templates/admin"),
         os.path.join(os.path.dirname(__file__),"../../../templates/layouts")]))

LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('new_organizations.html')

class AdminOrgNewHandler(BaseHandler.BaseHandler):
  def get(self):

    role = self.session.get('role')
    user_session = self.session.get("user")

    if role != "admin":
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return

    if not self.legacy:
      self.redirect("/#/admin/organizations/new")

    form = Organization.NewOrganizationForm()
    template_values = {
      "form": form,
      "user_session": user_session
    }
    language = None
    if "language" in self.request.cookies:
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    language = language.replace('"', '').replace("'", "")
    if language == "fr":

      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_new_organizations.html')
    else:
      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('new_organizations.html')
    self.response.write(LEGACY_TEMPLATE.render(template_values))

  def post(self):
    form = Organization.NewOrganizationForm(self.request.POST)
    if form.validate():
      user = Organization.save(self, form, LEGACY_TEMPLATE)
    else:
      self.response.write(LEGACY_TEMPLATE.render({"form": form}))
