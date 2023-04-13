from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat, Message
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
import base64
import json
from channels.layers import InMemoryChannelLayer

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

        if text_data_json['type'] == 'text':
            dict_message = await self.create_text_message(
                text_data=text_data_json['content']
            )
            await self.channel_layer.group_send(
                self.chat_group_name,
                {
                    'type': 'text_message',
                    'content': dict_message
                }
            )

        elif text_data_json['type'] == 'image':
            dict_message = await self.create_image_message(
                image_code=text_data_json['content']                
            )
            await self.channel_layer.group_send(
                self.chat_group_name,
                {
                    'type': 'image_message',
                    'content': dict_message
                }
            )

        elif text_data_json['type'] == 'get_member_count':
            mc = await self.get_group_member_count()
            
            await self.channel_layer.group_send(
                self.chat_group_name,
                {
                    'type': 'member_count_message',
                    'content': mc
                }
            )
            

    async def text_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def image_message(self, event):
        await self.send(text_data=json.dumps(event))
        
    async def member_count_message(self, event):
        await self.send(text_data=json.dumps(event))


    @database_sync_to_async
    def create_text_message(self, text_data: str) -> dict:
        try:
            chat = Chat.objects.get(pk=self.chat)
            receiver = User.objects.get(pk=self.receiver)
            message = Message.objects.create(
                chat=chat,
                sender=self.scope['user'],
                receiver=receiver,
                text=text_data,
            )

            return message.to_dict()

        except Exception as e:
            print(f'Message create error {e}')

    @database_sync_to_async
    def create_image_message(self, image_code) -> dict:
        chat = Chat.objects.get(pk=self.chat)
        receiver = User.objects.get(pk=self.receiver)

        message = Message.objects.create(
            chat=chat,
            sender=self.scope['user'],
            receiver=receiver,
        )

        format, imgstr = image_code.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{message.pk}_image.{ext}')
        message.image.save(f'{message.pk}_image.{ext}', data)

        return message.to_dict()


    async def disconnect(self, close_code):
        print(f'Disconnected {close_code}')

    @database_sync_to_async
    def get_receiver(self):
        chat = Chat.objects.get(pk=self.chat)
        return int(chat.u1.pk if chat.u1 != self.scope['user'] else chat.u2.pk)

    async def get_group_member_count(self: InMemoryChannelLayer):
        
        # group_channels = await self.channel_layer(f'chat_{self.chat}').as_asgi()
        # member_count = len(group_channels)
        # print(member_count)
        return 1