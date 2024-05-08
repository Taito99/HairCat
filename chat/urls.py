from django.urls import path
from . import views

urlpatterns = [
    # Ścieżka do widoku czatu z konkretnym użytkownikiem
    path('chatcreate/', views.create_chat, name='chat'),
    path('chats/', views.user_chats_list, name='chatlist'),
    path('chats/<uuid:chat_id>/messages/', views.chat_messages, name='chat-messages'),


]
