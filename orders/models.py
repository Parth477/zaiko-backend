from django.db import models
from users.models import Users
from product.models import Product


# Create your models here.

class Orders(models.Model):
    customer = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.FloatField()
    total_amount = models.FloatField()
    order_date = models.DateField()
    shipping_date = models.DateField()
    shipping_address = models.TextField()

    class Meta:
        db_table = 'orders'
