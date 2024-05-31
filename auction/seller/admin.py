from django.contrib import admin

from .import models
# Register your models here.
admin.site.register(models.SellerModel)
admin.site.register(models.SellerProfileModel)
admin.site.register(models.Product)