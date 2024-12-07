from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    
    phone = models.CharField(max_length=10, unique=True)
    


class Expense(models.Model):
    
    PAYMENT_CHOICES = (
        (None, 'Select'),
        ('card', 'Card'),
        ('cash', 'Cash'),
        ('upi', 'UPI')
    )
    
    CATEGORY_CHOICES = (
        (None, 'Select'),
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('Entertainment', 'Entertainment'),
        ('Health Care', 'Health Care'),
        ('Housing', 'Housing'),
        ('Transportation', 'Transportation'),
        ('Education', 'Education'),
        ('Personal Care', 'Personal Care'),
        ('Debt Payments', 'Debt Payments'),
        ('Savings & Investments', 'Savings & Investments'),
        ('Gifts & Donations', 'Gifts & Donations'),
        ('Insurance', 'Insurance'),
        ('Miscellaneous', 'Miscellaneous'),
    )
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Select', null=False, blank=False)
    amount = models.FloatField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='Select', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.title
    
    