from django.db import models

# Create your models here.


class Supplier(models.Model):

    supplier_name = models.CharField(max_length=120)

    supplier_office_address = models.TextField()

    supplier_phone_number = models.CharField(max_length=10)

    # created datetime
    created_at = models.DateTimeField(auto_now_add=True)

    # modified datetime
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'supplier'
