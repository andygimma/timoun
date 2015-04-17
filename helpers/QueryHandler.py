import os
import MySQLdb

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

    return records

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


def query_builder(table, attribute, select_statement, distinct_boolean, _as, _from, left_join, on, where_clause, order_by):
	# we have to be careful with this, since it's open source.
    # We'll have to make sure to sanitize anything we send in.

	sql_statement = "SELECT {0} FROM {1} WHERE {2} LIMIT {3} OFFSET {4}".format(select_statement, table, where_clause, limit, offset)
	sql_statement = "SELECT {0} ({1}.{2}) {3} {4} {5} {6} {7} {7} ".format(distinct_boolean, table, attribute, _as, _from, left_join, on, where_clause, order_by)

    # if service in service_options:
    # 	service_query = "service.name = {0}".format(service)
    # if age_end in age_ranges:
    # 	age_end_query = "service.ang = {0}".format(age_end)
    # if gender in genders:
    # 	genders_query = "service.gender = {0}".format(gender)

def search_page():
  sql_statement = """
        SELECT `name_french` AS `service_name_fr`, `name_english`  AS `service_name_en`, `org_id`, `org_nom`, `org_email`, `org_phone`, `program_id`, `latitude`, `longitude`, `age_2`+`age_3`+`age_4`+`age_5`+`age_6`+`age_7`+`age_8`+`age_9`+`age_10`+`age_11`+`age_12`+`age_13`+`age_14`+`age_15`+`age_16`+`age_17` AS `age_matches`
        FROM `service`
        WHERE `program_id` = {0}
        AND `name_french` = '{1}'
        AND `age_2`+`age_3`+`age_4`+`age_5`+`age_6`+`age_7`+`age_8`+`age_9`+`age_10`+`age_11`+`age_12`+`age_13`+`age_14`+`age_15`+`age_16`+`age_17`>0 
        AND {3}
        AND `commune` = '{4}'
        AND `departement` = '{4}'
        ;
  """.encode("utf-8")