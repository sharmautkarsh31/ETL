from bulk_update_or_create import BulkUpdateOrCreateQuerySet
from django.db import models

# Create your models here.
class Product(models.Model):

    name = models.CharField(max_length=255)
    sku =  models.CharField(unique=True,max_length=255)
    description = models.TextField()
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sku

