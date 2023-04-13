from django.urls import path

from .views import *

urlpatterns = [
    path('auth/', auth, name='auth'),
    path('', home, name='home'),
    path('chat/<pk>/', chat, name='chat'),  
]

