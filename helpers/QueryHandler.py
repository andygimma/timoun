import os
import json
import MySQLdb
from models import SearchRecord

_INSTANCE_NAME = 'timoun-production:surveydata'

def execute_query(query_string):
    if (os.getenv('SERVER_SOFTWARE') and
      os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
      db = MySQLdb.connect(unix_socket='/cloudsql/' + _INSTANCE_NAME, db='survey_data_4_15', user='andy2', passwd="11oinn")
    else:
      db = MySQLdb.connect(host='127.0.0.1', port=3306, db='timoun_4_15', user='root', passwd="11oinn")

    cursor = db.cursor()
    cursor.execute(query_string)

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

def form_query_builder(self, page=None, limit=25):
  keywords = self.request.get("keywords")
  service = self.request.get("service")
  department = self.request.get("department")
  age_start = self.request.get("age_start")
  age_end = self.request.get("age_end")
  gender = self.request.get("gender")
  record_search(keywords, service, department, age_start, age_end, gender)



  service_query = ""
  department_query = ""
  gender_query = ""
  age_query = ""
  page_query = ""
  if page:
    page_int = int(page)
    offset = page_int * 100
    page_query = "OFFSET {0}".format(offset)
  if age_start and age_end:
    age_start, age_end = order_age(age_start, age_end)
    age_query = sql_age_string(age_start, age_end)
  # raise Exception(age_query)
  if service:
    service_query = "AND `name_french` = '{0}'".format(service.encode("utf-8"))

  if department:
    department_query = "AND `commune` = '{0}'".format(department.encode("utf-8"))

  if gender:
    if gender == "male":
      gender_query = "AND `filles` = 1"
    if gender == "female":
      gender_query = "AND `garcons` = 1"
    if gender_query == "either":
      gender_query = "AND (`garcons` = 1 OR `filles`=1)"

  sql_statement = """SELECT  `org_nom`, `name_french` AS `service_name_fr`, `name_english`  AS `service_name_en`, `org_id`, `org_email`, `org_phone`, `program_id`, `latitude`, `longitude`, COUNT(DISTINCT(`name_french`)) AS `service_count`
                      FROM `service`
                      WHERE 1 = 1
                      {0}
                      {1}
                      {2}
                      {3}
                      GROUP BY `org_id`
                      LIMIT {4}
                      {5}
  """.format(gender_query, service_query, department_query, age_query, limit, page_query).decode("utf-8")
  # raise Exception(sql_statement)
  # raise Exception(len(execute_query(sql_statement)))

  return execute_query(sql_statement)

def order_age(age_start, age_end):
  if age_start > age_end:
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
  s = SearchRecord.SearchRecord(ip_address = ip, keywords = keywords, service = service, department = department, age_start = age_start, age_end = age_end, gender = gender)
  s.put()

