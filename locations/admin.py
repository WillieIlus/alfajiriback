from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

from .models import Country, Location

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'code', 'flag')
    prepopulated_fields = {'slug': ('name',)}


class LocationAdmin(ImportExportModelAdmin):
    list_display = ('name', 'slug', 'country', 'flag')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Country, CountryAdmin)
admin.site.register(Location, LocationAdmin)

