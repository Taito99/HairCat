from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from users.models import CustomUser
from .models import Chat  # Make sure to import the Chat model correctly


class ChatSerializer(serializers.ModelSerializer):
    specialist_id = serializers.IntegerField(write_only=True)  # Accept specialist_id as input

    class Meta:
        model = Chat
        fields = ['id', 'participants', 'specialist_id']
        extra_kwargs = {
            'participants': {'read_only': True},
        }

    def create(self, validated_data):
        specialist_id = validated_data.pop('specialist_id')
        request_user = self.context['request'].user

        specialist = CustomUser.objects.get(id=specialist_id)  # Proper error handling should be done here

        with transaction.atomic():  # Use atomic to ensure db integrity
            chat = Chat.objects.create()
            chat.participants.add(request_user, specialist)
            chat.save()

        return chat
