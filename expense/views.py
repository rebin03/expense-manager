from django.shortcuts import render, redirect
from django.views.generic import View
from expense.forms import SignUpForm, SignInForm, ExpenseForm
from django.contrib.auth import authenticate, login, logout
from expense.models import Expense
from expense.decorators import signin_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.db.models import Sum
from django.db.models.functions import TruncMonth

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

@method_decorator(decorators, name='dispatch')
class ExpenseSummaryView(View):
    
    template_name = 'expense_summary.html'

    def get(self, request, *args, **kwargs):
        
        total_expense = Expense.objects.filter(owner=request.user).values('amount').aggregate(Sum('amount')).get('amount__sum')
        
        food_expense = Expense.objects.filter(category='Food', owner=request.user).values('amount').aggregate(Sum('amount')).get('amount__sum')
        travel_expense = Expense.objects.filter(category='Travel', owner=request.user).values('amount').aggregate(Sum('amount')).get('amount__sum')
        entertainment_expense = Expense.objects.filter(category='Entertainment', owner=request.user).values('amount').aggregate(Sum('amount')).get('amount__sum')
        health_expense = Expense.objects.filter(category='Health Care', owner=request.user).values('amount').aggregate(Sum('amount')).get('amount__sum')
        miscellaneous_expense = Expense.objects.filter(category='Miscellaneous', owner=request.user).values('amount').aggregate(Sum('amount')).get('amount__sum')
        
        category_expenses = [food_expense, travel_expense, entertainment_expense, health_expense, miscellaneous_expense]
        
        card_expense = Expense.objects.filter(payment_method='card', owner=request.user).values('amount').aggregate(Sum('amount')).get('amount__sum')
        cash_expense = Expense.objects.filter(payment_method='cash', owner=request.user).values('amount').aggregate(Sum('amount')).get('amount__sum')
        upi_expense = Expense.objects.filter(payment_method='upi', owner=request.user).values('amount').aggregate(Sum('amount')).get('amount__sum')
        
        payment_expenses = [card_expense, cash_expense, upi_expense]
        
        expense_obj = Expense.objects.get(id=1)
        print(expense_obj.created_at.strftime("%B"))
        
        monthly_expenses = Expense.objects.filter(owner=request.user).annotate(month=TruncMonth('created_at')).values('month').annotate(total=Sum('amount')).order_by('month')
        monthly_expenses_data = [expense['total'] for expense in monthly_expenses]
        print(monthly_expenses_data)
    
        context = {
            'total_expense':total_expense, 
            'category_expenses':category_expenses,
            'payment_expenses':payment_expenses,
            'monthly_expenses_data':monthly_expenses_data
        }
        
        return render(request, self.template_name, context)