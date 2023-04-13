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
    
    if request.method == 'POST':
        q = request.POST.get('q')
        u1 = request.user 
        
        try:
            user_object = User.objects.get(username=q)
        except User.DoesNotExist:
            user_object = None
            
        if user_object is not None and user_object != request.user:
            new_chat = Chat.objects.get_or_create(
                u1=u1,
                u2=user_object
            )
            
            return redirect('home')
    
    chats = Chat.objects.filter(Q(u1=request.user) | Q(u2=request.user))
    context = {
        'chats': chats,
    }
    return render(request, 'base.html', context)
    

@login_required(login_url='auth')
def chat(request, pk):   
    if request.method == 'POST':
        q = request.POST.get('q')
        u1 = request.user 
        
        try:
            user_object = User.objects.get(username=q)
        except User.DoesNotExist:
            user_object = None
            
        if user_object is not None and user_object != request.user:
            new_chat = Chat.objects.get_or_create(
                u1=u1,
                u2=user_object
            ) 
            
            return redirect('chat', pk=pk)
            
             
        
     
    chats: list[Chat] = Chat.objects.filter(Q(u1=request.user) | Q(u2=request.user))
    
    try:    
        chat: Chat = Chat.objects.get(pk=pk)
        messages: list[Message] = Message.objects.filter(chat=chat)
    except Exception as e:
        return redirect('home')       
    
    context = {
        'chats': chats,
        'chat' : chat,
        'messages': messages
    }
    return render(request, 'chat.html', context)
    

