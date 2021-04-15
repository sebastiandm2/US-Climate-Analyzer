from django.contrib import admin
from .models import President, City, State, Country, Consistsof, Belongsto

# Register your models here.
admin.site.register(President)
admin.site.register(City)
admin.site.register(State)
admin.site.register(Country)
admin.site.register(Consistsof)
admin.site.register(Belongsto)

admin.site.site_header = "Backend of Climate Analyzer"