from django.shortcuts import redirect, render
from django.views.generic import View

from django.contrib.auth.models import User


class RegisterView(View):
    def get(self,request):
        return render(request, 'accounts/register.html')
    
    
    def post(self, requets):        
        
        try:
            first_name = requets.POST.get('first-name')
            last_name = requets.POST.get('last-name')
            username = requets.POST.get('username')
            email = requets.POST.get('email')
            
            password = requets.POST.get('password')
             
            user = User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username)    
                        
        except Exception as e:
            print(f'Register error {str(e).strip()}')
        
        return render(requets, 'accounts/register.html')
        
        
class LoginView(View):
    def get(self,request):
        return render(request, 'accounts/login.html')
    
    
    def post(self, requets):
        
        
        return render(requets, 'accounts/login.html')
        