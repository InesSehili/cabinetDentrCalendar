
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include  # add this
from patients.views import ajouter_patient, liste_patient, archiver_patient, afficher_detail_patient, liste_patient_archiver, supprimer_patient, desarchiver_patient, supprimer_patient, liste_patient_payees, liste_patient_non_payees
from rdvs.views import liste_rdv, modifier_rdv, ajouter_rdv, confirmer_rdv, ajouter_patient_from_rdv, supprimer_rdv, list_rdv_toDay, list_rdv_week, list_rdv_month, ajouter_rdv_formulaire
from consultations.views import  ajouter_consultation, modifier_prix_consultation,  modifier_consultation, liste_consultation, formulaire_creation_consultation, liste_consultation_non_payees, liste_consultation_patient, supprimer_consultation, liste_consultation_payees, liste_consultation_patient_payees, liste_consultation_patient_non_payees
from fichesMedical.views import modifier_fiche_medical, modifier_contenu_fiche_medical, formulaire_creation_fiche_medical, liste_fiche_medical, ajouter_fiche_medical, supprimer_fiche_medical, afficher_fiche_medical
from diagnostiques.views import ajouter_diagnostique, afficher_diagnostique, formulaire_creation_diagnostique,  modifier_diagnostique_formulaire, supprimer_diagnostique
from medicaments.views import ajouter_medicament, liste_medicament, supprimer_medicament, modifier_medicament_formulaire, modifier_medicament
from radios.views import ajouter_radio, formulaire_ajout_radio, liste_radio, supprimer_radio,  afficher_radio_patient, afficher_radio
from traitements.views import formulaire_creation_traitement, ajouter_traitement, valider_traitement, annuler_traitement, supprimer_traitement
from payements.views import formulaire_creation_payement, ajouter_payement
from fournisseurs.views import ajouter_fournisseur, statistique, liste_fournisseur, supprimer_fournisseur
from achats.views import ajouter_achat, fourmulaire_ajout_achat, formulaire_payer_achat, payer_achat, supprimer_achat, imprimer_bon_commande, valider_bon_commande
from ordonances.views import formulaire_creation_ordonance, ajouter_ordonance, view_pdf, liste_ordonance, list_medicament_ordonance, supprimer_ordonance
from depenses.views import ajouter_depense, formulaire_ajouter_depense, supprimer_depense, formulaire_ajouter_depense_employee
from employes.views import ajouter_employee, liste_employe, supprimer_employe
from django.contrib.auth.decorators import login_required

from typerdvs.views import formulaire_ajout_type_rdv, ajouter_type_rdv, supprimer_type_rdv

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin route afficher_fiche_medical/
    path('customers/', include("customers.urls")),  # Django customers route
    path('', include('cal.urls')),
    path("", include("app.urls")),  # UI Kits Html files
    path("", include("authentication.urls")),  # Auth routes - login / register liste_consultation_patient
    path('ajouter_patient', ajouter_patient, name="ajouter_patient"),
    path('patients',liste_patient, name="patients"),
    path('rdvs', liste_rdv, name="rdvs"),
    path('ajouter_rdv', ajouter_rdv, name="ajouter_rdv"),
    path(r'^modifier_rdv/(?P<event_id>\d+)/$', modifier_rdv, name="modifier_rdv"),
    path('confirmer_rdv',confirmer_rdv, name="confirmer_rdv"),
    path('ajouter_patients_rdv',ajouter_patient_from_rdv, name="ajouter_patients_rdv"),
    path('archiver_patient',archiver_patient, name="archiver_patient"),
    path('supprimer_rdv',supprimer_rdv, name="supprimer_rdv"),
    path('afficher_detail_patient',afficher_detail_patient, name="afficher_detail_patient"),
    path('ajouter_consultation',ajouter_consultation, name="ajouter_consultation"),
    path('consultations',liste_consultation, name="consultations"),
    path('formulaire_creation_consultation',formulaire_creation_consultation, name='formulaire_creation_consultation'),
    path('liste_consultation_patient',liste_consultation_patient, name='liste_consultation_patient'),
    path('supprimer_consultation',supprimer_consultation, name='supprimer_consultation'),
    path('consultations_payees',liste_consultation_payees, name="consultations_payees"),
    path('liste_consultation_non_payees',liste_consultation_non_payees, name="liste_consultation_non_payees"),
    path('modifier_consultation',modifier_consultation, name="modifier_consultation"),
    path('modifier_prix_consultation',modifier_prix_consultation,name="modifier_prix_consultation"),
    path('formulaire_creation_fiche_medical',formulaire_creation_fiche_medical, name='formulaire_creation_fiche_medical'),
    path('fiches_medical',liste_fiche_medical, name='fiches_medical'),
    path('ajouter_fiche_medical',ajouter_fiche_medical, name="ajouter_fiche_medical"),
    path('supprimer_fiche_medical',supprimer_fiche_medical, name="supprimer_fiche_medical"),
    path('afficher_fiche_medical',afficher_fiche_medical, name='afficher_fiche_medical'),
    path('modifier_contenu_fiche_medical',modifier_contenu_fiche_medical, name="modifier_contenu_fiche_medical"),
    path('modifier_fiche_medical',modifier_fiche_medical, name="modifier_fiche_medical"),
    path('ajouter_diagnostique',ajouter_diagnostique, name="ajouter_diagnostique"),
    path('formulaire_creation_diagnostique',formulaire_creation_diagnostique, name="formulaire_creation_diagnostique"),
    path('liste_patient_archiver',liste_patient_archiver, name="liste_patient_archiver"),
    path('supprimer_patient/',supprimer_patient),
    path('desarchiver_patient',desarchiver_patient, name="desarchiver_patient"),
    path('afficher_diagnostique',afficher_diagnostique, name="afficher_diagnostique"),
    path('medicaments',liste_medicament, name="medicaments"),
    path('ajouter_medicaments',ajouter_medicament, name="ajouter_medicaments"),
    path('supprimer_medicament',supprimer_medicament, name="supprimer_medicament"),
    path('modifier_medicament_formulaire',modifier_medicament_formulaire, name="modifier_medicament_formulaire"),
    path('modifier_medicament',modifier_medicament, name="modifier_medicament"),
    path('formulaire_creation_ordonance',formulaire_creation_ordonance, name="formulaire_creation_ordonance"),
    path('ajouter_ordonance',ajouter_ordonance, name="ajouter_ordonance"),
    path('view_pdf',view_pdf, name="view_pdf"),
    path('liste_ordonance',liste_ordonance, name="liste_ordonance"),
    path('list_medicament_ordonance', list_medicament_ordonance, name="list_medicament_ordonance"),
    path('liste_consultation_patient_payees', liste_consultation_patient_payees, name="liste_consultation_patient_payees"),
    path('liste_consultation_patient_non_payees', liste_consultation_patient_non_payees, name="liste_consultation_patient_non_payees"),
    path('modifier_diagnostique_formulaire',  modifier_diagnostique_formulaire, name="modifier_diagnostique_formulaire"),
    path('list_rdv_toDay', list_rdv_toDay, name="list_rdv_toDay"),
    #list_rdv_week, list_rdv_month, formulaire_ajout_radio, lition_traitement
    path('list_rdv_week', list_rdv_week, name="list_rdv_week"),
    path('list_rdv_month', list_rdv_month, name="list_rdv_month"),
    path('supprimer_ordonance', supprimer_ordonance, name="supprimer_ordonance"),
    path('ajouter_radio', ajouter_radio, name="ajouter_radio"),
    path('formulaire_ajout_radio', formulaire_ajout_radio, name="formulaire_ajout_radio"),
    path('liste_radio', liste_radio, name="liste_radio"),
    path('supprimer_radio', supprimer_radio, name="supprimer_radio"),
    path('afficher_radio_patient', afficher_radio_patient, name="afficher_radio_patient"),
    #ajouter_traitement, valider_traitement, afficher_radio
    path('formulaire_creation_traitement', formulaire_creation_traitement, name="formulaire_creation_traitement"),
    path('ajouter_traitement', ajouter_traitement, name="ajouter_traitement"),
    path('valider_traitement', valider_traitement, name="valider_traitement"),
    path('annuler_traitement', annuler_traitement, name="annuler_traitement"),
    path('afficher_radio', afficher_radio, name="afficher_radio"),
    path('formulaire_creation_payement', formulaire_creation_payement, name="formulaire_creation_payement"),
    path('ajouter_payement', ajouter_payement, name="ajouter_payement"),
    path('ajouter_fournisseur', ajouter_fournisseur, name="ajouter_fournisseur"),
    path('statistique', statistique, name="statistique"),
    path('fourmulaire_ajout_achat', fourmulaire_ajout_achat, name="fourmulaire_ajout_achat"),
    path('ajouter_achat', ajouter_achat, name="ajouter_achat"),
    path('formulaire_payer_achat', formulaire_payer_achat, name="formulaire_payer_achat"),
    path('payer_achat', payer_achat, name="payer_achat"),
    path('supprimer_patient', supprimer_patient, name="supprimer_patient"),
    path('supprimer_diagnostique', supprimer_diagnostique, name="supprimer_diagnostique"),
    path('ajouter_depense', ajouter_depense, name="ajouter_depense"),
    path('formulaire_ajouter_depense', formulaire_ajouter_depense, name="formulaire_ajouter_depense"),
    path('supprimer_depense', supprimer_depense, name="supprimer_depense"),
    path('supprimer_achat', supprimer_achat, name="supprimer_achat"),
    path('ajouter_employee', ajouter_employee, name="ajouter_employee"),
    #formulaire_ajouter_depense
    path('formulaire_ajouter_depense_employee', formulaire_ajouter_depense_employee, name="formulaire_ajouter_depense_employee"),
    path('liste_patient_non_payees', liste_patient_non_payees, name="liste_patient_non_payees"),
    path('liste_patient_payees', liste_patient_payees, name="liste_patient_payees"),
    path('liste_fournisseur', liste_fournisseur, name="liste_fournisseur"),
    path('imprimer_bon_commande', imprimer_bon_commande, name="imprimer_bon_commande"),
    path('valider_bon_commande', valider_bon_commande, name="valider_bon_commande"),
    path('liste_employe', liste_employe, name="liste_employe"),
    path('supprimer_employe', supprimer_employe, name="supprimer_employe"),
    path('supprimer_fournisseur', supprimer_fournisseur, name="supprimer_fournisseur"),
    path('supprimer_traitement', supprimer_traitement, name="supprimer_traitement"),
    path('formulaire_ajout_type_rdv', formulaire_ajout_type_rdv, name="formulaire_ajout_type_rdv"),
    path('ajouter_type_rdv', ajouter_type_rdv, name="ajouter_type_rdv"),
    path('ajouter_rdv_formulaire', ajouter_rdv_formulaire, name="ajouter_rdv_formulaire"),
    path('supprimer_type_rdv', supprimer_type_rdv, name="supprimer_type_rdv"),

    


 


    
]

if settings.DEVEL:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
