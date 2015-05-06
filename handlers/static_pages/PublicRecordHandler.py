import os
import jinja2
import webapp2
from handlers import BaseHandler
from google.appengine.ext import db
from models import Record
from helpers import QueryHandler

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/static_pages"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('view_public_records.html')

class PublicRecordHandler(BaseHandler.BaseHandler):
  def get(self, record_id):

    role = self.session.get('role')  
    user_session = self.session.get("user")


    sql_statement = """
      SELECT * FROM organization WHERE id='{0}' LIMIT 1
    """.format(record_id)


    record = QueryHandler.execute_query(sql_statement)
    sql_services = "SELECT name_french, id  FROM service WHERE org_id = {0};".format(record_id)
    services = QueryHandler.execute_query(sql_services)


    sql_programs = """SELECT DISTINCT(`program_id`), `program`.`name_french`, `program`.`name_english`
      FROM `service`
      LEFT JOIN `program`
      ON `service`.`program_id` = `program`.`id`
      WHERE `service`.`org_id` = {0};
    """.format(record_id)
    programs = QueryHandler.execute_query(sql_programs)

    template_values = {
      "message": self.request.get("message"),
      "user_session": user_session,
      "record": record[0],
      "services": services,
      "programs": programs
    }
    language = None
    if "language" in self.request.cookies:
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    language = language.replace('"', '').replace("'", "")
    if language == "fr":

      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_view_public_records.html')
    else:
      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('view_public_records.html')
    self.response.write(LEGACY_TEMPLATE.render(template_values))


# def format_html(records, record_id):
#   last_header = ""
#   html_string = ""
#   added_list = []
#   all_layers_array = []
#   form_dict = get_record_info(record_id)
#   level_ids = []
#   errors_count = 0

#   for record in records:

#     lev_0 = record[2]
#     lev_1 = record[5]
#     lev_2 = record[10]
#     lev_3 = record[15]
#     # raise Exception(record[0])
#       # raise Exception(show_highest_lev_id(record))
#     highest_lev_id = show_highest_lev_id(record)
#     # raise Exception(record)
#     # raise Exception(lev_id)

#     if lev_0 != last_header:
#       html_string += "<h3>{0}</h3>".format(lev_0)
#       last_header = lev_0
#       added_list.append(lev_0)

#     all_layers_array = get_layers_array(lev_0, lev_1, lev_2, lev_3)
#     for layer in all_layers_array:
#       if layer not in added_list:
#         html_string += ("<p>{0}".format(layer))  
#         if get_level_id(record, all_layers_array.index(layer)) in form_dict:
#           level_ids.append(get_level_id(record, all_layers_array.index(layer)))
#           try:
#             html_string +=": <u><strong>{0}</u></strong></p>".format(form_dict[get_level_id(record, all_layers_array.index(layer))])
#           except:
#             info = form_dict[get_level_id(record, all_layers_array.index(layer))]
#             html_string += ":{0}</p>".format(info.encode("latin-1"))

          
#         else:
#           html_string += "</p>"
#         added_list.append(layer)
#   return html_string   


# def get_record_info(record_id):
#   sql_statement = """SELECT `data`.`record_id`, `data`.`attribute_id`, `data`.`program_id`, `data`.`content_integer`, `data`.`content_text`, `data`.`content_decimal`, `data`.`content_date`, `attribute`.`name_safe_short`, `attribute`.`access`, `attribute`.`is_enum`, `attribute`.`format`
#   FROM `data`
#   LEFT JOIN `attribute` ON `data`.`attribute_id` = `attribute`.`id`
#   WHERE `data`.`record_id` = {0};
#   """.format(record_id)
#   items = QueryHandler.execute_query(sql_statement)

#   info_dict = {}

#   for item in items:
#     info_dict[item[1]] = get_correct_data(item)
    
#   return info_dict

# def get_correct_data(item):
#   if item[3]:
#     return item[3]
#   if item[4]:
#     return item[4]
#   if item[5]:
#     return item[5]
#   if item[6]:
#     return item[6]


# def get_layers_array(lev_0, lev_1, lev_2, lev_3):
#   layers_array = []
#   if lev_0 != None:
#     layers_array.append(lev_0)
#   if lev_1 != None:
#     layers_array.append(lev_1)
#   if lev_2 != None:
#     layers_array.append(lev_2)
#   if lev_3 != None:
#     layers_array.append(lev_3)
#   return layers_array


# def get_level_id(record, index):
#   if index == 3:
#     return record[13]
#   if index == 2:
#     return record[8]
#   if index == 1:
#     return record[3]


# def show_highest_lev_id(record):
#   if record[13]:
#     return record[13]
#   if record[8]:
#     return record[8]
#   if record[3]:
#     return record[3]