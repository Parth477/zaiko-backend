from django.db import models
from supplier.models import Supplier


class Category(models.Model):

    category_name = models.CharField(max_length=120)

    # created datetime
    created_at = models.DateTimeField(auto_now_add=True)

    # modified datetime
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'category'


class Product(models.Model):

    product_name = models.CharField(max_length=120)

    product_description = models.TextField()

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    unit_in_stock = models.IntegerField()

    product_sell_amount = models.FloatField()

    product_cost_amount = models.FloatField()

    # created datetime
    created_at = models.DateTimeField(auto_now_add=True)

    # modified datetime
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product'
