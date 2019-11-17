from django.db import models
from river.models.fields.state import StateField


class Shipping(models.Model):
    product = models.CharField(max_length=50, null=True, blank=True)
    customer = models.CharField(max_length=50, null=True, blank=True)
    shipping_status = StateField()

    def __str__(self):
        return self.product
