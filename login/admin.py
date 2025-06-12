from django.contrib import admin
from .models import Panchayat, Household, Citizen, User, Land, Cultivationrecord, Asset, Welfareprogram, Application, Servicerequest, Vaccinationrecord, Censusevent, Censusparticipation

admin.site.register(Panchayat)
admin.site.register(Household)
admin.site.register(Citizen)
admin.site.register(User)
admin.site.register(Land)
admin.site.register(Cultivationrecord)
admin.site.register(Asset)
admin.site.register(Welfareprogram)
admin.site.register(Application)
admin.site.register(Servicerequest)
admin.site.register(Vaccinationrecord)
admin.site.register(Censusevent)
admin.site.register(Censusparticipation)