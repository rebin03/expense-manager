from django.shortcuts import redirect

def signin_required(func):
    
    def wrapper(request, *args, **kwargs):
        
        if not request.user.is_authenticated:
            return redirect('signin')
        
        else:
            
            return func(request, *args, **kwargs)
        
    return wrapper