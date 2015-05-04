# -*- coding: utf-8 -*- 
import os
import json
import MySQLdb
from models import SearchRecord
import unicodedata
from helpers import QueryHandler
from models import Audit
### Same general idea should work for edit

### Then Delete

### All three models

### After is roles


ATTRIBUTES =  ['id_1', 'informations_generales', '1_nom', 'departement', 'commune', 'section_communale', 'adresse', 'gps_location', 'latitude', 'longitude', 'boite_postale', 'telephone', 'personne_contact', 'email', 'site_web', '1_estce_que_votre', '3_connaissezvous', '3a', '3b', '3c', '3d', '4estce_que_votre', '4a_comment_publicisezvous', '4b_estce_que_vos', '5_ces_services', '6_recevezvous_des', '6_type_plusieurs', '6a_precisez_autre', '6b_autre_organisation', '6c_statut', '6d_autre_status', '7_jour', '7_preciser_lales', '7a_heure', '8_objectifs_fondamentaux', '8_pouvezvous_decrire', '8a_quel_est_le', '8b1_precisez_', '8c_offrezvous_des', '8c1_medication', '8c2_activites_psychosociales', '8c3_accompagnement', '8c4_psychanalyse', '8c5_musicotherapie', '8c6_club_denfants', '8c7_activites_socioculturelles', '8c8_groupe_dentraide', '8c9_psychoeducation', '8c10_therapie_corporelle', '8c11_therapie_cognitive', '8c12_therapie_par', '8c13_autres', '9_source_de_financement', '9a_lequel_t', '9b_autre_source', '10_comment_votre', '9a_combien', '9c_precisez', '10_que_faitesvous', '10a_si_vous_referez', '11_quelle_categorie', '11_pouvezvous_dire', '11a_dechanges_de', '11b_de_referencement', '11c_de_formation', '11d_autres', '13_quels_sont_les', 'combien_13', 'autre_assistance13', '14_quels_obstacles', '14a_si_autres_', '15_quels_obstacles', '16_connaissezvous', '_17_tranche_dge', '_18_tranche_dge', '19_quel_est_le', '20_etesvous_en', '21_comment_lorganisation', '21a_citez_5_defis', '21b_citez_5_lecons', '23_connaissezvous', '23a_noms_des_oganisation', '23b_citez_les_services', '23c_si_oui_lesquels', 'quels_sont_les', 'question_a', 'question_b', 'question_c', 'question_d', 'created_date', 'created_by', 'created_location', 'created_device_id', 'modified_date', 'modified_by', 'modified_location', 'modified_device_id', 'server_modified', 'quand_votre_service', 'quand_estce_que', 'votre_organisation', 'si_oui_prciser', 'catgories_denfants', 'my_element14', 'quel_endroit', 'les_principaux', 'services_fin']

REQUIRED_ATTRIBUTES = ["1_nom"]

def get_int(string):
	try:
		return int(string)
	except:
		# change to an error later
		return 0

def get_float(string):
	try:
		return float(string)
	except:
		return 0.0

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
	return self.request.get(name)

def get_attributes(self):
	data = {}
	for attr in ATTRIBUTES:
		data[attr] = get_request(self, attr)
	return data

def populate_sql_statement(data):
	sql_statement = """
		INSERT INTO `organization` SET
		`id` = NULL,
		`is_deleted` = 0,
		`id_1` = '{0}',
		`informations_generales` = '{1}',
		`1_nom` = '{2}',
		`departement` = '{3}',
		`commune` = '{4}',
		`section_communale` = '{5}',
		`adresse` = '{6}',
		`gps_location` = '{7}',
		`latitude` = '{8}',
		`longitude` = '{9}',
		`boite_postale` = '{10}',
		`telephone` = '{11}',
		`personne_contact` = '{12}',
		`email` = '{13}',
		`site_web` = '{14}',
		`1_estce_que_votre` = '{15}',
		`3_connaissezvous` = '{16}',
		`3a` = '{17}',
		`3b` = '{18}',
		`3c` = '{19}',
		`3d` = '{20}',
		`4estce_que_votre` = '{21}',
		`4a_comment_publicisezvous` = '{22}',
		`4b_estce_que_vos` = '{23}',
		`5_ces_services` = '{24}',
		`6_recevezvous_des` = '{25}',
		`6_type_plusieurs` = '{26}',
		`6a_precisez_autre` = '{27}',
		`6b_autre_organisation` = '{28}',
		`6c_statut` = '{29}',
		`6d_autre_status` = '{30}',
		`7_jour` = '{31}',
		`7_preciser_lales` = '{32}',
		`7a_heure` = '{33}',
		`8_objectifs_fondamentaux` = '{34}',
		`8_pouvezvous_decrire` = '{35}',
		`8a_quel_est_le` = '{36}',
		`8b1_precisez_` = '{37}',
		`8c_offrezvous_des` = '{38}',
		`8c1_medication` = '{39}',
		`8c2_activites_psychosociales` = '{40}',
		`8c3_accompagnement` = '{41}',
		`8c4_psychanalyse` = '{42}',
		`8c5_musicotherapie` = '{43}',
		`8c6_club_denfants` = '{44}',
		`8c7_activites_socioculturelles` = '{45}',
		`8c8_groupe_dentraide` = '{46}',
		`8c9_psychoeducation` = '{47}',
		`8c10_therapie_corporelle` = '{48}',
		`8c11_therapie_cognitive` = '{49}',
		`8c12_therapie_par` = '{50}',
		`8c13_autres` = '{51}',
		`9_source_de_financement` = '{52}',
		`9a_lequel_t` = '{53}',
		`9b_autre_source` = '{54}',
		`10_comment_votre` = '{55}',
		`9a_combien` = '{56}',
		`9c_precisez` = '{57}',
		`10_que_faitesvous` = '{58}',
		`10a_si_vous_referez` = '{59}',
		`11_quelle_categorie` = '{60}',
		`11_pouvezvous_dire` = '{61}',
		`11a_dechanges_de` = '{62}',
		`11b_de_referencement` = '{63}',
		`11c_de_formation` = '{64}',
		`11d_autres` = '{65}',
		`13_quels_sont_les` = '{66}',
		`combien_13` = '{67}',
		`autre_assistance13` = '{68}',
		`14_quels_obstacles` = '{69}',
		`14a_si_autres_` = '{70}',
		`15_quels_obstacles` = '{71}',
		`16_connaissezvous` = '{72}',
		`_17_tranche_dge` = '{73}',
		`_18_tranche_dge` = '{74}',
		`19_quel_est_le` = '{75}',
		`20_etesvous_en` = '{76}',
		`21_comment_lorganisation` = '{77}',
		`21a_citez_5_defis` = '{78}',
		`21b_citez_5_lecons` = '{79}',
		`23_connaissezvous` = '{80}',
		`23a_noms_des_oganisation` = '{81}',
		`23b_citez_les_services` = '{82}',
		`23c_si_oui_lesquels` = '{83}',
		`quels_sont_les` = '{84}',
		`question_a` = '{85}',
		`question_b` = '{86}',
		`question_c` = '{87}',
		`question_d` = '{88}',
		`created_date` = CURRENT_TIMESTAMP(),
		`created_by` = '{90}',
		`created_location` = '{91}',
		`created_device_id` = '{92}',
		`modified_date` = CURRENT_TIMESTAMP(),
		`modified_by` = '{93}',
		`modified_location` = '{94}',
		`modified_device_id` = '{95}',
		`server_modified` = CURRENT_TIMESTAMP(),
		`quand_votre_service` = '{98}',
		`quand_estce_que` = '{99}',
		`votre_organisation` = '{100}',
		`si_oui_prciser` = '{101}',
		`catgories_denfants` = '{102}',
		`my_element14` = '{103}',
		`quel_endroit` = '{104}',
		`les_principaux` = '{105}',
		`services_fin` = '{106}';
		""".format(get_int(data['id_1']), data['informations_generales'], data['1_nom'], data['departement'], data['commune'], data['section_communale'], data['adresse'], data['gps_location'], get_float(data['latitude']), get_float(data['longitude']), data['boite_postale'], data['telephone'], data['personne_contact'], data['email'], data['site_web'], data['1_estce_que_votre'], data['3_connaissezvous'], data['3a'], data['3b'], data['3c'], data['3d'], data['4estce_que_votre'], data['4a_comment_publicisezvous'], data['4b_estce_que_vos'], data['5_ces_services'], data['6_recevezvous_des'], data['6_type_plusieurs'], data['6a_precisez_autre'], data['6b_autre_organisation'], data['6c_statut'], data['6d_autre_status'], data['7_jour'], data['7_preciser_lales'], data['7a_heure'], data['8_objectifs_fondamentaux'], data['8_pouvezvous_decrire'], data['8a_quel_est_le'], data['8b1_precisez_'], data['8c_offrezvous_des'], data['8c1_medication'], data['8c2_activites_psychosociales'], data['8c3_accompagnement'], data['8c4_psychanalyse'], data['8c5_musicotherapie'], data['8c6_club_denfants'], data['8c7_activites_socioculturelles'], data['8c8_groupe_dentraide'], data['8c9_psychoeducation'], data['8c10_therapie_corporelle'], data['8c11_therapie_cognitive'], data['8c12_therapie_par'], data['8c13_autres'], data['9_source_de_financement'], data['9a_lequel_t'], data['9b_autre_source'], data['10_comment_votre'], data['9a_combien'], data['9c_precisez'], data['10_que_faitesvous'], data['10a_si_vous_referez'], data['11_quelle_categorie'], data['11_pouvezvous_dire'], data['11a_dechanges_de'], data['11b_de_referencement'], data['11c_de_formation'], data['11d_autres'], data['13_quels_sont_les'], data['combien_13'], data['autre_assistance13'], data['14_quels_obstacles'], data['14a_si_autres_'], data['15_quels_obstacles'], data['16_connaissezvous'], data['_17_tranche_dge'], data['_18_tranche_dge'], data['19_quel_est_le'], data['20_etesvous_en'], data['21_comment_lorganisation'], data['21a_citez_5_defis'], data['21b_citez_5_lecons'], data['23_connaissezvous'], data['23a_noms_des_oganisation'], data['23b_citez_les_services'], data['23c_si_oui_lesquels'], data['quels_sont_les'], data['question_a'], data['question_b'], data['question_c'], data['question_d'], data['created_date'], data['created_by'], data['created_location'], data['created_device_id'], data['modified_date'], data['modified_by'], data['modified_location'], data['modified_device_id'], data['server_modified'], data['quand_votre_service'], data['quand_estce_que'], data['votre_organisation'], data['si_oui_prciser'], data['catgories_denfants'], data['my_element14'], data['quel_endroit'], data['les_principaux'], data['services_fin'])
	return sql_statement


def save_record(self):
	data = get_attributes(self)
	valid, errors = validate_attributes(data)
	sql_statement = populate_sql_statement(data)

	# raise Exception(sql_statement)
	record = QueryHandler.execute_query(sql_statement, insert=True)
	last_record_sql = "SELECT id FROM organization ORDER BY id DESC LIMIT 1;"

	last = QueryHandler.execute_query(last_record_sql)
	self.redirect("/records/{0}?message=Saved".format(last[0][0]))
	record_audit = Audit.save(initiated_by = self.session.get("user"), user_affected = data['1_nom'], security_clearance = self.session.get("role"), json_data = str(data), model= "Organization", action = "Create Organization")
	return 


