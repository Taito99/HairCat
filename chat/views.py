from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Message, Chat
from .serializers import ChatSerializer, ChatListSerializer, MessageSerializer


@api_view(['POST'])
@login_required
def create_chat(request):
    serializer = ChatSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        chat = serializer.save()
        return Response(ChatSerializer(chat).data,
                        status=status.HTTP_201_CREATED)  # Serialize chat instance to include updated participants
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@login_required
def user_chats_list(request):
    # Get the current user from the request
    user = request.user
    # Filter chats where the current user is a participant
    chats = Chat.objects.filter(participants=user)
    # Serialize the data
    serializer = ChatListSerializer(chats, many=True)
    # Return the data
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@login_required
def chat_messages(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.method == 'GET':
        messages = Message.objects.filter(chat=chat)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MessageSerializer(data=request.data, context={'request': request, 'chat': chat})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
