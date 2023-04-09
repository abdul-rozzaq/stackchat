from django.shortcuts import redirect, render
from django.views.generic import View

from django.contrib.auth.models import User
from django.contrib.auth import login, logout as lgt, authenticate, decorators


class RegisterView(View):
    def get(self,request):
        return render(request, 'accounts/register.html')
    
    
    def post(self, requets):        
        
        try:
            username = requets.POST.get('username')
            email = requets.POST.get('email')
            password = requets.POST.get('password')
            
            user = User.objects.create_user(username=username, email=email, password=password)
            login(requets, user)
            
            return redirect('home')
                    
        except Exception as e:
            print(f'Register error {str(e).strip()}')
        
        return render(requets, 'accounts/register.html')
        
        
class LoginView(View):
    def get(self,request):
        return render(request, 'accounts/login.html')
    
    
    def post(self, request):
        try:
            username = request.POST['username']
            password = request.POST['password']
            
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')
                
        except Exception as e:
            print(f'Login error {str(e).strip()}')
             
        return render(request, 'accounts/login.html')


@decorators.login_required(login_url='auth')
def logout(request):
    lgt(request)
    return redirect('login')