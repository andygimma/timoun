import logging
import models
from google.appengine.ext import deferred
from google.appengine.ext import db

from models import Commune
from models import Record
BATCH_SIZE = 100  # ideal batch size may vary based on entity size.

def addIfUnique(commune, arr):
    if not commune in arr:
        arr.append(commune)
    return arr

def AddCommune(cursor=None, num_updated=0):
    logging.info("in Add Commune")
    query = Record.Record.query()
    if cursor:
        query.with_cursor(cursor)

    communes = Commune.Commune.query()
    communes_array = []
    for commune in communes:
      communes_array = addIfUnique(commune.name, communes_array)

    for p in query.fetch(limit=BATCH_SIZE):
        commune = p.commune
        communes_array = addIfUnique(commune, communes_array)
    if len(communes_array) > 1:
        logging.info(len(communes_array))
        for commune in communes_array:
          logging.info(commune)
          logging.info(commune)
          c = Commune.Commune(name = commune)
          try:
            c.put()
          except:
            pass
        num_updated += len(to_put)
        logging.debug(
            'Put %d entities to Datastore for a total of %d',
            len(to_put), num_updated)
        deferred.defer(
            UpdateSchema, cursor=query.cursor(), num_updated=num_updated)
    else:
        logging.debug(
            'UpdateSchema complete with %d updates!', num_updated)
