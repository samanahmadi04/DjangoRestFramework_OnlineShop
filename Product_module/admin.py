from django.contrib import admin
from . import models


# Register your models here.

class OptionFieldAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(models.ProductParentCategory)
admin.site.register(models.ProductCategory)
admin.site.register(models.Product)
admin.site.register(models.OptionField)
admin.site.register(models.ProductOption)
