from django.urls import path
from . import views

urlpatterns = [
    # Ścieżka do widoku czatu
    path('chat/', views.chat_room, name='chat_room'),
    # Ścieżka do widoku czatu z konkretnym użytkownikiem
    path('chat/<int:receiver_id>/', views.chat_with_contact, name='chat_with_contact'),
    path('chatcreate/', views.create_chat, name='chat'),
]
