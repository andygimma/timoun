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


    if result.status_code == 200:
      data = json.loads(result.content)
      count = 0
      error_count = 0
      for obj in data:
        if count < 15000:
          record = Record.Record()
          full_obj = obj["record"]
          for k in full_obj:
            try:
              if not full_obj[k] == None:
                if isinstance( full_obj[k], ( int, long ) ):
                  full_obj[k] = str(full_obj[k])
                setattr(record, k.lower(), full_obj[k].encode("utf-8").strip())

                if k.encode("utf-8").strip().lower() == "gps_":
                  logging.info("length")
                  logging.info(len(full_obj[k].encode("utf-8").strip().lower()))
                  if len(str(full_obj[k].encode("utf-8").strip().lower())) is not 0:
                    k = full_obj[k].encode("utf-8").strip()
                    try:
                      latitude_index = k.index("Latitude:")
                      latitude_index = latitude_index + 9
                      latitude = k[latitude_index: latitude_index + 8]
                      #logging.info(latitude)

                      setattr(record, "latitude", latitude.encode("utf-8").strip())

                      longitude_index = k.index("Longitude:")
                      longitude_index = longitude_index + 10
                      longitude = k[longitude_index: longitude_index + 8]
                      #logging.info(longitude)
                      setattr(record, "longitude", longitude.encode("utf-8").strip())
                    except:
                      latitude = k[:9]
                      setattr(record, "latitude", latitude.encode("utf-8").strip())

                      longitude = k[11:20]
                      setattr(record, "latitude", latitude.encode("utf-8").strip())
                  else:
                    setattr(record, "latitude", "empty")
                    setattr(record, "latitude", "empty")

            except Exception as e:
              error_count += 1
              logging.info("error_count")
              logging.info(error_count)
              logging.info(k)
              #logging.info(full_obj[k])
              logging.info(e)


          record.put()
          count += 1
      logging.info("Finished")
      return True

