# -*- coding: utf-8 -*- 
import os
import json
import MySQLdb
from models import SearchRecord
import unicodedata
from helpers import QueryHandler
from models import Audit

ATTRIBUTES = ["org_id", "program_id", "name_french", "name_english", "age_0", "age_1","age_2","age_3","age_4","age_5","age_6","age_7","age_8","age_9","age_10","age_11","age_12","age_13","age_14","age_15","age_16","age_17","age_18", "garcons", "filles", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche", "notes"]
REQUIRED_ATTRIBUTES = ["org_id", "program_id", "name_french"]

def find_or_create_program(data):
	sql_statement = """
			SELECT id FROM org_prog WHERE id="{0}"
			""".format(data['program_id'])
	program = QueryHandler.execute_query(sql_statement)
	if len(program) == 0:
		sql_statement = """
		INSERT INTO `org_prog` SET
		`id` = NULL,
		`org_id` = "{0}",
		`program_id` = "{1}"
		""".format(data['org_id'], data['program_id'])

def check_for_service_duplicate(data):
	words = QueryHandler.words
	name_french = data['name_french']
	if name_french:
	    for word in words:
	    	name_french = name_french.replace(word, words[word])
	sql_statement = """
		SELECT name_french FROM service WHERE name_french="{0}" AND org_id="{1}"
		""".format(name_french, data['org_id'])
	service = QueryHandler.execute_query(sql_statement)
	if len(service) > 0:
		raise Exception("Service already exists")

def validate_attributes(data):
	errors = {}
	for attr in REQUIRED_ATTRIBUTES:
		if data[attr] == "":
			errors[attr] = "Required field" #map attr to name
			return False, errors
	if errors == {}:
		errors = None
	return True, errors

def get_request(self, name):
	return self.request.get(name).encode("utf-8").replace('"', "'")

def get_attributes(self):
	data = {}
	for attr in ATTRIBUTES:
		data[attr] = get_request(self, attr)
	return data

def populate_sql_statement(data):
	sql_statement = """
		INSERT INTO `service` SET
		`id` = NULL, 
		`name_french` = "{2}", 
		`name_english` = "{3}", 
		`program_id` = "{1}", 
		`age_0` = "{4}", 
		`age_1` = "{5}", 
		`age_2` = "{6}", 
		`age_3` = "{7}", 
		`age_4` = "{8}", 
		`age_5` = "{9}", 
		`age_6` = "{10}", 
		`age_7` = "{11}", 
		`age_8` = "{12}", 
		`age_9` = "{13}", 
		`age_10` = "{14}", 
		`age_11` = "{15}", 
		`age_12` = "{16}", 
		`age_13` = "{17}", 
		`age_14` = "{18}", 
		`age_15` = "{19}", 
		`age_16` = "{20}", 
		`age_17` = "{21}", 
		`age_18` = "{22}", 
		`garcons` = "{23}", 
		`filles` = "{24}", 
		`lundi` = "{25}", 
		`mardi` = "{26}", 
		`mercredi` = "{27}", 
		`jeudi` = "{28}", 
		`vendredi` = "{29}", 
		`samedi` = "{30}", 
		`dimanche` = "{31}", 
		`service_details` = 
		(SELECT CONCAT("| ",
		"{0}", " || ",
		"{1}", " || ",
		`organization`.`1_nom`, " || ",
		`organization`.`departement`, " || ",
		`organization`.`commune`, " || ",
		`organization`.`section_communale`, " || ",
		`organization`.`adresse`, " || ",
		`organization`.`boite_postale`, " || ",
		`organization`.`telephone`, " || ",
		`organization`.`personne_contact`, " || ",
		`organization`.`email`, " || ",
		`organization`.`site_web`, " || ",
		`organization`.`6_type_plusieurs`, " || ",
		`organization`.`6a_precisez_autre`, " || ",
		`organization`.`6c_statut`, " || ",
		`organization`.`7_jour`, " || ",
		`organization`.`7a_heure`, " || ",
		`organization`.`8_objectifs_fondamentaux`, " || ",
		`organization`.`11_quelle_categorie`, " |")
		FROM `organization`
		WHERE `organization`.`id` = "120"
		),
		`notes` = "";
	""".format(data['org_id'], data['program_id'], data['name_french'], data["name_english"], data['age_0'], data['age_1'], data['age_2'], data['age_3'], data['age_4'], data['age_5'], data['age_6'], data['age_7'], data['age_8'], data['age_9'], data['age_10'], data['age_11'], data['age_12'], data['age_13'], data['age_14'], data['age_15'], data['age_16'], data['age_17'], data['age_18'], data['garcons'], data['filles'], data['lundi'], data['mardi'], data['mercredi'], data['jeudi'], data['vendredi'], data['samedi'], data['dimanche'], data['notes'])
	return sql_statement


def save_record(self):
	data = get_attributes(self)
	# raise Exception(data)
	find_or_create_program(data)
	check_for_service_duplicate(data)
	valid, errors = validate_attributes(data)
	# raise Exception(len(data))

	sql_statement = populate_sql_statement(data)
	# raise Exception(sql_statement)
	record = QueryHandler.execute_query(sql_statement, insert=True)
	self.redirect("/admin/records/" + data['org_id'] + "?message=Service saved")
	record_audit = QueryHandler.create_audit(self, "Service", data['name_french'], data, "Create Service")
	return 
