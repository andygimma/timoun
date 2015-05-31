# -*- coding: utf-8 -*- 
import os
import json
import MySQLdb
from models import SearchRecord, Audit
import unicodedata
import json

_INSTANCE_NAME = 'timoun-production:timoun427'
words = {
"Š": "S",
"š": "s",
"Ð": "Dj",
"Ž": "Z",
"ž": "z",
"À": "A",
"Á": "A",
"Â": "A",
"Ã": "A",
"Ä": "A",
"Å": "A",
"Æ": "A",
"Ç": "C",
"È": "E",
"É": "E",
"Ê": "E",
"Ë": "E",
"Ì": "I",
"Í": "I",
"Î": "I",
"Ï": "I",
"Ñ": "N",
"Ò": "O",
"Ó": "O",
"Ô": "O",
"Õ": "O",
"Ö": "O",
"Ø": "O",
"Ù": "U",
"Ú": "U",
"Û": "U",
"Ü": "U",
"Ý": "Y",
"Þ": "B",
"ß": "Ss",
"à": "a",
"á": "a",
"â": "a",
"ã": "a",
"ä": "a",
"å": "a",
"æ": "a",
"ç": "c",
"è": "e",
"é": "e",
"ê": "e",
"ë": "e",
"ì": "i",
"í": "i",
"î": "i",
"ï": "i",
"ð": "o",
"ñ": "n",
"ò": "o",
"ó": "o",
"ô": "o",
"õ": "o",
"ö": "o",
"ø": "o",
"ù": "u",
"ú": "u",
"û": "u",
"ý": "y",
"ý": "y",
"þ": "b",
"ÿ": "y",
"ƒ": "f",
"a": "a",
"î": "i",
"â": "a",
"A": "A",
"Î": "I",
"Â": "A",
"?": "",
"\'": "",
"\"": "",
"(": "",
")": "",
"`": "",
"~": "",
"!": "",
"@": "",
"#": "",
"$": "",
"%": "",
"^": "",
"&": "",
"*": "",
"(": "",
")": "",
"+": "",
"=": "",
"{": "",
"[": "",
"}": "",
"]": "",
"|": "",
"\\": "",
"/": "",
";": "",
":": "",
"<": "",
">": "",
".": "",
",": "_"
}


def execute_query(query_string, insert=False):
    if (os.getenv('SERVER_SOFTWARE') and
      os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
      db = MySQLdb.connect(unix_socket='/cloudsql/' + _INSTANCE_NAME, db='timoun_4_30', user='root', passwd="11oinn")
    else:
      db = MySQLdb.connect(host='127.0.0.1', port=3306, db='timoun_4_30', user='root', passwd="11oinn")

    cursor = db.cursor()
    cursor.execute(query_string.decode("utf-8"))

    if insert:
      db.commit()
      db.close()
      return True
    else:
      records = [];
      for row in cursor.fetchall():
        records.append(row)
      
      return encoded_records(records)

def get_services_select():
	services_select_sql = "SELECT DISTINCT `service`.`program_id`, `program`.`name_french` AS `prog_name_fr`, `program`.`name_english` AS `prog_name_en`, `service`.`name_french` AS `service_name_fr`, `service`.`name_english` AS `service_name_en` FROM `service` LEFT JOIN `program` ON `service`.`program_id` = `program`.`id` ORDER BY `program_id` ASC, `service_name_fr` ASC"
	return execute_query(services_select_sql)

def get_index_by_page(page = 0):
	offset = page * 100
	index_sql = "SELECT 1_nom FROM organization LIMIT 100 OFFSET {0}".format(offset)
	return execute_query(index_sql)


def get_all_organizations():
	orgs_sql = "SELECT * FROM organization"
	return execute_query(orgs_sql)

def get_organization_by_id(organization_id):
	org_sql = "SELECT * FROM organization WHERE id = {0}".format(organization_id)
	return execute_query(org_sql)
def form_query_total(self, page=None):
  keywords = self.request.get("keywords").encode("utf-8")
  service = self.request.get("service").encode("latin-1")
  department = self.request.get("department").encode("utf-8")
  age_start = self.request.get("age_start").encode("utf-8")
  age_end = self.request.get("age_end").encode("utf-8")
  gender = self.request.get("gender").encode("utf-8")
  keywords = self.request.get("keywords").encode("utf-8")
  record_search(keywords, service, department, age_start, age_end, gender)
  # raise Exception(keywords)

  service_query = ""
  department_query = ""
  gender_query = ""
  age_query = ""
  page_query = ""
  full_text_query = ""
  if page:
    page_int = int(page)
    offset = page_int * 100
    page_query = "OFFSET {0}".format(offset)
  if age_start and age_end:
    age_start, age_end = order_age(age_start, age_end)
    age_query = sql_age_string(age_start, age_end)

  if service:
    service_query = "AND `service`.`name_french` = '{0}'".format(service)

  if department:
    department_query = "AND `commune` = \"{0}\"".format(department.encode("utf-8"))

  if gender:
    if gender == "male":
      gender_query = "AND `filles` = 1"
    if gender == "female":
      gender_query = "AND `garcons` = 1"
    if gender_query == "either":
      gender_query = "AND (`garcons` = 1 OR `filles`=1)"

  if keywords:
    for word in words:
      keywords = keywords.replace(word, words[word])
      # raise Exception(keywords)
    full_text_query = "AND MATCH(service_details) AGAINST(\"{0}\")".format(keywords)

  sql_statement = """SELECT org_id
        FROM `service`
        LEFT JOIN `organization`
        ON `service`.`org_id` = `organization`.`id`
      WHERE 1=1
      {0}
      {1}
      {2}
      {3}
      {4}
      GROUP BY `org_id`
  """.format(gender_query, service_query, department_query, age_query, full_text_query)
  total =  execute_query(sql_statement)
  return len(total)


def form_query_builder(self, page=None, limit=25):
  keywords = self.request.get("keywords").encode("utf-8")
  service = self.request.get("service").encode("latin-1")
  department = self.request.get("department").encode("utf-8")
  age_start = self.request.get("age_start").encode("utf-8")
  age_end = self.request.get("age_end").encode("utf-8")
  gender = self.request.get("gender").encode("utf-8")
  keywords = self.request.get("keywords").encode("utf-8")
  record_search(keywords, service, department, age_start, age_end, gender)

  service_query = ""
  department_query = ""
  gender_query = ""
  age_query = ""
  page_query = ""
  full_text_query = ""
  if page:
    page_int = int(page)
    offset = page_int * 100
    page_query = "OFFSET {0}".format(offset)
  if age_start and age_end:
    age_start, age_end = order_age(age_start, age_end)
    age_query = sql_age_string(age_start, age_end)

  if service:
    service_query = "AND `service`.`name_french` = '{0}'".format(service)

  if department:
    department_query = "AND `commune` = \"{0}\"".format(department.encode("utf-8"))

  if gender:
    if gender == "male":
      gender_query = "AND `filles` = 1"
    if gender == "female":
      gender_query = "AND `garcons` = 1"
    if gender_query == "either":
      gender_query = "AND (`garcons` = 1 OR `filles`=1)"

  if keywords:
    # keywords = keywords.decode("latin-1")
    for word in words:
      keywords = keywords.replace(word, words[word])

    full_text_query = "AND MATCH(service_details) AGAINST(\"{0}\")".format(keywords)


  sql_statement = """SELECT `service`.`id`, 
        `service`.`name_french`, 
        `service`.`org_id`, 
        `service`.`program_id`, 
        `service`.`notes`, 
        `organization`.`1_nom` AS `org_nom`, 
        `organization`.`departement`, 
        `organization`.`commune`, 
        `organization`.`section_communale`,
        `organization`.`adresse`, 
        `organization`.`latitude`, 
        `organization`.`longitude`, 
        `organization`.`boite_postale`, 
        `organization`.`telephone`, 
        `organization`.`personne_contact`, 
        `organization`.`email`, 
        `organization`.`site_web`
        FROM `service`
        LEFT JOIN `organization`
        ON `service`.`org_id` = `organization`.`id`
      WHERE 1=1
      {0}
      {1}
      {2}
      {3}
      {4}
      GROUP BY `org_id`
      LIMIT {5}
      {6}
  """.format(gender_query, service_query, department_query, age_query, full_text_query, limit, page_query)
  # raise Exception(department_query)
  # raise Exception(sql_statement)
  return execute_query(sql_statement)

def order_age(age_start, age_end):
  if int(age_start) > int(age_end):
    temp = age_start
    age_start = age_end
    age_end = temp
  return age_start, age_end

def sql_age_string(age_start, age_end):
  sql_string = "AND "
  for index in range(int(age_start), int(age_end) + 1):
    sql_string += "`age_{0}`+".format(index)

  sql_string = sql_string[:-1] + ">0" # removes the last + sign from the string
  return sql_string

def form_builder(sql_statement):
  execute_query()

def encoded_records(records):
  return [[word.decode("latin-1") if isinstance(word, str) or isinstance(word, unicode) else word for word in sets] for sets in records]

def record_search(keywords, service, department, age_start, age_end, gender):
  ip = os.environ["REMOTE_ADDR"]
  s = SearchRecord.SearchRecord(ip_address = ip, keywords = keywords, service = service.decode("latin-1"), department = department, age_start = age_start, age_end = age_end, gender = gender)
  s.put()

def add_services(records):
  for record in records:
    sql_statement = """SELECT GROUP_CONCAT(`service`.`name_french`) AS `all_services_fr`, 
      GROUP_CONCAT(`service`.`name_english`) AS `all_services_en`
      FROM `service`
      WHERE `service`.`org_id` = {0};
    """.format(record[0])

    services = execute_query(sql_statement)
    record.append(services)
  return records

  # raise Exception(department_query)
  # raise Exception(sql_statement)
  return execute_query(sql_statement)

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def create_audit(self, data_type, name, data, action):
  for word in words:
      name = name.replace(word, words[word])

  for item in data:
    for word in words:
      data[item] = data[item].replace(word, words[word])
  a = Audit.save(initiated_by = self.session.get("user"), user_affected = name, security_clearance = self.session.get("role"), json_data = json.dumps(data), model= data_type, action = action)  
  return