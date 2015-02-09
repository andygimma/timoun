import logging
import webapp2
import json
from handlers import BaseHandler
from google.appengine.api import urlfetch
from models import Record


class AdminIFormBuilderHandler(BaseHandler.BaseHandler):
  def get(self):
    logging.info('Starting Main handler')


    url = "https://crs.iformbuilder.com/exzact/dataJSON.php?PAGE_ID=8669630&TABLE_NAME=_data11323_mapping_services_sante_mentales_survey&USERNAME=IBERSLINK&PASSWORD=PASSword@123"

    result = urlfetch.fetch(url=url, deadline=3600)
    logging.info('result')
    logging.info(result)

    if result.status_code == 200:
      data = json.loads(result.content)
      logging.info('data')
      logging.info("len")
      logging.info(len(data))
      logging.info("First data")
      logging.info(data[0]["record"])
      for obj in data:
        record = Record.Record()
        full_obj = obj["record"]
        for k in full_obj:
          setattr(record, k, full_obj[k])
        record.put()
      logging.info("Finished")
      return True

  def post(self):
    raise Exception(22)

    role = self.session.get('role')
    user_session = self.session.get("user")

    if role != "admin":
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return

    if not self.legacy:
      self.redirect("/#/admin")


    url = "https://crs.iformbuilder.com/exzact/dataJSON.php?PAGE_ID=8669630&TABLE_NAME=_data11323_mapping_services_sante_mentales_survey&USERNAME=IBERSLINK&PASSWORD=PASSword@123"

    result = urlfetch.fetch(url=url)

    if result.status_code == 200:
      data = json.loads(result.content)
      raise Exception("post")
      return data
