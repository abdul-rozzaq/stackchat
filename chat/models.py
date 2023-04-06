from django.db import models

from django.contrib.auth.models import User


class Message(models.Model):
    text = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Receiver')
    date = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return self.text
    
    