from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Chat(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username} at {self.timestamp}: {self.message}"
