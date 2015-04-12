import os
import webapp2
from handlers import BaseHandler
from models import User, Audit
import csv

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

class ExportHandler(BaseHandler.BaseHandler):
  def get(self, export_type):
    self.response.headers['Content-Type'] = 'text/csv'

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
