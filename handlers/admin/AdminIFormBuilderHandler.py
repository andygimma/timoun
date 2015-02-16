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
      count = 0
      error_count = 0
      for obj in data:
        if count < 150:
          record = Record.Record()
          full_obj = obj["record"]
          for k in full_obj:
            try:
              if not full_obj[k] == None:
                if isinstance( full_obj[k], ( int, long ) ):
                  full_obj[k] = str(full_obj[k])
                setattr(record, k.lower(), full_obj[k].encode("utf-8").strip())
            except Exception as e:
              error_count += 1
              logging.info("error_count")
              logging.info(error_count)
              logging.info(k)
              logging.info(full_obj[k])
              logging.info(e)
          record.put()
          count += 1
      logging.info("Finished")
      return True

