import uuid
from django.db import models

from django.contrib.auth.models import User


class Message(models.Model):
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
    text = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Receiver')
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.text
    
    def to_dict(self) -> dict:
        return {
            'chat_id' : f'{self.chat.pk}',
            'pk' : self.pk,
            'text': self.text,
            'sender' : self.sender.pk,
            'receiver' : self.receiver.pk,
            'date' : f'{self.date}'
        }
    
class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    u1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='u1')
    u2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='u2')
    
    def __str__(self) -> str:
        return f"{self.u1} * {self.u2}"

    