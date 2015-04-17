from google.appengine.ext import ndb
import os
import jinja2
import webapp2
from handlers import BaseHandler
from helpers import QueryHandler

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/static_pages"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('en_search.html')

class SearchHandler(BaseHandler.BaseHandler):
  def get(self):
    keywords = self.request.get("keywords")
    service = self.request.get("service")
    department = self.request.get("department")
    age_start = self.request.get("age_start")
    age_end = self.request.get("age_end")
    gender = self.request.get("gender")
    if False: #search(self):
      pass
    else: 
      page = self.request.get("page")
      if page == None:
        page = 0
      if gender:
        if gender == "male":
          qry = ndb.gql("SELECT * FROM Record WHERE estce_que_votre_organisation_offre_des_services_en_sant_men = 'oui' LIMIT 50")
        if gender == "female":
          qry = ndb.gql("SELECT * FROM Record WHERE estce_que_votre_organisation_offre_des_services_en_sant_men = 'non' LIMIT 50")

        if gender == "none" or gender == None:
          qry = ndb.gql("SELECT * FROM Record")

        records = qry.fetch(50)
        role = self.session.get('role')
        user_session = self.session.get("user")
        template_values = {
          "role": self.session.get("role"),
          "user_session": user_session,
          "message": self.request.get("message"),
          "records": records,
          "gender": gender
        }
        LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('en_search.html')
        self.response.write(LEGACY_TEMPLATE.render(template_values))
        return

      language = None
      if "language" in self.request.cookies:
        language = self.request.cookies["language"]
      else:
        language = "fr"
        self.response.set_cookie("language", "fr")

      language = language.replace('"', '').replace("'", "")
      if language == "fr":
        LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_search.html')
      else:
        LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('en_search.html')

      if not self.legacy:
        self.redirect("/#/search")

      role = self.session.get('role')
      user_session = self.session.get("user")
      template_values = {
        "role": self.session.get("role"),
        "user_session": user_session,
        "message": self.request.get("message"),
        "services_select": QueryHandler.get_services_select()
      }
      self.response.write(LEGACY_TEMPLATE.render(template_values))

  def post(self):
    gql_string = None
    gender = self.request.get("gender")
    #if male == "male":
    page = 2
    gql_string = query_builder(None, "estce_que_votre_organisation_offre_des_services_en_sant_men = 'oui' AND si_autre_precisez_ = 'oui' AND soins_de_sant_communautaires_informels = 'oui' AND soins_de_sant_primaire = 'oui' AND si_oui_prciser__plusieurs_rponses_possibles = 'oui' AND soins_psychiatriques = 'oui' AND soins_psychologiques = 'oui' AND relation_daide = 'oui' AND counseling = 'oui' AND precisez2 = 'oui' AND autre_petita = 'oui' AND preciser_autres = 'oui' AND sant_communautaires = 'oui' AND santprimaire2 = 'oui' AND soins_de_counseling = 'oui' AND soins_sante_psychologiques2 = 'uoi' AND soins_santepsychiatriques3 = 'oui' AND grille_tarifaire_relation3 = 'oui' AND combien_mensuellement = 'oui' AND pour_quelles_raisons = 'oui' AND approx_precisez = 'oui' AND comment_publicisez = 'uoi' AND precisez_autres2 = 'oui' AND dcrire_les_catgories_dintervenants_ = 'oui' AND autre_categorie_intervenants = 'oui' AND autres_categories_precisez = 'oui' AND endroits_formation_precisez_autres = 'oui' AND autres_endroit_de_suivi_formation='oui' AND quels_organismes_vous_rfrez_les_demandes = 'oui' AND organisme_relation_de_formation='oui' AND organisme_relation_dchanges_de_pratique = 'oui' AND autres_organismes_relations = 'oui' AND obstacles_rencontre_dispensation_services = 'oui' AND autres_obstacles_precisez = 'oui' AND obstacles_rencontre_par_patients = 'oui' AND si_oui_savezvous_pourquoi = 'oui' AND demandes_pas_de_specialites = 'oui' AND connaissezvous_gens_communaute_formation_academik = 'oui' AND sant_communautaires_informels = 'oui' AND sant_primaire = 'oui' AND counseling2 = 'oui'")
    qry = None

    if gender == "male":
      qry = ndb.gql("SELECT * FROM Record WHERE estce_que_votre_organisation_offre_des_services_en_sant_men = 'oui' LIMIT 50 OFFSET {0}".format(str(page * 50)))
    if gender == "female":
      qry = ndb.gql("SELECT * FROM Record WHERE estce_que_votre_organisation_offre_des_services_en_sant_men = 'non' LIMIT 50 OFFSET {0}".format(str(page * 50)))

    if gender == "none" or gender == None:
      qry = ndb.gql("SELECT * FROM Record")

    records = qry.fetch(50)
    #raise Exception(len(entities))
    role = self.session.get('role')
    user_session = self.session.get("user")
    template_values = {
      "role": self.session.get("role"),
      "user_session": user_session,
      "message": self.request.get("message"),
      "records": records,
      "gender": gender,
    }
    LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('en_search.html')
    self.response.write(LEGACY_TEMPLATE.render(template_values))

def query_builder(query_string, new_string):
  if not query_string:
    query_string = "SELECT * FROM Record WHERE "
  return query_string + new_string

def search(self):
  keywords = self.request.get("keywords")
  service = self.request.get("service")
  department = self.request.get("department")
  age_start = self.request.get("age_start")
  age_end = self.request.get("age_end")
  gender = self.request.get("gender")

  if keywords or service or department or age_start or age_end or gender:
    return True
  else:
    return False
