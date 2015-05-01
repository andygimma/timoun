# -*- coding: utf-8 -*- 

import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import Record
from helpers import QueryHandler
from config import enums

NOT_IN_ORG_SCOPE = ["Program", "Service", "Nutrition", "Home-Based Care", "Child Protection", "Health", "Psychosocial Support", "Education", "Mental Health Services"]

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/admin"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('new_record.html')

class NewRecordHandler(BaseHandler.BaseHandler):
  def get(self):

    sql_statement= """
      SELECT `t0`.`id` AS `lev0_id`, `t0`.`name_french` AS `lev0_name_fr`, `t0`.`name_english` AS `lev0_name_en`, `t1`.`id` AS `lev1_id`, `t1`.`name_french` AS `lev1_name_fr`, `t1`.`name_english` AS `lev1_name_en`, `t1`.`name_safe_short` AS `lev1_name_short`, `t1`.`access` AS `lev1_access`, `t1`.`html_form_type` AS `lev1_type`, `t2`.`id` AS `lev2_id`, `t2`.`name_french` AS `lev2_name_fr`, `t2`.`name_english` AS `lev2_name_en`, `t2`.`name_safe_short` AS `lev2_name_short`, `t2`.`access` AS `lev2_access`, `t2`.`html_form_type` AS `lev2_type`, `t3`.`id` AS `lev3_id`, `t3`.`name_french` AS `lev3_name_fr`, `t3`.`name_english` AS `lev3_name_en`, `t3`.`name_safe_short` AS `lev3_name_short`, `t3`.`access` AS `lev3_access`, `t3`.`html_form_type` AS `lev3_type`
      FROM `section` AS `t0`
      LEFT JOIN `attribute` AS `t1` ON `t1`.`section_id` = `t0`.`id`
      LEFT JOIN `attribute` AS `t2` ON `t2`.`parent_id` = `t1`.`id`
      LEFT JOIN `attribute` AS `t3` ON `t3`.`parent_id` = `t2`.`id`
      WHERE `t1`.`parent_id` = 0
      AND `t1`.`is_depreciated` = 0;

    """

    records = QueryHandler.execute_query(sql_statement)
    # raise Exception(records[23][8])
    html_string = form_builder(records)
    role = self.session.get('role')
    user_session = self.session.get("user")

    if role != "admin":
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return


    form = Record.RecordForm()
    template_values = {
      "form": form,
      "user_session": user_session,
      "html_string": html_string
    }
    language = None
    if "language" in self.request.cookies:
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    language = language.replace('"', '').replace("'", "")
    if language == "fr":

      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_new_record.html')
    else:
      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('new_record.html')
    self.response.write(LEGACY_TEMPLATE.render(template_values))

  def post(self):
    form = Record.RecordForm(self.request.POST)
    if form.validate():
      user = Record.save(self, form, LEGACY_TEMPLATE)
    else:
      self.response.write(LEGACY_TEMPLATE.render({"form": form}))

def form_builder(records):
  html_string = ""
  last_header = ""
  for record in records:
    html_string += "<br>"
    if record[2] in NOT_IN_ORG_SCOPE:
      pass
    else:
      if record[2] != last_header:
        html_string += "<h2>{0}</h2>".format(record[2])
        last_header = record[2]
      name = get_name(record)
      name = record[12]
      if record[8] == "text":
        html_string += "{0}: <input id='first' name='{0}'' type='text' />\n".format(name)
      if record[8] == "dropdown":
        html_string += "{0}: <select><option>Select</option>\n".format(name)

        form_enums = enums.form_enums
        count = 0
        if record[12] in form_enums:
          this_enum = form_enums[record[12]]
          for item in this_enum:
            # encoded_item = item.encode("latin-1").decode("utf-8")
            html_string += "<option>{0}</option>".format(item.encode('ascii', 'ignore'))

        html_string += "</select>\n"
      if record[8] == "textarea":
        html_string += "{0}: <textarea name='{0}'' cols=40 rows=6></textarea>\n".format(name)

  return html_string

def get_name(record):
  if record[17]:
    return record[17]
  if record[11]:
    return record[11]
  if record[5]:
    return record[5]