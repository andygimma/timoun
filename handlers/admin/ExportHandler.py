import os
import webapp2
from handlers import BaseHandler
from models import User, Audit, SearchRecord
import csv
from helpers import QueryHandler


SEARCHES_CSV_FIELDS = [
      'ip_address',
      'created_at',
      'keywords',
      'service',
      'department',
      'age_start',
      'age_end',
      'gender'
]

USER_CSV_FIELDS = [
      'name',
      'email',
      'organization',
      'phone',
      'email',
      'role',
      'email_authorized',
      'created_at'
]

USER_DASHBOARD_CSV_FIELDS =[
      'action',
      'initiated_by',
      'json_data',
      'model_affected',
      'security_clearance',
      'user_affected',
      'created_at'
]

USER_DASHBOARD_CSV_HEADER =[
      'action',
      'initiated_by',
      'changes',
      'model_affected',
      'security_clearance',
      'user_affected',
      'created_at'
]

DASHBOARD_CSV_HEADER = [
      'action',
      'initiated_by',
      'changes',
      'model_affected',
      'security_clearance',
      'user_affected',
      'created_at'
]

DASHBOARD_CSV_FIELDS = [
      'action',
      'initiated_by',
      'json_data',
      'model_affected',
      'security_clearance',
      'user_affected',
      'created_at'
]

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
  "Site Web",
  "1_estce_que_votre",
  "3_connaissezvous",
  "4estce_que_votre",
  "4a_comment_publicisezvous",
  "4b_estce_que_vos",
  "5_ces_services",
  "6_recevezvous_des",
  "6_type_plusieurs",
  "6a_precisez_autre",
  "6b_autre_organisation",
  "6c_statut",
  "6d_autre_status",
  "7_jour",
  "7_preciser_lales",
  "7a_heure",
  "8_objectifs_fondamentaux",
  "8_pouvezvous_decrire",
  "8a_quel_est_le",
  "8b1_precisez_",
  "8c_offrezvous_des",
  "8c1_medication",
  "8c2_activites_psychosociales",
  "8c3_accompagnement",
  "8c4_psychanalyse",
  "8c5_musicotherapie",
  "8c6_club_denfants",
  "8c7_activites_socioculturelles",
  "8c8_groupe_dentraide",
  "8c9_psychoeducation",
  "8c10_therapie_corporelle",
  "8c11_therapie_cognitive",
  "8c12_therapie_par",
  "8c13_autres",
  "9_source_de_financement",
  "9a_lequel_t",
  "9b_autre_source",
  "10_comment_votre",
  "10a_si_vous_referez",
  "11_quelle_categorie",
  "11_pouvezvous_dire",
  "11a_dechanges_de",
  "11b_de_referencement",
  "11c_de_formation",
  "11d_autres",
  "13_quels_sont_les",
  "14_quels_obstacles",
  "14a_si_autres_",
  "15_quels_obstacles",
  "16_connaissezvous",
  "_17_tranche_dge",
  "_18_tranche_dge",
  "19_quel_est_le",
  "20_etesvous_en",
  "21_comment_lorganisation",
  "21a_citez_5_defis",
  "21b_citez_5_lecons",
  "23_connaissezvous",
  "23a_noms_des_oganisation",
  "23b_citez_les_services",
  "23c_si_oui_lesquels",
  "quels_sont_les",
  "question_a",
  "question_b",
  "question_c",
  "question_d",
  "created_date",
  "created_by",
  "created_location",
  "created_device_id",
  "modified_date",
  "modified_by",
  "modified_location",
  "modified_device_id",
  "server_modified",
  "quand_votre_service",
  "quand_estce_que",
  "votre_organisation",
  "si_oui_prciser",
  "catgories_denfants",
  "my_element14",
  "quel_endroit",
  "les_principaux",
  "services_fin"

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
  "16",
  "49",
  "50",
  "55",
  "56",
  "57",
  "58",
  "59",
  "17",
  "18",
  "20",
  "19",
  "21",
  "22",
  "60",
  "23",
  "24",
  "61",
  "62",
  "64",
  "65",
  "66",
  "67",
  "68",
  "69",
  "70",
  "71",
  "72",
  "73",
  "74",
  "75",
  "76",
  "77",
  "78",
  "25",
  "27",
  "26",
  "30",
  "80",
  "31",
  "81",
  "82",
  "83",
  "84",
  "85",
  "86",
  "87",
  "88",
  "89",
  "90",
  "44",
  "45",
  "32",
  "33",
  "34",
  "35",
  "35",
  "37",
  "38",
  "39",
  "40",
  "96",
  "97",
  "98",
  "99",
  "100",
  "101",
  "102",
  "103",
  "104",
  "105",
  "106",
  "107",
  "108",
  "109",
  "41",
  "42",
  "43",
  "91",
  "92",
  "93",
  "94",
  "95",
  "48"
]


def ToCsvLine(model, fields):
  """Returns the site as a list of string values, one per field in
  CSV_FIELDS."""
  csv_row = []
  for field in fields:
    value = getattr(model, field)
    if value is None:
      csv_row.append('')
    else:
      try:
        csv_row.append(unicode(value).encode("utf-8"))
      except:
        logging.critical("Failed to parse: " + value + " " + str(self.key().id()))
  return csv_row

def SqlToCsvLine(record, fields):
  csv_row = []
  count = 0
  for field in fields:
    value = record[int(RECORD_CSV_FIELDS[count])]
    if value is None:
      csv_row.append("")
    else:
      try:
        csv_row.append(unicode(value).encode("utf-8"))
      except:
        logging.critical("Failed to parse: " + value + " " + str(self.key().id()))
    count += 1
  return csv_row    
      
class ExportHandler(BaseHandler.BaseHandler):
  def get(self, export_type):
    self.response.headers['Content-Type'] = 'text/csv'

    if export_type == "searches":
      self.response.headers['Content-Disposition'] = \
        'attachment; filename="timoun_search_records.csv"'

      writer = csv.writer(self.response.out)

      writer.writerow(SEARCHES_CSV_FIELDS)
      searches = SearchRecord.SearchRecord.query()
      for search in searches:
          writer.writerow(ToCsvLine(search, SEARCHES_CSV_FIELDS))


    if export_type == "user_dashboard":
      self.response.headers['Content-Disposition'] = \
        'attachment; filename="timoun_user_dashboard.csv"'

      writer = csv.writer(self.response.out)

      writer.writerow(USER_DASHBOARD_CSV_HEADER)
      audits = Audit.Audit.query(Audit.Audit.model_affected == "User").order(Audit.Audit.created_at)

      for audit in audits:
          writer.writerow(ToCsvLine(audit, USER_DASHBOARD_CSV_FIELDS))


    if export_type == "users":
      self.response.headers['Content-Disposition'] = \
          'attachment; filename="timoun_users.csv"'
      writer = csv.writer(self.response.out)

      writer.writerow(USER_CSV_FIELDS)
      users = User.User.query().order(User.User.email)

      for user in users:
          writer.writerow(ToCsvLine(user, USER_CSV_FIELDS))

    if export_type == "dashboard":
      self.response.headers['Content-Disposition'] = \
          'attachment; filename="timoun_users.csv"'
      writer = csv.writer(self.response.out)

      writer.writerow(DASHBOARD_CSV_HEADER)
      audits = Audit.Audit.query().order(Audit.Audit.created_at)
      for audit in audits:
          writer.writerow(ToCsvLine(audit, DASHBOARD_CSV_FIELDS))


    if export_type == "records":
      self.response.headers['Content-Disposition'] = \
          'attachment; filename="timoun_records.csv"'
      writer = csv.writer(self.response.out)

      writer.writerow(RECORDS_CSV_HEADER)
      sql_statement = "SELECT * FROM organization;"
      records = QueryHandler.execute_query(sql_statement)
      for record in records:
        writer.writerow(SqlToCsvLine(record, RECORD_CSV_FIELDS))

    if export_type == "view_record":
      self.response.headers['Content-Disposition'] = \
          'attachment; filename="timoun_records.csv"'
      writer = csv.writer(self.response.out)
      record_id = self.request.get("record_id")
      writer.writerow(RECORDS_CSV_HEADER)
      sql_statement = """
        SELECT * FROM organization WHERE id="{0}";
        """.format(record_id)
      records = QueryHandler.execute_query(sql_statement)
      for record in records:
        writer.writerow(SqlToCsvLine(record, RECORD_CSV_FIELDS))
