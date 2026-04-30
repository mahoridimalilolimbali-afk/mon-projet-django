from django.db import models

# Create your models here.
class Agent(models.Model):
    nom=models.CharField(max_length=50)
    postnom=models.CharField(max_length=50)
    prenom=models.CharField(max_length=50)
    sexe=models.CharField(max_length=13)
    lieuNais=models.CharField(max_length=30)
    dateNais=models.DateField()
    Quartier=models.CharField(max_length=50)
    Avenu=models.CharField(max_length=50)

class Service(models.Model):
    NomService=models.CharField(max_length=50)
    Designation=models.CharField(max_length=50)

class Poste(models.Model):
    Designation=models.CharField(max_length=50)

class Affectation(models.Model):
    Ag=models.ForeignKey(Agent, on_delete=models.CASCADE)
    Se=models.ForeignKey(Service, on_delete=models.CASCADE)
    Po=models.ForeignKey(Poste, on_delete=models.CASCADE)
