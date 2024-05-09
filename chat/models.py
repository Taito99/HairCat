import uuid

from django.db import models
from django.conf import settings

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_messages',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(
        'Chat',  # This is important, make sure this is correctly referencing the Chat model.
        related_name='messages',
        on_delete=models.CASCADE
    )
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Message from {self.sender.username} sent at {self.timestamp}'
class Chat(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chats', blank=True)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)

    def __str__(self):
        return f'Chat between {", ".join(str(participant) for participant in self.participants.all())}'

