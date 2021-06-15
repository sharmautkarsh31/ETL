from django.contrib import admin

# Register your models here.
from productimporter.files_manager.models import FileItem


@admin.register(FileItem)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('user', 'name', 'path')
    list_filter = ('file_type','active','uploaded')
