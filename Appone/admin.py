from django.contrib import admin
from .models import ProductInventory , ContactUsForm

# Register your models here.
admin.site.register(ProductInventory)
admin.site.register(ContactUsForm)