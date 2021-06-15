from django.contrib import admin

# Register your models here.
from productimporter.products.models import Product


@admin.register(Product)
class OrganizationReviewEventAdmin(admin.ModelAdmin):
    search_fields = ('name', 'sku', 'description')
    list_filter = ('active',)
