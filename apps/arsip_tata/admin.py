from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Year)
admin.site.register(models.Box)
admin.site.register(models.Bundle)
admin.site.register(models.Item)
admin.site.register(models.Customer)

# class ItemsAdmin(admin.ModelAdmin):
#     # readonly_fields = ('created_by',)
#     # list_display = ('title', 'created_by')
#     exclude = ['added_by',]
#     def save_model(self, request, obj, form, change):
#         obj.created_by = request.user
#         super().save_model(request, obj, form, change)

# admin.site.register(models.Item, ItemsAdmin)
