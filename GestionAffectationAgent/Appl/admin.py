from django.contrib import admin

# Register your models here.
from .models import Agent, Service, Poste, Affectation

class AgentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'postnom', 'prenom', 'sexe', 'lieuNais', 'dateNais')
    list_filter = ('sexe',)
    search_fields = ('nom', 'postnom', 'prenom')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('NomService', 'Designation')
    search_fields = ('NomService',)

class PosteAdmin(admin.ModelAdmin):
    list_display = ('Designation',)
    search_fields = ('Designation',)

class AffectationAdmin(admin.ModelAdmin):
    list_display = ('Ag', 'Se', 'Po')
    list_filter = ('Se', 'Po')
    search_fields = ('Ag__nom', 'Ag__postnom', 'Se__NomService')
    raw_id_fields = ('Ag', 'Se', 'Po')

admin.site.register(Agent, AgentAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Poste, PosteAdmin)
admin.site.register(Affectation, AffectationAdmin)