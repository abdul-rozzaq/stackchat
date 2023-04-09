from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Chat, Message

def auth(request):
    if not request.user.is_authenticated:
        return render(request, 'auth.html')
    else:
        return redirect('home')

@login_required(login_url='auth')
def home(request):    
    chats = Chat.objects.filter(Q(u1=request.user) | Q(u2=request.user))
    context = {
        'chats': chats,
    }
    return render(request, 'base.html', context)
    
    




@login_required(login_url='auth')
def chat(request, pk):    
    chats: list[Chat] = Chat.objects.filter(Q(u1=request.user) | Q(u2=request.user))
    chat: Chat = Chat.objects.get(pk=pk)
    messages: list[Message] = Message.objects.filter(chat=chat)
    
    
    context = {
        'chats': chats,
        'chat' : chat,
        'messages': messages
    }
    return render(request, 'chat.html', context)
    

