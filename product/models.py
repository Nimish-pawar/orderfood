from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class ProductTable(models.Model):
   id=models.AutoField(primary_key=True)
   name=models.CharField(max_length=100)
   price=models.IntegerField()
   description=models.CharField(max_length=100)
   quantity=models.IntegerField()
   category=models.CharField(max_length=100)
   image=models.ImageField(upload_to='image')
   
   
class CartItem(models.Model):
    product = models.ForeignKey(ProductTable, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    
    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return self.name  


class Payment(models.Model):
    order_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id
