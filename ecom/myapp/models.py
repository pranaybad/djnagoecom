from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Product(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(max_length=300)
    image = models.ImageField(upload_to='media/', default='products/default.jpg')  
    price=models.IntegerField(default=0)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to Django User model
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to Product model
    quantity = models.PositiveIntegerField(default=1)  