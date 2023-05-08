from django.contrib import admin
from .models import Candidate , Company ,Vessel, Experience,Rank,Grade, Port, PortAgent, Hospital, DocumentType, Vendors, Profile, OfficeDocument,CountryName

# Register your models here.
admin.site.register(Candidate)
admin.site.register(Company)
admin.site.register(Vessel)
admin.site.register(Experience)
admin.site.register(Rank)
admin.site.register(Grade)
admin.site.register(Port)
admin.site.register(PortAgent)
admin.site.register(Hospital)
admin.site.register(DocumentType)
admin.site.register(Vendors)
admin.site.register(Profile)
admin.site.register(OfficeDocument)
admin.site.register(CountryName)
#admin.site.register(CarAdmin)
