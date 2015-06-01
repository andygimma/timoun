# -*- coding: utf-8 -*- 
import os
import json
import MySQLdb
from models import SearchRecord
import unicodedata
from helpers import QueryHandler
from models import Audit

ATTRIBUTES = ["org_id", "program_id", "date", "budget", "other", "types", "assistance"]
REQUIRED_ATTRIBUTES = ["org_id", "program_id"]

def find_or_create_program(data):
	sql_statement = """
			SELECT id FROM org_prog WHERE id="{0}"
			""".format(data['program_id'])
	program = QueryHandler.execute_query(sql_statement)
	if len(program) > 0:
		raise Exception("Program already exists")

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
		INSERT INTO `org_prog` SET
		`id` = NULL,
		`org_id` = "{0}",
		`program_id` = "{1}",
		`date` = "{2}",
		`budget` = "{3}",
		`other` = "{4}",
		`types` = "{5}",
		`assistance` = "{6}";
	""".format(data["org_id"], data["program_id"], data["date"], data["budget"], data["other"], data["types"], data["assistance"])
	# raise Exception(sql_statement)
	return sql_statement

def populate_update_statement(data):
	sql_statement = """
		UPDATE `org_prog` SET
		`org_id` = "{0}",
		`program_id` = "{1}",
		`date` = "{2}",
		`budget` = "{3}",
		`other` = "{4}",
		`types` = "{5}",
		`assistance` = "{6}"
		WHERE `id` = "{1}"
		LIMIT 1;
	""".format(data["org_id"], data["program_id"], data["date"], data["budget"], data["other"], data["types"], data["assistance"])
	# raise Exception(sql_statement)
	return sql_statement


def save_record(self):
	data = get_attributes(self)
	valid, errors = validate_attributes(data)
	sql_statement = populate_sql_statement(data)
	record = QueryHandler.execute_query(sql_statement, insert=True)
	self.redirect("/admin/records/" + data['org_id'] + "?message=Program saved")
	record_audit = QueryHandler.create_audit(self, "Program", "Program", data, "Create Program")
	return 

def update_record(self):
	data = get_attributes(self)
	# raise Exception(data)
	valid, errors = validate_attributes(data)
	sql_statement = populate_update_statement(data)
	record = QueryHandler.execute_query(sql_statement, True)
	record_audit = QueryHandler.create_audit(self, "Program", "Program", data, "Update Program")
	return

    
