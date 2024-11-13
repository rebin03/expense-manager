from django import forms
from django.contrib.auth.forms import UserCreationForm
from expense.models import User, Expense

# user register form
class SignUpForm(UserCreationForm):
    
    class Meta:
        
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone']
    
    
class SignInForm(forms.Form):
    
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    
    
class ExpenseForm(forms.ModelForm):
    
    class Meta:
        
        model = Expense
        fields = ['title', 'category', 'amount', 'payment_method']