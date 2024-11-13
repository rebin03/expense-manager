from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    
    phone = models.CharField(max_length=10, unique=True)
    


class Expense(models.Model):
    
    PAYMENT_CHOICES = (
        ('card', 'Card'),
        ('cash', 'Cash'),
        ('upi', 'UPI')
    )
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    amount = models.FloatField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.title