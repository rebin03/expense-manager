from django.shortcuts import render, redirect
from django.views.generic import View
from expense.forms import SignUpForm, SignInForm, ExpenseForm
from django.contrib.auth import authenticate, login, logout
from expense.models import Expense
from expense.decorators import signin_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

# Create your views here.

decorators = [signin_required, never_cache]

@method_decorator(never_cache, name='dispatch')
class SignUpView(View):
    
    template_name = 'register.html'
    form_class = SignUpForm
    
    def get(self, request, *args, **kwargs):
        
        form = self.form_class()
        
        return render(request, self.template_name, {'form':form, 'action':'Signup'})
    
    def post(self, request, *args, **kwargs):
        
        form_data = request.POST
        form = self.form_class(form_data)
        
        if form.is_valid():
            
            form.save()
            return redirect('signin')
        
        return render(request, self.template_name, {'form':form, 'action':'Signup'})

@method_decorator(never_cache, name='dispatch')
class SignInView(View):
    
    template_name = 'login.html'
    form_class = SignInForm
    
    def get(self, request, *args, **kwargs):
        
        form = self.form_class()
        
        return render(request, self.template_name, {'form':form, 'action':'Signin'})

    def post(self, request, *args, **kwargs):
        
        form_data = request.POST
        form = self.form_class(form_data)
        
        if form.is_valid():
            
            data = form.cleaned_data
                    
            uname = data.get('username')
            pwd = data.get('password')
        
            user_obj = authenticate(request, username=uname, password=pwd)
            
            if user_obj:
                
                login(request, user_obj)
                return redirect('index')
        
        return render(request, self.template_name, {'form':form, 'action':'Signin'})

@method_decorator(decorators, name='dispatch')
class SignOutView(View):
    
    def get(self, request, *args, **kwargs):
        
        logout(request)
        return redirect('signin')
 
@method_decorator(decorators, name='dispatch')       
class indexView(View):
    
    template_name = 'index.html'
    form_class = ExpenseForm
    
    def get(self, request, *args, **kwargs):
        
        qs = Expense.objects.filter(owner=request.user.id)
        
        form = self.form_class()
        
        return render(request, self.template_name, {'form':form, 'data':qs})
    
    def post(self, request, *args, **kwargs):
        
        form_data = request.POST
        form = self.form_class(form_data)

        if form.is_valid():
            
            form.instance.owner = request.user
            form.save()
            return redirect('index')
        
        return render(request, self.template_name, {'form':form})
    
@method_decorator(decorators, name='dispatch')   
class ExpenceDeleteView(View):
    
    def get(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        Expense.objects.get(id=id).delete()
        return redirect('index')
    
@method_decorator(decorators, name='dispatch')
class ExpenseUpdateView(View):
    
    template_name = 'update.html'
    form_class = ExpenseForm
    
    def get(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        expense_obj = Expense.objects.get(id=id)
        form = self.form_class(instance=expense_obj)
        
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        
        form_data = request.POST
        id = kwargs.get('pk')
        expense_obj = Expense.objects.get(id=id)
        
        form = self.form_class(form_data, instance=expense_obj)
        
        if form.is_valid():
            
            form.instance.owner = request.user
            form.save()
            return redirect('index')
        
        return render(request, self.template_name, {'form':form})
