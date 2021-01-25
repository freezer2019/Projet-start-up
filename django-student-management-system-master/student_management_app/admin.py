from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Ministere, Policier, Commissaire, Commissariat, Ville, Region, District, Crime, Secteur, Quartier, Equipe_enquetrice, Delinquant


class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)

admin.site.register(Ministere)
admin.site.register(Policier)
admin.site.register(Commissaire)
admin.site.register(Commissariat)
admin.site.register(Ville)
admin.site.register(Region)
admin.site.register(District)
admin.site.register(Crime)
admin.site.register(Secteur)
admin.site.register(Quartier)
admin.site.register(Equipe_enquetrice)
admin.site.register(Delinquant)

