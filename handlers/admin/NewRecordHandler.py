# -*- coding: utf-8 -*- 

import os
import jinja2
import webapp2
from handlers import BaseHandler
from models import Record
from helpers import QueryHandler, OrganizationHelper
from config import enums

NOT_IN_ORG_SCOPE = ["Program", "Service", "Nutrition", "Home-Based Care", "Child Protection", "Health", "Psychosocial Support", "Education", "Mental Health Services"]

DO_NOT_SHOW = [
  "assistance_avec",
  "autre_education",
  "autre_home_bases",
  "autre_nutrition",
  "autre_protection",
  "autre_sante_passe",
  "autre_soutien_passe",
  "budget_us_prog1",
  "budget_us_prog2",
  "budget_us_prog3",
  "budget_us_prog4",
  "budget_us_prog5",
  "budget_us_prog6",
  "budget_us_prog7",
  "date_prog1_exemple",
  "date_prog2_exemple",
  "date_prog3_exemple",
  "date_prog4_exemple",
  "date_prog5_exemple",
  "date_prog6_exemple",
  "date_prog7_exemple",
  "types_de_thrapie"
]

DROPDOWNS = [
  "6_type_plusieurs", 
  "6c_statut",
  "7_jour", 
  "7a_heure", 
  "9_source_de_financement",
  "11_quelle_categorie",
  "4a_comment_publicisezvous",
  "5_ces_services",
  "7_preciser_lales",
  "8_pouvezvous_decrire",
  "8a_quel_est_le",
  "8b_a_quel_endroit",
  "10_que_faitesvous",
  "14_quels_obstacles",
  "assistance_avec",
  "si_oui_prciser",
  "catgories_denfants",
  "my_element14",
  "quel_endroit",
  "les_principaux",
  "types_de_thrapie"
]

TEXTAREAS = [
  "8_objectifs_fondamentaux",
  "10_comment_votre",
  "21_comment_lorganisation",
  "21a_citez_5_defis",
  "21b_citez_5_lecons",
  "23a_noms_des_oganisation",
  "23b_citez_les_services",
  "15_quels_obstacles",
]
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__),"../../templates/admin"),
         os.path.join(os.path.dirname(__file__),"../../templates/layouts")]))

LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('new_record.html')

class NewRecordHandler(BaseHandler.BaseHandler):
  def post(self):
    OrganizationHelper.save_record(self)

  def get(self):

    sql_statement= """
      SELECT `t0`.`id` AS `lev0_id`, `t0`.`name_french` AS `lev0_name_fr`, `t0`.`name_english` AS `lev0_name_en`, `t1`.`id` AS `lev1_id`, `t1`.`name_french` AS `lev1_name_fr`, `t1`.`name_english` AS `lev1_name_en`, `t1`.`name_safe_short` AS `lev1_name_short`, `t1`.`access` AS `lev1_access`, `t1`.`html_form_type` AS `lev1_type`, `t2`.`id` AS `lev2_id`, `t2`.`name_french` AS `lev2_name_fr`, `t2`.`name_english` AS `lev2_name_en`, `t2`.`name_safe_short` AS `lev2_name_short`, `t2`.`access` AS `lev2_access`, `t2`.`html_form_type` AS `lev2_type`, `t3`.`id` AS `lev3_id`, `t3`.`name_french` AS `lev3_name_fr`, `t3`.`name_english` AS `lev3_name_en`, `t3`.`name_safe_short` AS `lev3_name_short`, `t3`.`access` AS `lev3_access`, `t3`.`html_form_type` AS `lev3_type`
      FROM `section` AS `t0`
      LEFT JOIN `attribute` AS `t1` ON `t1`.`section_id` = `t0`.`id`
      LEFT JOIN `attribute` AS `t2` ON `t2`.`parent_id` = `t1`.`id`
      LEFT JOIN `attribute` AS `t3` ON `t3`.`parent_id` = `t2`.`id`
      WHERE `t1`.`parent_id` = 0
      AND `t1`.`is_depreciated` = 0;

    """

    better_sql = """
      SELECT `name_safe_short`, `name_french`, `name_english` FROM `attribute` WHERE `is_depreciated` = 0 AND `section_id` < 16;
    """

    records = QueryHandler.execute_query(sql_statement)
    # raise Exception(records[23][8])
    better_records = QueryHandler.execute_query(better_sql)
    better_html = better_form(better_records)

    html_string = form_builder(records)
    role = self.session.get('role')
    user_session = self.session.get("user")

    if role != "admin":
      self.redirect("/users/login?message={0}".format("You are not authorized to view this page"))
      return


    form = Record.RecordForm()
    template_values = {
      "form": form,
      "user_session": user_session,
      "html_string": html_string,
      "better_html": better_html
    }
    language = None
    if "language" in self.request.cookies:
      language = self.request.cookies["language"]
    else:
      language = "fr"
      self.response.set_cookie("language", "fr")

    language = language.replace('"', '').replace("'", "")
    if language == "fr":

      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('fr_new_record.html')
    else:
      LEGACY_TEMPLATE = JINJA_ENVIRONMENT.get_template('new_record.html')
    self.response.write(LEGACY_TEMPLATE.render(template_values))

def form_builder(records):
  html_string = ""
  last_header = ""
  for record in records:
    html_string += "<br>"
    if record[2] in NOT_IN_ORG_SCOPE:
      pass
    else:
      if record[2] != last_header:
        html_string += "<h2>{0}</h2>".format(record[2])
        last_header = record[2]
      name = get_name(record)
      if record[8] == "text":
        html_string += "{0}: <input id='first' name='{0}'' type='text' />\n".format(name)
      if record[8] == "dropdown":
        name = record[12]

        html_string += "{0}: <select><option>Select</option>\n".format(name)

        form_enums = enums.form_enums
        count = 0
        if record[12] in form_enums:
          this_enum = form_enums[record[12]]
          for item in this_enum:
            # encoded_item = item.encode("latin-1").decode("utf-8")
            html_string += "<option>{0}</option>".format(item.encode('ascii', 'ignore'))

        html_string += "</select>\n"
      if record[8] == "textarea":
        html_string += "{0}: <textarea name='{0}'' cols=40 rows=6></textarea>\n".format(name)

  return html_string

def get_name(record):
  if record[17]:
    return record[17]
  if record[11]:
    return record[11]
  if record[5]:
    return record[5]

def better_form(records):
  html_string = "<br>"
  for record in records:
    if record[0] not in DO_NOT_SHOW:
      if record[0] in DROPDOWNS:
        if record[0] == "6c_statut":
          select = """
            {0}: <select name='6c_statut'>
              <option value="">Select one</option>
              <option value='Permis de fonctionnement'>Permis de fonctionnement</option>
              <option value='Autorisation de fonctionnement'>Autorisation de fonctionnement</option>
              <option value='Démarche en cours'>Démarche en cours</option>
              <option value='Refus de repondre'>Refus de repondre</option>
              <option value='Autres'>Autres</option>
            </select>
          """.decode('utf-8').format(record[2])
          html_string += select
        elif record[0] == "6_type_plusieurs":
          select = """
            {0}: <select name='6_type_plusieurs'>
              <option value="">Select one</option>
              <option value='Organisation non gouvernementale internationale'>Organisation non gouvernementale internationale</option>
              <option value='Autres à spécifier'>Autres à spécifier</option>
              <option value='Organisation non gouvernementale nationale'>Organisation non gouvernementale nationale</option>
              <option value='Association locale'>Association locale</option>
              <option value='Entreprise privée'>Entreprise privée</option>
              <option value='précisez___________________'>précisez</option>
              <option value='Structure religieuse'>Structure religieuse</option>
              <option value='Organisation communautaire de base'>Organisation communautaire de base</option>
              <option value='Organisme gouvernemental'>Organisme gouvernemental</option>
              <option value='Coopérative'>Coopérative</option>
              <option value='Autres'>Autres</option>
              <option value='Organisation des Nations Unies'>Organisation des Nations Unies</option>
              <option value='Mutuelles'>Mutuelles</option>
            </select>
          """.decode('utf-8').format(record[2])
          html_string += select
        elif record[0] == "7_jour":
          select = """
          {0}: <select name='7_jour'>
            <option value="">Select one</option>
            <option value='Mardi'>Mardi</option>
            <option value='Mercredi'>Mercredi</option>
            <option value='Vendre'>Vendre</option>
            <option value='Jeudi'>Jeudi</option>
            <option value='Lundi'>Lundi</option>
            <option value='Vendredi'>Vendredi</option>
            <option value='Dimanche'>Dimanche</option>
            <option value='Samedi'>Samedi</option>
          </select>
          """.decode('utf-8').format(record[2])
          html_string += select

        elif record[0] == "7a_heure":
          select = """
          {0}: <select name='7a_heure'>
            <option value="">Select one</option>
            <option value='Temps partiel'>Temps partiel</option>
            <option value='Temps Plein'>Temps Plein</option>
            <option value='24/24'>24/24</option>
          </select>
          """.decode('utf-8').format(record[2]) 
          html_string += select  
          
        elif record[0] == "9_source_de_financement":
          select = """
          {0}: <select name='9_source_de_financement'>
            <option value="">Select one</option>
            <option value='Bailleur international'>Bailleur international</option>
            <option value='laquelle ? ____________________'>laquelle</option>
            <option value='lequel ?______________________'>lequel</option>
            <option value='Structure religieuse'>Structure religieuse</option>
            <option value='Privée'>Privée</option>
            <option value='Autres'>Autres</option>
            <option value='Levée de fonds auprès de _____ préciser___________'>Levée de fonds auprès de _____ préciser___________</option>
            <option value='Levée de fonds'>Levée de fonds</option>
            <option value='Cotisations de membres'>Cotisations de membres</option>
            <option value='Bailleur privé (veuillez ne pas citer de nom)'>Bailleur privé (veuillez ne pas citer de nom)</option>
            <option value='Combien ?_______________'>Combien ?_______________</option>
            <option value='Services payants'>Services payants</option>
            <option value='Gouvernement'>Gouvernement</option>
            <option value='ministère'>ministère</option>
          </select>
          """.decode('utf-8').format(record[2]) 
          html_string += select 

        elif record[0] == "11_quelle_categorie":
          select = """
          {0}: <select name='11_quelle_categorie'>
            <option value="">Select one</option>
            <option value='Enfant parents'>Enfant parents</option>
            <option value='Enfants abandonnés'>Enfants abandonnés</option>
            <option value='Enfants chef de ménage'>Enfants chef de ménage</option>
            <option value='Enfants en domesticité'>Enfants en domesticité</option>
            <option value='Enfants en situation d'urgence.'>Enfants en situation d'urgence.</option>
            <option value='Enfants en situation de rue'>Enfants en situation de rue</option>
            <option value='Enfants handicapés'>Enfants handicapés</option>
            <option value='Enfants orphelins'>Enfants orphelins</option>
            <option value='Enfants pratiquant la mendicité'>Enfants pratiquant la mendicité</option>
            <option value='Enfants sans documentation'>Enfants sans documentation</option>
            <option value='Enfants séparés'>Enfants séparés</option>
            <option value='Enfants travailleurs / marchands / vendeurs'>Enfants travailleurs / marchands / vendeurs</option>
            <option value='marchands'>marchands</option>
            <option value='Enfants victimes d'exploitation sexuelle'>Enfants victimes d'exploitation sexuelle</option>
            <option value='Enfants non accompagnés'>Enfants non accompagnés</option>
            <option value='Enfants victimes de la traite'>Enfants victimes de la traite</option>
            <option value='Enfants vivant en institution Médicalisée'>Enfants vivant en institution Médicalisée</option>
            <option value='enfants affectés par le VIH'>enfants affectés par le VIH</option>
            <option value='Autres'>Autres</option>
            <option value='Enfants en contact avec la loi'>Enfants en contact avec la loi</option>
            <option value='Enfants vivant en institution Maison d'enfants généraliste'>Enfants vivant en institution Maison d'enfants généraliste</option>
            <option value='Enfants vivant en institution Centre de détention'>Enfants vivant en institution Centre de détention</option>
            <option value='nfants en conflit avec la loi'>nfants en conflit avec la loi</option>
            <option value='Enfants affectés par la violence armée'>Enfants affectés par la violence armée</option>
          </select>
          """.decode('utf-8').format(record[2]) 
          html_string += select 

        elif record[0] == "4a_comment_publicisezvous":
          select = """
          {0}: <select name='4a_comment_publicisezvous'>
            <option value="">Select one</option>
            <option value='Autres'>Autres</option>
            <option value='AffichesAffiches'>Affiches</option>
            <option value='Réunions communautaires'>Réunions communautaires</option>
            <option value='Dépliants'>Dépliants</option>
            <option value='Radio'>Radio</option>
            <option value='Télévision'>Télévision</option>
          </select>
          """.decode('utf-8').format(record[2]) 
          html_string += select 

        elif record[0] == "5_ces_services":
          select = """
          {0}: <select name='5_ces_services'>
            <option value="">Select one</option>
            <option value='Enfants vulnérables et parents/tuteurs'>Enfants vulnérables et parents/tuteurs</option>
            <option value='Enfants Vulnérables seulement'>Enfants Vulnérables seulement</option>
            <option value='Parents/tuteurs seulement'>Parents/tuteurs seulement</option>
          </select>
          """.decode('utf-8').format(record[2]) 
          html_string += select 

        elif record[0] == "7_preciser_lales":
          select = """
          {0}: <select name='7_preciser_lales'>
            <option value="">Select one</option>
            <option value='enfants affectés par le VIH'>enfants affectés par le VIH</option>
            <option value='Enfants infectés'>Enfants infectés</option>
            <option value='Enfants handicapés'>Enfants handicapés</option>
            <option value='Enfants orphelin'>Enfants orphelin</option>
            <option value='Enfants chef de ménage'>Enfants chef de ménage</option>
            <option value='Enfants en situation d'urgence'>Enfants en situation d'urgence</option>
            <option value='Enfants exploités sexuellement'>Enfants exploités sexuellement</option>
            <option value='Filles mères'>Filles mères</option>
            <option value='Enfants abandonnés'>Enfants abandonnés</option>
            <option value='non accompagnés'>non accompagnés</option>
            <option value='Enfants en domesticité'>Enfants en domesticité</option>
            <option value='Enfants en situation de mendicité'>Enfants en situation de mendicité</option>
            <option value='Enfants en situation de Rue'>Enfants en situation de Rue</option>
            <option value='Autres'>Autres</option>
            <option value='Enfants victimes de la traite et du trafic'>Enfants victimes de la traite et du trafic</option>
            <option value='Enfants en conflit avec la loi'>Enfants en conflit avec la loi</option>
            <option value='Enfants marchands / vendeurs'>Enfants marchands / vendeurs</option>
            <option value='Enfants affectés par la violence armée'>Enfants affectés par la violence armée</option>
          </select>
          """.decode('utf-8').format(record[2]) 
          html_string += select 

        elif record[0] == "8_pouvezvous_decrire":
          select = """
          {0}: <select name='8_pouvezvous_decrire'>
            <option value="">Select one</option>
            <option value='Autres'>Autres</option>
            <option value='Infirmiers/infirmières spécialisé (e)s'>Infirmiers/infirmières spécialisé (e)s</option>
            <option value='Psychiatres'>Psychiatres</option>
            <option value='Travailleurs sociaux'>Travailleurs sociaux</option>
            <option value='Bénévoles'>Bénévoles</option>
            <option value='Travailleurs communautaires'>Travailleurs communautaires</option>
            <option value='Aidants naturels'>Aidants naturels</option>
            <option value='Pairs aidants'>Pairs aidants</option>
            <option value='Médecins généralistes'>Médecins généralistes</option>
          </select>
          """.decode('utf-8').format(record[2]) 
          html_string += select 

        elif record[0] == "8a_quel_est_le":
          select = """
          {0}: <select name='8a_quel_est_le'>
            <option value="">Select one</option>
            <option value='Formation spécialisées en santé mentale'>Formation spécialisées en santé mentale</option>
            <option value='Universitaire licencié'>Universitaire licencié</option>
            <option value='Mémorand'>Mémorand</option>
            <option value='Formation sur le tas'>Formation sur le tas</option>
            <option value='Universitaire en cours de formation'>Universitaire en cours de formation</option>
            <option value='Autres'>Autres</option>
            <option value='Formation de base en santé mentale'>Formation de base en santé mentale</option>
          </select>
          """.decode('utf-8').format(record[2]) 
          html_string += select 

        elif record[0] == "8b_a_quel_endroit":
          select = """
          {0}: <select name='8b_a_quel_endroit'>
            <option value="">Select one</option>
            <option value='Autres'>Autres</option>
            <option value='Université d'État d'Haïti (UEH)'>Université d'État d'Haïti (UEH)</option>
            <option value='Université privée'>Université privée</option>
            <option value='Formation non formelle'>Formation non formelle</option>
           </select>
          """.decode('utf-8').format(record[2]) 

        elif record[0] == "10_que_faitesvous":
          select = """
          {0}: <select name='10_que_faitesvous'>
            <option value="">Select one</option>
            <option value='Vous référez'>Vous référez</option>
            <option value='Rien'>Rien</option>
            <option value='Il n'y a aucune possibilité dans la région'>Il n'y a aucune possibilité dans la région</option>
            <option value='nous ne sommes pas en contact avec d'autres centres'>nous ne sommes pas en contact avec d'autres centres</option>
          </select>
          """.decode('utf-8').format(record[2])
          html_string += select

        elif record[0] == "14_quels_obstacles":
          select = """
          {0}: <select name='14_quels_obstacles'>
            <option value="">Select one</option>
            <option value='Autres'>Autres</option>
            <option value='Perception de la maladie mentale dans le milieu'>Perception de la maladie mentale dans le milieu</option>
            <option value='Absence de matériels'>Absence de matériels</option>
            <option value='Absence de professionnels'>Absence de professionnels</option>
            <option value='Problèmes logistiques'>Problèmes logistiques</option>
            <option value='Non observance des thérapies'>Non observance des thérapies</option>
          </select>
          """.decode('utf-8').format(record[2])
          html_string += select  

        elif record[0] == "assistance_avec":
          select = """
          {0}: <select name='assistance_avec'>
            <option value="">Select one</option>
            <option value='par anenfant'>par anenfant</option>
            <option value='autres spcifierautres spcifier'>autres spcifier</option>
            <option value='matriels dcole livres uniforme cahier'>matriels dcole livres uniforme cahier</option>
            <option value='paiement de frais scolaire si oui combien'>paiement de frais scolaire si oui combien</option>
            <option value='par moisenfant'>par moisenfant</option>
          </select>
          """.decode('utf-8').format(record[2])
          html_string += select  

        elif record[0] == "si_oui_prciser":
          select = """
          {0}: <select name='si_oui_prciser'>
            <option value="">Select one</option>
            <option value='counseling'>counseling</option>
            <option value='soins de sant communautaires informels'>soins de sant communautaires informels</option>
            <option value='soins de sant primaire'>soins de sant primaire</option>
            <option value='soins psychologiques'>soins psychologiques</option>
            <option value='relation daide'>relation daide</option>
            <option value='soins psychiatriques'>soins psychiatriques</option>
            <option value='autres'>autres</option>
          </select>
          """.decode('utf-8').format(record[2])
          html_string += select

        elif record[0] == "catgories_denfants":
          select = """
          {0}: <select name='catgories_denfants'>
            <option value="">Select one</option>
            <option value='enfants affects par le vih'>enfants affects par le vih</option>
            <option value='enfants infects'>enfants infects</option>
            <option value='enfants en institution'>enfants en institution</option>
            <option value='enfants handicaps'>enfants handicaps</option>
            <option value='enfants orphelin'>enfants orphelin</option>
            <option value='enfants abandonns non accompagns'>enfants abandonns non accompagns</option>
            <option value='enfants chef de mnage'>enfants chef de mnage</option>
            <option value='enfants en domesticit'>enfants en domesticit</option>
            <option value='enfants en situation de mendicit'>enfants en situation de mendicit</option>
            <option value='enfants en situation de rue'>enfants en situation de rue</option>
            <option value='filles mres'>filles mres</option>
            <option value='enfants en situation durgence.'>enfants en situation durgence.</option>
            <option value='enfants exploits sexuellement'>enfants exploits sexuellement</option>
            <option value='enfants marchands vendeurs'>enfants marchands vendeurs</option>
            <option value='enfants en conflit avec la loi'>enfants en conflit avec la loi</option>
            <option value='autres'>autres</option>
            <option value='enfants victimes de la traite et du trafic'>enfants victimes de la traite et du trafic</option>
            <option value='enfants affects par la violence arme'>enfants affects par la violence arme</option>
          </select>
          """.decode('utf-8').format(record[2])
          html_string += select

        elif record[0] == "my_element14":
          select = """
          {0}: <select name='my_element14'>
            <option value="">Select one</option>
            <option value='autres'>autres</option>
            <option value='bailleur international'>bailleur international</option>
            <option value='leve de fonds'>leve de fonds</option>
            <option value='bailleur priv veuillez ne pas citer de nom'>bailleur priv veuillez ne pas citer de nom</option>
            <option value='prive'>prive</option>
            <option value='cotisations de membres'>cotisations de membres</option>
            <option value='gouvernement ministre'>gouvernement ministre</option>
            <option value='services payants'>services payants</option>
            <option value='structure religieuse'>structure religieuse</option>
          </select>
          """.decode('utf-8').format(record[2])
          html_string += select

        elif record[0] == "quel_endroit":
          select = """
          {0}: <select name='quel_endroit'>
            <option value="">Select one</option>
            <option value='autres'>autres</option>
            <option value='universit dtat dhati ueh'>universit dtat dhati ueh</option>
            <option value='universit prive'>universit prive</option>
            <option value='formation non formelle'>formation non formelle</option>
          </select>
          """.decode('utf-8').format(record[2])
          html_string += select

        elif record[0] == "les_principaux":
          select = """
          {0}: <select name='les_principaux'>
            <option value="">Select one</option>
            <option value='dpression'>dpression</option>
            <option value='troubles des apprentissages'>troubles des apprentissages</option>
            <option value='retard de dveloppement psychomoteur'>retard de dveloppement psychomoteur</option>
            <option value='troubles de comportements'>troubles de comportements</option>
            <option value='troubles de personnalittroubles de personnalit'>troubles de personnalit</option>
            <option value='dficience mentale'>dficience mentale</option>
            <option value='folie'>folie</option>
            <option value='maltraitance'>maltraitance</option>
            <option value='agression sexuelle'>agression sexuelle</option>
            <option value='counseling larv'>counseling larv</option>
            <option value='counseling prposttest vih'>counseling prposttest vih</option>
            <option value='autres'>autres</option>
          </select>
          """.decode('utf-8').format(record[2])
          html_string += select

        elif record[0] == "types_de_thrapie":
          select = """
          {0}: <select name='types_de_thrapie'>
            <option value="">Select one</option>
            <option value='activits psychosociales'>activits psychosociales</option>
            <option value='activits socioculturelles'>activits socioculturelles</option>
            <option value='psychoducation'>psychoducation</option>
            <option value='thrapie cognitive et comportementale'>thrapie cognitive et comportementale</option>
            <option value='accompagnement psychosocial'>accompagnement psychosocial</option>
            <option value='club denfants'>club denfants</option>
            <option value='groupe dentraide'>groupe dentraide</option>
            <option value='autres'>autres</option>
            <option value='psychanalyse'>psychanalyse</option>
            <option value='musicothrapie'>musicothrapie</option>
            <option value='thrapie corporelle'>thrapie corporelle</option>
            <option value='thrapie par le thtre'>thrapie par le thtre</option>
            <option value='mdication'>mdication</option>
          </select>
          """.decode('utf-8').format(record[2])
          html_string += select



        else:
          html_string += "{0}: <select name='{1}'><option value=''>Choose Value</option></select>".format(record[2], record[0])
      elif record[0] in TEXTAREAS: 
        html_string += "{0}: <textarea name='{1}' cols=40 rows=6></textarea>".format(record[2], record[0])
      else:
        html_string += "{0}: <input name='{1}' type='text' />".format(record[2], record[0])
  html_string += "When do your services end: <input name='services_fin' type='text' />"
  return html_string


  
