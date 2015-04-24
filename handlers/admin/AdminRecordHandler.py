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
    
    role = self.session.get('role')
    user_session = self.session.get("user")
    page = self.request.get("page")
    offset_string = ""
    if page:
      offset = int(page) * 100
      offset_string = "OFFSET {0}".format(offset)

    if role != "admin":
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return

    if not self.legacy:
      self.redirect("/#/admin")

    query = Record.Record.query()
    if not page:
      page = 0
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
    records = None
    if search(self):
      records = QueryHandler.form_query_builder(self, page, 100)
    else:
      records = QueryHandler.execute_query("SELECT 1_nom, id FROM organization LIMIT 100 {0}".format(offset_string))

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

def search(self):
  keywords = self.request.get("keywords")
  service = self.request.get("service")
  department = self.request.get("department")
  age_start = self.request.get("age_start")
  age_end = self.request.get("age_end")
  gender = self.request.get("gender")

  if keywords or service or department or age_start or age_end or gender:
    return True
  else:
    return False
