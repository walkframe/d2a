from django.contrib.gis import admin

from .models import Lake, Address

admin.site.register(Lake, admin.OSMGeoAdmin)
admin.site.register(Address, admin.OSMGeoAdmin)
