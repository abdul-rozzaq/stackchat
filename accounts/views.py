from django.shortcuts import redirect, render
from django.views.generic import View


class RegisterView(View):
    def get(self,request):
        return render(request, 'accounts/register.html')
    
    
    def post(self, request):
        return render(request, 'accounts/register.html')
        
        
class LoginView(View):
    def get(self,request):
        return render(request, 'accounts/login.html')
    
    
    def post(self, request):
        return render(request, 'accounts/login.html')
        