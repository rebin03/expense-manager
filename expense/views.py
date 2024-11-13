from django.shortcuts import render, redirect
from django.views.generic import View
from expense.forms import SignUpForm, SignInForm, ExpenseForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.


class SignUpView(View):
    
    template_name = 'signup_signin.html'
    form_class = SignUpForm
    
    def get(self, request, *args, **kwargs):
        
        form = self.form_class()
        
        return render(request, self.template_name, {'form':form})
    
    def post(self, request, *args, **kwargs):
        
        form_data = request.POST
        form = self.form_class(form_data)
        
        if form.is_valid():
            
            form.save()
            return redirect('signup')
        

class SignInView(View):
    
    template_name = 'signup_signin.html'
    form_class = SignInForm
    
    def get(self, request, *args, **kwargs):
        
        form = self.form_class()
        
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        
        user_obj = authenticate(request, username=uname, password=pwd)
        
        if user_obj:
            
            login(request, user_obj)
            return redirect('signin')
        
        
class indexView(View):
    
    template_name = 'index.html'
    
    def get(self, request, *args, **kwargs):
        
        
        return render(request, self.template_name)