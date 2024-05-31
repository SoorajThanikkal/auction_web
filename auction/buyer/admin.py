from django.contrib import admin
from .import models

# Register your models here.

admin.site.register(models.BuyerModel)
admin.site.register(models.BuyerProfileModel)
admin.site.register(models.BuyerCart)
admin.site.register(models.Payment)
admin.site.register(models.Order)
