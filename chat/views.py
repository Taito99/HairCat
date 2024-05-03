from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from users.models import CustomUser  # Załóżmy, że CustomUser to model użytkownika w Twojej aplikacji

@login_required
def chat_room(request):
    if request.method == 'POST':
        # Obsługa wysłania nowej wiadomości
        sender = request.user
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('content')
        receiver = CustomUser.objects.get(id=receiver_id)
        # Zapisz nową wiadomość
        Message.objects.create(sender=sender, receiver=receiver, content=content)
        # Przekieruj z powrotem do widoku czatu
        return redirect('chat_room')

    # Pobierz wszystkie wiadomości, gdzie aktualny użytkownik jest nadawcą lub odbiorcą
    messages_sent = Message.objects.filter(sender=request.user).order_by('timestamp')
    messages_received = Message.objects.filter(receiver=request.user).order_by('timestamp')

    # Połącz oba zbiory wiadomości i posortuj je według czasu
    messages = list(messages_sent) + list(messages_received)
    messages.sort(key=lambda x: x.timestamp)

    # Wyświetlaj nazwę użytkownika/administratora, który wysłał ostatnią wiadomość, aby użytkownik mógł szybko zidentyfikować
    # Ostatnia wiadomość będzie wiadomością z najnowszym znacznikiem czasu
    last_message = messages[-1] if messages else None
    last_sender = last_message.sender if last_message else None

    # Sprawdź, czy są jakieś nieprzeczytane wiadomości
    unread_messages = Message.objects.filter(receiver=request.user, is_read=False)

    return render(request, 'chat/chat_room.html', {'messages': messages, 'last_sender': last_sender, 'unread_messages': unread_messages})
