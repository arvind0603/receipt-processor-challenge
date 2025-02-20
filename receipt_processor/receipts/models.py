from django.db import models
import uuid

# Create your models here.
class Receipt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  #PK
    retailer = models.CharField(max_length=255)  
    purchase_date = models.DateField()
    purchase_time = models.TimeField()
    items = models.JSONField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    points = models.IntegerField(default=0)

class Item(models.Model):
    short_description = models.CharField(max_length=200)
    price = models.FloatField()