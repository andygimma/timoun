import os
import jinja2
import webapp2
from handlers import BaseHandler
from google.appengine.ext import db
from models import Record
import MySQLdb
from helpers import QueryHandler

_INSTANCE_NAME = 'timoun-production:surveydata'

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/admin"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('records.html')

class AdminRecordHandler(BaseHandler.BaseHandler):
  def get(self):
    sql_statement = """
    SELECT `t0`.`id` AS `lev0_id`, `t0`.`name_french` AS `lev0_name_fr`, `t0`.`name_english` AS `lev0_name_en`, `t1`.`id` AS `lev1_id`, `t1`.`name_french` AS `lev1_name_fr`, `t1`.`name_english` AS `lev1_name_en`, `t1`.`name_safe_short` AS `lev1_name_short`, `t1`.`access` AS `lev1_access`, `t2`.`id` AS `lev2_id`, `t2`.`name_french` AS `lev2_name_fr`, `t2`.`name_english` AS `lev2_name_en`, `t2`.`name_safe_short` AS `lev2_name_short`, `t2`.`access` AS `lev2_access`, `t3`.`id` AS `lev3_id`, `t3`.`name_french` AS `lev3_name_fr`, `t3`.`name_english` AS `lev3_name_en`, `t3`.`name_safe_short` AS `lev3_name_short`, `t3`.`access` AS `lev3_access`
    FROM `section` AS `t0`
    LEFT JOIN `attribute` AS `t1` ON `t1`.`section_id` = `t0`.`id`
    LEFT JOIN `attribute` AS `t2` ON `t2`.`parent_id` = `t1`.`id`
    LEFT JOIN `attribute` AS `t3` ON `t3`.`parent_id` = `t2`.`id`
    WHERE `t1`.`parent_id` = 0;
    """

    records = QueryHandler.execute_query(sql_statement)
    missed = []
    html_string = ""
    html_string += format_html(records)

    # raise Exception(missed)
    # raise Exception(records[140])
    self.response.headers['Content-Type'] = 'text/html'
    self.response.write(html_string)
    return
    role = self.session.get('role')
    user_session = self.session.get("user")
    page = self.request.get("page")

    if role != "admin":
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return

    if not self.legacy:
      self.redirect("/#/admin")

    query = Record.Record.query()
    records = None
    if page:
      offset = int(page) * 100
      records = query.fetch(100, offset = offset)
    else:
      records = query.fetch(100)

    if not page:
      page = 0
    else:
      page = int(page)

    records = QueryHandler.execute_query('SELECT 1_nom, id FROM organization LIMIT 100')

    #raise Exception(len(guestlist))
    next_page = page + 1
    last_page = page - 1
    template_values = {
      "message": self.request.get("message"),
      "user_session": user_session,
      "records": records,
      "records_length": len(records),
      "next_page": next_page,
      "last_page": last_page
    }

    language = None
    if "language" in self.request.cookies:
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    language = language.replace('"', '').replace("'", "")
    if language == "fr":

      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_records.html')
    else:
      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('records.html')
    self.response.write(LEGACY_TEMPLATE.render(template_values))

def humanize_text(string):
    string = string.replace("_", " ")
    string = string.title()
    return string

def select_info(record):
  if record[15]:
    return record[15]
  if record[10]:
    return record[10]    
  if record[5]:
    return record[5]
  if record[2]:
    return record[2]        

def format_html(records):
  last_header = ""
  html_string = ""
  added_list = []
  all_layers_array = []
  record_id = records[0][0]
  form_dict = get_record_info(record_id)
  level_ids = []
  errors_count = 0

  for record in records:
    # raise Exception(record)
    lev_0 = record[2]
    lev_1 = record[5]
    lev_2 = record[10]
    lev_3 = record[15]
    if lev_0 != last_header:
      html_string += "<h3>{}</h3>".format(lev_0)
      last_header = lev_0
      added_list.append(lev_0)

    all_layers_array = get_layers_array(lev_0, lev_1, lev_2, lev_3)
    for layer in all_layers_array:
      if layer not in added_list:
        # raise Exception(form_dict[get_level_id(record, all_layers_array.index(layer))])
        html_string += ("<p>{0}| {1}".format(all_layers_array.index(layer), layer))  
        if get_level_id(record, all_layers_array.index(layer)) in form_dict:
          level_ids.append(get_level_id(record, all_layers_array.index(layer)))
          try:
            html_string += ": <u><strong>{0}</u></strong></p>".format(form_dict[get_level_id(record, all_layers_array.index(layer))])
          except:
            info = form_dict[get_level_id(record, all_layers_array.index(layer))]
            html_string += ":{0}</p>".format(info.encode("latin-1"))

          
        else:
          html_string += "</p>"
          # raise Exception(1)
        added_list.append(layer)
  # raise Exception(errors_count)
  return html_string   

def get_outer_layer(record):
  records_array = []
  if record[15]:
    records_array.append(record[15])
    # if record[10] not in records_array
    return "<p>LEV3| {}</p>".format(record[15])
  if record[10]:
    records_array.append(record[10])
    return "<p>LEV2| {}</p>".format(record[10])    
  if record[5]:
    records_array.append(record[5])
    return "<p>LEV1|{}</p>".format(record[5])


def get_layers_array(lev_0, lev_1, lev_2, lev_3):
  layers_array = []
  if lev_0 != None:
    layers_array.append(lev_0)
  if lev_1 != None:
    layers_array.append(lev_1)
  if lev_2 != None:
    layers_array.append(lev_2)
  if lev_3 != None:
    layers_array.append(lev_3)
  return layers_array


def get_record_info(record_id):
  sql_statement = """SELECT `data`.`record_id`, `data`.`attribute_id`, `data`.`program_id`, `data`.`content_integer`, `data`.`content_text`, `data`.`content_decimal`, `data`.`content_date`, `attribute`.`name_safe_short`, `attribute`.`access`, `attribute`.`is_enum`, `attribute`.`format`
  FROM `data`
  LEFT JOIN `attribute` ON `data`.`attribute_id` = `attribute`.`id`
  WHERE `data`.`record_id` = {0};
  """.format(record_id)
  items = QueryHandler.execute_query(sql_statement)

  info_dict = {}

  for item in items:
    info_dict[item[1]] = get_correct_data(item)
    
  return info_dict

def get_correct_data(item):
  if item[3]:
    return item[3]
  if item[4]:
    return item[4]
  if item[5]:
    return item[5]
  if item[6]:
    return item[6]

def get_level_id(record, index):
  if index == 3:
    return record[13]
  if index == 2:
    return record[8]
  if index == 1:
    return record[3]