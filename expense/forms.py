from django import forms
from django.contrib.auth.forms import UserCreationForm
from expense.models import User, Expense

# user register form
class SignUpForm(UserCreationForm):
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control mb-3', 'placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control mb-3', 'placeholder':'Confirm Password'}))
    
    class Meta:
        
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone']
        
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Username'}),
            'email': forms.EmailInput(attrs={'class':'form-control mb-3', 'placeholder':'Email Address'}),
            'phone': forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Phone Number'})
        }
    
    
class SignInForm(forms.Form):
    
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mb-3'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control mb-3'}))
    
    
class ExpenseForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(ExpenseForm, self).__init__(*args, **kwargs)
    
    class Meta:
        
        model = Expense
        fields = ['title', 'category', 'amount', 'payment_method']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder':'Enter title'}),
            'category': forms.Select(attrs={'class': 'form-control form-select mb-3', 'placeholder':'Enter carogory'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder':'Enter amount'}),
            'payment_method': forms.Select(attrs={'class': 'form-control form-select mb-3'})
        }
        
        labels = {
            'title': '',
            'category': '',
            'amount': '',
            'payment_method': 'Select Payment Method'
        }
        
        