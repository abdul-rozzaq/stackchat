import uuid
from django.db import models
from django.contrib.auth.models import User
import base64

from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import base64

class Message(models.Model):
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='messages/images/', blank=True, null=True)
    text = models.TextField(null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Receiver')
    date = models.DateTimeField(auto_now_add=True)
    
    def to_dict(self) -> dict:
        data = {
            'chat_id' : f'{self.chat.pk}',
            'pk' : self.pk,
            'sender' : self.sender.pk,
            'receiver' : self.receiver.pk,
            'date' : f'{self.date}',
        }
        
        if self.text:
            data['text'] = self.text
        
        elif self.image:
            data['image'] = self.image.url
                
        return data


class Chat(models.Model):
    u1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='u1')
    u2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='u2')
    
    def __str__(self) -> str:
        return f"{self.u1} * {self.u2}"

    