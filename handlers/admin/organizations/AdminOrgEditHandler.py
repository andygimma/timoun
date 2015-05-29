import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import Organization
from helpers import QueryHandler, OrganizationHelper
import json

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../../templates/admin"),
         os.path.join(os.path.dirname(__file__),"../../../templates/layouts")]))

TEMPLATE = JINJA_ENVIRONMENT.get_template('edit_organization.html')

class AdminOrgEditHandler(BaseHandler.BaseHandler):
  def get(self, org_id):
    role = self.session.get('role')
    user_session = self.session.get("user")

    if role != "admin":
      self.redirect("/organizations/login?message={0}".format("You are not authorized to view this page"))
      return

    if not self.legacy:
      self.redirect("/#/organizations/{0}/edit".format(org_id))

    sql_statement = """
          SELECT * FROM organization WHERE id='{0}' LIMIT 1
        """.format(org_id)


    org = QueryHandler.execute_query(sql_statement)
    if len(org) == 0:
      self.redirect("/admin?message=That organization does not exist")
      return
    data = OrganizationHelper.get_hash(org[0])
    template_values = {
      "role": self.session.get("role"),
      "user_session": user_session,
      "message": self.request.get("message"),
      "org": org[0],
      "data": data
    }
    # g = "show columns from organization;"
    # r = QueryHandler.execute_query(g)
    # attrs = []
    # # raise Exception(r)
    # for item in r:
    #   attrs.append(item[0])
    # raise Exception(attrs)

    language = None
    if "language" in self.request.cookies:
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    language = language.replace('"', '').replace("'", "")
    if language == "fr":
      # raise Exception(2)
      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_edit_organization.html')
    else:
      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('edit_organization.html')
    self.response.write(LEGACY_TEMPLATE.render(template_values))

  def post(self, org_key):
    role = self.session.get('role')
    user_session = self.session.get("user")

    if role != "admin":
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return

    sql_statement = """
      SELECT id FROM organization WHERE id="{0}"
      """.format(org_key)
    organization = QueryHandler.execute_query(sql_statement)
    if len(organization) > 0:
      OrganizationHelper.update_record(self, org_key)
      self.redirect("/records/" + org_key + "/edit?message=Update complete")
    else:
      self.redirect("/admin?message=Program does not exist")
