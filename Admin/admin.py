from django.contrib import admin
from django.contrib.auth.models import Group
from . import models
# Register your models here.

admin.site.site_header = 'SVU HEALTH CENTER ADMIN PANEL'

class MainStock(admin.ModelAdmin):
    list_filter = ('RecievedFrom',)



admin.site.register(models.Invoice)
admin.site.register(models.TabDetails)
admin.site.register(models.AvailableStock)
admin.site.register(models.PharmacyIssuedStock)
admin.site.register(models.PharmacyAvailableStock)

