from django.shortcuts import redirect, render
from django.views.generic import View

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


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
    
    
    def post(self, requets):        
        return render(requets, 'accounts/login.html')
        