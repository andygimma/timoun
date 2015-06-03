import os
import webapp2
from handlers import BaseHandler
from models import User, Audit, SearchRecord
import csv
from helpers import QueryHandler

RECORDS_CSV_HEADER = [
  "Nom",
  "General Info",
  "Departement",
  "Commune",
  "Section Communal",
  "Adresse",
  "GPS",
  "Latitude",
  "longitude",
  "Boite Postal",
  "Telephone",
  "Personne Contact",
  "Email",
  "Site Web"
]
RECORD_CSV_FIELDS = [
  "4",
  "3",
  "5",
  "6",
  "7",
  "8",
  "9",
  "10",
  "11",
  "12",
  "13",
  "14",
  "15",
  "16"
]



def SqlToCsvLine(record, fields):
  csv_row = []
  count = 0
  for field in fields:
    try:
      value = record[int(RECORD_CSV_FIELDS[count])]
    except:
      raise Exception(count)
    if value is None:
      csv_row.append("")
    else:
      try:
        csv_row.append(unicode(value).encode("utf-8"))
      except:
        logging.critical("Failed to parse: " + value + " " + str(self.key().id()))
    count += 1
  return csv_row    
      
class PublicExportHandler(BaseHandler.BaseHandler):
  def get(self, export_type):
    self.response.headers['Content-Type'] = 'text/csv'

    if export_type == "map_search":
      self.response.headers['Content-Disposition'] = \
        'attachment; filename="timoun_search_records.csv"'

      page = self.request.get("page")
      page_int = 0
      if page:
        page_int = int(page)
      records = QueryHandler.form_query_builder(self, page_int, limit=2000)
      writer = csv.writer(self.response.out)
      writer.writerow(RECORDS_CSV_HEADER)
      records_string = ""
      for record in records:
        s = '"' + record[5].encode("utf-8") + '"'
        records_string += '{0},'.format(s)
      records_string = records_string[:-1]

      sql_statement = "SELECT * FROM organization WHERE 1_nom IN ({0});".format(records_string)
      # raise Exception(sql_statement)
      org_records = QueryHandler.execute_query(sql_statement)
      for record in org_records:
        writer.writerow(SqlToCsvLine(record, RECORD_CSV_FIELDS))

