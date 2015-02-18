import datetime
from google.appengine.ext import ndb

class Record(ndb.Model):
  created_at = ndb.DateTimeProperty(required=True, auto_now_add=True)
  record_id = ndb.StringProperty(default="empty")
  parent_record_id = ndb.StringProperty(default="empty")
  parent_page_id = ndb.StringProperty(default="empty")
  parent_element_id = ndb.StringProperty(default="empty")
  created_date = ndb.StringProperty(default="empty")
  created_by = ndb.StringProperty(default="empty")
  created_location = ndb.StringProperty(default="empty")
  created_device_id = ndb.StringProperty(default="empty")
  modified_date = ndb.StringProperty(default="empty")
  modified_by = ndb.StringProperty(default="empty")
  modified_location = ndb.StringProperty(default="empty")
  modified_device_id = ndb.StringProperty(default="empty")
  server_modified_date = ndb.StringProperty(default="empty")
  si_autre_precisez_ = ndb.StringProperty(default="empty")
  soins_de_sant_communautaires_informels = ndb.StringProperty(default="empty")
  soins_de_sant_primaire = ndb.StringProperty(default="empty")
  si_oui_prciser__plusieurs_rponses_possibles = ndb.StringProperty(default="empty")
  soins_psychiatriques = ndb.StringProperty(default="empty")
  soins_psychologiques = ndb.StringProperty(default="empty")
  relation_daide = ndb.StringProperty(default="empty")
  counseling = ndb.StringProperty(default="empty")
  precisez2 = ndb.StringProperty(default="empty")
  autre_petita = ndb.StringProperty(default="empty")
  preciser_autres = ndb.StringProperty(default="empty")
  sant_communautaires = ndb.StringProperty(default="empty")
  santprimaire2 = ndb.StringProperty(default="empty")
  soins_de_counseling = ndb.StringProperty(default="empty")

  soins_sante_psychologiques2 = ndb.StringProperty(default="empty")
  soins_santepsychiatriques3 = ndb.StringProperty(default="empty")
  grille_tarifaire_relation3 = ndb.StringProperty(default="empty")
  combien_mensuellement = ndb.StringProperty(default="empty")
  pour_quelles_raisons = ndb.StringProperty(default="empty")
  approx_precisez = ndb.StringProperty(default="empty")
  comment_publicisez = ndb.StringProperty(default="empty")
  precisez_autres2 = ndb.StringProperty(default="empty")
  a = ndb.StringProperty(default="empty")
  b = ndb.StringProperty(default="empty")
  c = ndb.StringProperty(default="empty")
  d = ndb.StringProperty(default="empty")
  otre_precisez = ndb.StringProperty(default="empty")
  catgories_denfants_vulnrables_que_vous_recevez = ndb.StringProperty(default="empty")
  autre_categorie = ndb.StringProperty(default="empty")
  dcrire_les_catgories_dintervenants_ = ndb.StringProperty(default="empty")
  autre_categorie_intervenants = ndb.StringProperty(default="empty")
  autres_categories_precisez = ndb.StringProperty(default="empty")
  endroits_formation_precisez_autres = ndb.StringProperty(default="empty")
  autres_endroit_de_suivi_formation = ndb.StringProperty(default="empty")
  quels_organismes_vous_rfrez_les_demandes = ndb.StringProperty(default="empty")
  organisme_relation_de_formation = ndb.StringProperty(default="empty")
  organisme_relation_dchanges_de_pratique = ndb.StringProperty(default="empty")
  autres_organismes_relations = ndb.StringProperty(default="empty")
  obstacles_rencontre_dispensation_services = ndb.StringProperty(default="empty")
  autres_obstacles_precisez = ndb.StringProperty(default="empty")
  obstacles_rencontre_par_patients = ndb.StringProperty(default="empty")
  si_oui_savezvous_pourquoi = ndb.StringProperty(default="empty")

  demandes_pas_de_specialites = ndb.StringProperty(default="empty")
  connaissezvous_gens_communaute_formation_academik = ndb.StringProperty(default="empty")
  estce_que_votre_organisation_offre_des_services_en_sant_men = ndb.StringProperty(default="empty")
  sant_communautaires_informels = ndb.StringProperty(default="empty")
  sant_primaire = ndb.StringProperty(default="empty")
  counseling2 = ndb.StringProperty(default="empty")
  soins_psychologiques2 = ndb.StringProperty(default="empty")
  psychiatriques2 = ndb.StringProperty(default="empty")
  nombres_de_demandes = ndb.StringProperty(default="empty")
  relation_daide2 = ndb.StringProperty(default="empty")
  c_estce_que_les_services_sont_gratuits__ = ndb.StringProperty(default="empty")
  approximation_de_la_distance = ndb.StringProperty(default="empty")
  refuser_des_demandes = ndb.StringProperty(default="empty")
  autre_centre_offrant_des_services = ndb.StringProperty(default="empty")
  recevezvous_des_enfants_vulnrables_ou_leurs_parents = ndb.StringProperty(default="empty")
  formations_en_sant_mentale_amliorer_comptences = ndb.StringProperty(default="empty")
  nombre_intervenants_travaillant = ndb.StringProperty(default="empty")

  commune = ndb.StringProperty(default="empty")
  departement = ndb.StringProperty(default="empty")
  adresse = ndb.StringProperty(default="empty")
  nom_de_lorganisation = ndb.StringProperty(default="empty")
  gps_ = ndb.StringProperty(default="empty")
  telephone = ndb.StringProperty(default="empty")
  personne_de_contact = ndb.StringProperty(default="empty")
  email = ndb.StringProperty(default="empty")
  site_web = ndb.StringProperty(default="empty")

  type_plusieurs_rponses_possibles = ndb.StringProperty(default="empty")
  statut = ndb.StringProperty(default="empty")
  jour = ndb.StringProperty(default="empty")
  heure = ndb.StringProperty(default="empty")
  precisez_autres_sources_financements = ndb.StringProperty(default="empty")
  my_element14 = ndb.StringProperty(default="empty")
  precisez_type_organisme = ndb.StringProperty(default="empty")
  source_de_financement = ndb.StringProperty(default="empty")
  niveau_de_formation_intervenants = ndb.StringProperty(default="empty")
  quel_endroit = ndb.StringProperty(default="empty")
  autre_status = ndb.StringProperty(default="empty")
  les_principaux_motifs_de_consultation_plusieurs_rponses_possib = ndb.StringProperty(default="empty")
  preciser_autres_motifs_consultation = ndb.StringProperty(default="empty")
  types_de_thrapie_utiliss_plusieurs_rponses_possibles = ndb.StringProperty(default="empty")
  si_autres_precisez_types_de_therapie = ndb.StringProperty(default="empty")
  globalement__combien_estimezvous_le_cot_annuel_de_ces_servic = ndb.StringProperty(default="empty")
  prcisez_leur_groupe_dge = ndb.StringProperty(default="empty")

  services_sontils_disponibles_pour_les_enfants_vulnrables = ndb.StringProperty(default="empty")
  activits_socioculturelles = ndb.StringProperty(default="empty")
  mdication = ndb.StringProperty(default="empty")
  activits_psychosociales = ndb.StringProperty(default="empty")
  psychanalyse = ndb.StringProperty(default="empty")
  accompagnement_psychosocial = ndb.StringProperty(default="empty")
  musicothrapie = ndb.StringProperty(default="empty")
  club_denfants = ndb.StringProperty(default="empty")
  niveau_de_formation_intervenants = ndb.StringProperty(default="empty")
  psychoducation = ndb.StringProperty(default="empty")
  thrapie_par_le_thtre = ndb.StringProperty(default="empty")
  thrapie_corporelle = ndb.StringProperty(default="empty")
  thrapie_cognitive_et_comportementale = ndb.StringProperty(default="empty")
  autres = ndb.StringProperty(default="empty")
  si_vous_referez_precisez_ou = ndb.StringProperty(default="empty")
  quels_sont_les_organismes_qui_vous_rfrent_des_demandes_ = ndb.StringProperty(default="empty")
  de_rfrencement = ndb.StringProperty(default="empty")

  votre_organisation_offre_des_services_de_types_psychosociaux = ndb.StringProperty(default="empty")
  si_oui_preciser_types_de_services_psycho = ndb.StringProperty(default="empty")
  precisez_autres_types_services_psycho = ndb.StringProperty(default="empty")
  connaissezvous_centre_offrant_des_services_sante = ndb.StringProperty(default="empty")
  question_a = ndb.StringProperty(default="empty")
  question_b = ndb.StringProperty(default="empty")
  question_c = ndb.StringProperty(default="empty")
  question_d = ndb.StringProperty(default="empty")

  latitude = ndb.StringProperty(default="empty")
  longitude = ndb.StringProperty(default="empty")


def save():
  pass
