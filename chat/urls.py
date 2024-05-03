from django.urls import path
from . import views

urlpatterns = [
    # Inne ścieżki URL
    path('chat/', views.chat_room, name='chat_room'),
]
