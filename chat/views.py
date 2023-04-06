from django.shortcuts import redirect, render

def auth(request):
    if not request.user.is_authenticated:       
        return render(request,'auth.html')
    
    else:
        return redirect('home')
        

def home(request):
    if not request.user.is_authenticated:       
        return redirect('auth')
    
    else:
        return render(request,'index.html')
    
