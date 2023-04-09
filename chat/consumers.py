import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat = self.scope["url_route"]["kwargs"]["pk"]
        self.receiver = await self.get_receiver()
        self.chat_group_name = f'chat_{self.chat}'
        
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        await self.accept()


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        dict_message = await self.create_message(
            text_data_json['message'],
        )
                
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': dict_message
            }
        )
        
        
    async def chat_message(self, event):
        print(event)
        await self.send(text_data=json.dumps(
            event['message']
        ))
    
    
    @database_sync_to_async
    def create_message(self, text_data):
        
        try:
            chat = Chat.objects.get(pk=self.chat)
            receiver = User.objects.get(pk=self.receiver)
                
            return Message.objects.create(chat=chat, sender=self.scope['user'], receiver=receiver, text=text_data).to_dict()
        except Exception as e:
            print(f'Error creating message {e}')
            
    
    @database_sync_to_async
    def get_receiver(self):
        chat = Chat.objects.get(pk=self.chat)
        return int(chat.u1.pk if chat.u1 != self.scope['user'] else chat.u2.pk)
    
    async def disconnect(self, close_code):
        print(f'Disconnected {close_code}')
