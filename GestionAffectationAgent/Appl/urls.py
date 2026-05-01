from django.urls import path
from .views import *
from . import views

urlpatterns = [
    # Pages principales
    path('', chargAccueil),
    path('Rapp',chargRapport),
    path('Accc',chargAcceuilInsc),

    path('Service', chargService),
    path('ListeAgent/', views.liste_agents, name='liste_agents'),
    path('Ag', inserer_agent),
    path('inscription/', chargInscr),
    path('Poste', chargPoste),
    # Actions POST (modifier, supprimer, affecter)
    path('modifier/<int:id_agent>/', views.modifier_agent, name='modifier_agent'),
    path('supprimer/<int:id_agent>/', views.supprimer_agent, name='supprimer_agent'),
    path('affecter/<int:id_agent>/', views.affecter_agent, name='affecter_agent'),
    # APIs pour AJAX
    path('api/agents/', views.api_agents, name='api_agents'),
    path('api/agent/<int:id_agent>/', views.api_agent_detail, name='api_agent_detail'),
    path('api/services/', views.api_services, name='api_services'),
    path('api/postes/', views.api_postes, name='api_postes'),
    path('api/affectation/<int:id_agent>/', views.api_affectation_agent, name='api_affectation_agent'),
    path('desaffecter/<int:id>/', views.desaffecter_agent, name='desaffecter_agent'),
    #service
    path('services/', views.service_list_view, name='service_list'),
    # Endpoints API (utilisés par le JavaScript fetch)
    path('api/services/', views.api_services, name='api_services'),
    path('ajouter-service/', views.ajouter_service, name='ajouter_service'),
    path('modifier-service/<int:pk>/', views.modifier_service, name='modifier_service'),
    path('supprimer-service/<int:pk>/', views.supprimer_service, name='supprimer_service'),
    # API pour charger les données
    path('api/postes/', views.api_liste_postes, name='api_liste_postes'),
    # Actions CRUD
    path('ajouter-poste/', views.ajouter_poste, name='ajouter_poste'),
    path('modifier-poste/<int:pk>/', views.modifier_poste, name='modifier_poste'),
    path('supprimer-poste/<int:pk>/', views.supprimer_poste, name='supprimer_poste'),
    #creation compte
    path('lo',chargLogin),
    path('los', chargLogin, name='login'),
    path('util',connectUtilisateur),
    path('accAdmin',chargAccueilAdmin),
    path('inscrUtili',chargInscrUtilisateur),

    path('Rapp', chargRapport),  # Déjà dans votre urls.py


]