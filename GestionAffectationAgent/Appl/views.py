from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Agent, Affectation, Service, Poste
from django.contrib import messages
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm # Import important
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q




#Appelation du formulaire de login pour se connecter
def chargLogin(request):
    return render(request, "Appl/login.html")

#Appelation du formulaire de rapport par filtrage
def chargRapport(request):
    return render(request, "Appl/agents_par_service.html")

#CONNEXION lors de l'authentification
def connectUtilisateur(request):
    username=request.POST["txtUt"]
    password=request.POST["txtMot"]
    user=authenticate(request,username=username,password=password)
    if user is not None:
        login(request,user)
        return redirect("/Appl/accAdmin")
    else:
        messages.success(request,("Le compte est inexistant"))
        return redirect("/Appl/lo")


# Appelation de la page accueil
def chargAccueil(request):
    return render(request, "Appl/Accueil.html")
@login_required
#Appelation de la page accueil de l'administrateur après l'authentification
def chargAccueilAdmin(request):
    return render(request, "Appl/AccueilAdmin.html")

@login_required
#Appellation de la page de service
def chargService(request):
    return render(request, "Appl/Service.html")
@login_required
#Appellation de la page de poste
def chargPoste(request):
    return render(request, "Appl/ListePoste.html")
@login_required
#Appellation de la page liste des agents pour la gestion de agents
def liste_agents(request):
    return render(request, 'Appl/liste_agents.html')
@login_required
#Appellation de la page de inscription pour que l'administrateur enregistre un agent
def chargInscr(request):
    return render(request, "Appl/inscription_agent.html")
#Appellation de la page de inscription pour que l'agent s'inscrit seul
def chargInscrUtilisateur(request):
    return render(request, "Appl/inscriptionUtilisateur.html")
#Fonction d'insertion d'agent
def inserer_agent(request):
    if request.method == 'POST':
        try:
            agent = Agent(
                nom=request.POST.get('nom', '').upper(),
                postnom=request.POST.get('postnom', '').upper(),
                prenom=request.POST.get('prenom', '').capitalize(),
                sexe=request.POST.get('sexe', ''),
                lieuNais=request.POST.get('lieuNais', '').upper(),
                dateNais=request.POST.get('dateNais', ''),
                Quartier=request.POST.get('Quartier', '').capitalize(),
                Avenu=request.POST.get('Avenu', '').capitalize()
            )
            agent.save()

            # On ajoute le message dans le framework de Django
            messages.success(request, f" enregistré avec succès ✅")
            
            # TRÈS IMPORTANT : On redirige pour recharger la page et afficher le Toast
            return redirect("/Appl/inscription/") # Ou l'URL correspondante à cette vue

        except Exception as e:
            messages.error(request, f"Erreur lors de l'enregistrement : {e}")
            return render(request, "Appl/inscription_agent.html")
#Fonction de modification d'agent
def modifier_agent(request, id_agent):
    agent = get_object_or_404(Agent, id=id_agent)

    if request.method == 'POST':
        agent.nom = request.POST.get('nom', '').upper()
        agent.postnom = request.POST.get('postnom', '').upper()
        agent.prenom = request.POST.get('prenom', '').capitalize()
        agent.sexe = request.POST.get('sexe', '')
        agent.lieuNais = request.POST.get('lieuNais', '').upper()
        agent.dateNais = request.POST.get('dateNais', '')
        agent.Quartier = request.POST.get('Quartier', '').capitalize()
        agent.Avenu = request.POST.get('Avenu', '').capitalize()
        agent.save()

        return JsonResponse({
            'success': True,
            'message': f'Agent "{agent.prenom} {agent.nom}" modifié avec succès ✅'
        })

    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'}, status=405)
#Fonction de la suppression d'agent
def supprimer_agent(request, id_agent):
    agent = get_object_or_404(Agent, id=id_agent)
    nom_complet = f"{agent.prenom} {agent.nom}"

    if request.method == 'POST':
        affectations = Affectation.objects.filter(Ag=agent)

        if affectations.exists():
            return JsonResponse({
                'success': False,
                'message': f'Impossible de supprimer "{nom_complet}" car il a {affectations.count()} affectation(s) ❌'
            })

        agent.delete()

        return JsonResponse({
            'success': True,
            'message': f'Agent "{nom_complet}" supprimé avec succès 🗑️'
        })

    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'}, status=405)

#Fonction d'affectation des agents
def affecter_agent(request, id_agent):
    agent = get_object_or_404(Agent, id=id_agent)

    if request.method == 'POST':
        service_id = request.POST.get('service')
        poste_id = request.POST.get('poste')

        if not service_id or not poste_id:
            return JsonResponse({
                'success': False,
                'message': 'Veuillez sélectionner un service et un poste ❌'
            })

        service = get_object_or_404(Service, id=service_id)
        poste = get_object_or_404(Poste, id=poste_id)

        affectation_existante = Affectation.objects.filter(Ag=agent).first()

        if affectation_existante:
            affectation_existante.Se = service
            affectation_existante.Po = poste
            affectation_existante.save()

            return JsonResponse({
                'success': True,
                'message': f'Affectation de "{agent.prenom} {agent.nom}" modifiée avec succès 🔄'
            })

        else:
            Affectation.objects.create(Ag=agent, Se=service, Po=poste)

            return JsonResponse({
                'success': True,
                'message': f'Agent "{agent.prenom} {agent.nom}" affecté avec succès 🤝'
            })

    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'}, status=405)


def api_agents(request):
    agents = Agent.objects.all().order_by('-id')
    agents_affectes_ids = Affectation.objects.values_list('Ag_id', flat=True).distinct()

    data = {'agents': []}

    for agent in agents:
        data['agents'].append({
            'id': agent.id,
            'nom': agent.nom,
            'postnom': agent.postnom,
            'prenom': agent.prenom,
            'sexe': agent.sexe,
            'lieuNais': agent.lieuNais,
            'dateNais': agent.dateNais.strftime('%d/%m/%Y'),
            'Quartier': agent.Quartier,
            'Avenu': agent.Avenu,
            'est_affecte': agent.id in agents_affectes_ids
        })

    return JsonResponse(data)


def api_agent_detail(request, id_agent):
    agent = get_object_or_404(Agent, id=id_agent)

    return JsonResponse({
        'id': agent.id,
        'nom': agent.nom,
        'postnom': agent.postnom,
        'prenom': agent.prenom,
        'sexe': agent.sexe,
        'lieuNais': agent.lieuNais,
        'dateNais': agent.dateNais.strftime('%Y-%m-%d'),
        'Quartier': agent.Quartier,
        'Avenu': agent.Avenu
    })


def api_services(request):
    services = Service.objects.all().values('id', 'NomService')
    return JsonResponse(list(services), safe=False)


def api_postes(request):
    postes = Poste.objects.all().values('id', 'Designation')
    return JsonResponse(list(postes), safe=False)


def api_affectation_agent(request, id_agent):
    affect = Affectation.objects.filter(Ag_id=id_agent).first()

    if affect:
        return JsonResponse({
            'service_id': affect.Se_id,
            'poste_id': affect.Po_id
        })

    return JsonResponse({})

#Fonction de desaffectation d'agent
def desaffecter_agent(request, id):
    if request.method == 'POST':
        try:
            # 1. On récupère l'agent par son ID
            agent_obj = Agent.objects.get(id=id)
            
            # 2. On cherche toutes les affectations liées à cet agent
            # Attention : dans ton modèle, la clé étrangère s'appelle 'Ag'
            affectations = Affectation.objects.filter(Ag=agent_obj)
            
            if affectations.exists():
                count = affectations.count()
                affectations.delete() # On supprime le lien (désaffectation)
                return JsonResponse({
                    'success': True, 
                    'message': f'L\'agent {agent_obj.nom} a été libéré ({count} affectation(s) supprimée(s)). Il peut maintenant être supprimé. ✅'
                })
            else:
                return JsonResponse({
                    'success': False, 
                    'message': 'Cet agent n\'a aucune affectation active.'
                })

        except Agent.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Agent introuvable.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erreur : {str(e)}'})

    return JsonResponse({'success': False, 'message': 'Méthode non autorisée.'})


def service_list_view(request):
    return render(request, 'Appl/votre_page_service.html')

# 2. API pour charger les services en JSON
def api_services(request):
    services = list(Service.objects.values('id', 'NomService', 'Designation'))
    return JsonResponse(services, safe=False)

# Fonction d'ajout de service
def ajouter_service(request):
    if request.method == 'POST':
        nom = request.POST.get('NomService')
        designation = request.POST.get('Designation')
        if nom:
            service = Service.objects.create(NomService=nom, Designation=designation)
            return JsonResponse({'success': True, 'message': 'Service créé avec succès !'})
    return JsonResponse({'success': False, 'message': 'Données invalides'}, status=400)

# fonction Modifier un service
def modifier_service(request, pk):
    if request.method == 'POST':
        service = get_object_or_404(Service, pk=pk)
        service.NomService = request.POST.get('NomService')
        service.Designation = request.POST.get('Designation')
        service.save()
        return JsonResponse({'success': True, 'message': 'Service mis à jour !'})
    return JsonResponse({'success': False, 'message': 'Erreur'}, status=400)

# Fonction Supprimer un service
def supprimer_service(request, pk):
    if request.method == 'POST':
        service = get_object_or_404(Service, pk=pk)
        service.delete()
        return JsonResponse({'success': True, 'message': 'Service supprimé avec succès.'})
    return JsonResponse({'success': False, 'message': 'Erreur'}, status=400)

def api_liste_postes(request):
    postes = list(Poste.objects.all().values('id', 'Designation'))
    return JsonResponse(postes, safe=False)

# Fonction Ajouter un poste
def ajouter_poste(request):
    if request.method == 'POST':
        designation = request.POST.get('Designation')
        if designation:
            Poste.objects.create(Designation=designation)
            return JsonResponse({'success': True, 'message': 'Poste ajouté avec succès !'})
    return JsonResponse({'success': False, 'message': 'Erreur lors de l\'ajout.'})

# Fonction Modifier un poste
def modifier_poste(request, pk):
    poste = get_object_or_404(Poste, pk=pk)
    if request.method == 'POST':
        designation = request.POST.get('Designation')
        if designation:
            poste.Designation = designation
            poste.save()
            return JsonResponse({'success': True, 'message': 'Poste modifié avec succès !'})
    return JsonResponse({'success': False, 'message': 'Erreur lors de la modification.'})

# Fonction Supprimer un poste
def supprimer_poste(request, pk):
    poste = get_object_or_404(Poste, pk=pk)
    if request.method == 'POST':
        poste.delete()
        return JsonResponse({'success': True, 'message': 'Poste supprimé définitivement.'})
    return JsonResponse({'success': False, 'message': 'Erreur lors de la suppression.'})


#RAPPORTfrom django.shortcuts import render
def liste_agents_par_service(request):
    """Affiche la liste des agents filtrés par service"""
    
    # Récupérer tous les services
    services = Service.objects.all()
    
    # Initialisation des variables
    agents_list = []
    selected_service = None
    
    # Vérifier si un service a été sélectionné
    service_id = request.GET.get('service')
    
    if service_id:
        try:
            # Récupérer le service sélectionné
            selected_service = Service.objects.get(id=service_id)
            
            # Récupérer toutes les affectations de ce service
            affectations = Affectation.objects.filter(
                Se=selected_service
            ).select_related('Ag', 'Po')
            
            # Construire la liste des agents avec leurs postes
            for affectation in affectations:
                agents_list.append({
                    'agent': affectation.Ag,
                    'poste': affectation.Po,
                    'affectation_id': affectation.id,
                })
        except Service.DoesNotExist:
            pass
    
    # Contexte pour le template
    context = {
        'services': services,
        'selected_service': selected_service,
        'agents_list': agents_list,
        'total_agents': len(agents_list),
    }
    
    return render(request, 'agents_par_service.html', context)


