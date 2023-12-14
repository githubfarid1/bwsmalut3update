from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Year)
admin.site.register(models.Box)
admin.site.register(models.Bundle)
admin.site.register(models.Item)
admin.site.register(models.Customer)
