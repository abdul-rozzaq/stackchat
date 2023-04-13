from django.shortcuts import redirect, render
from django.views.generic import View

from django.contrib.auth.models import User
from django.contrib.auth import login as lgn, logout as lgt, authenticate, decorators


def login(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                lgn(request, user)
                return redirect('home')
            else:
                print('User not found')   
        except Exception as e:
            print(f'Login error {str(e).strip()}')
                
    return render(request, 'accounts/login.html')


def register(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
                        
            user = User.objects.create_user(username=username, email=email, password=password)
            
            lgn(request, user)
            
            return redirect('home')
                    
        except Exception as e:
            print(f'Register error {str(e).strip()}')
        
        return render(request, 'accounts/register.html')
        
        
    
    return render(request, 'accounts/register.html')


@decorators.login_required(login_url='auth')
def logout(request):
    lgt(request)
    return redirect('login')