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

    # Pobierz listę kontaktów w zależności od roli użytkownika
    if request.user.is_staff:
        # Jeśli użytkownik jest administratorem, pobierz listę wszystkich użytkowników
        contacts = CustomUser.objects.exclude(id=request.user.id)
    else:
        # W przeciwnym razie, pobierz listę administratorów
        contacts = CustomUser.objects.filter(is_staff=True)

    chosen_contact = request.GET.get('receiver')

    if chosen_contact:
        # Jeśli został wybrany kontakt, przekieruj użytkownika do nowej strony z czatem
        return redirect('chat_with_contact', receiver_id=chosen_contact)

    return render(request, 'chat/chat_room.html', {'contacts': contacts, 'chosen_contact': None})


@login_required
def chat_with_contact(request, receiver_id):
    # Pobierz kontakt na podstawie ID odbiorcy
    receiver = CustomUser.objects.get(id=receiver_id)

    # Pobierz wszystkie wiadomości między aktualnym użytkownikiem a wybranym użytkownikiem
    sender_messages = Message.objects.filter(sender=request.user, receiver=receiver).order_by('timestamp')
    receiver_messages = Message.objects.filter(sender=receiver, receiver=request.user).order_by('timestamp')

    # Połącz oba zbiory wiadomości i posortuj je według czasu
    messages = list(sender_messages) + list(receiver_messages)
    messages.sort(key=lambda x: x.timestamp)

    # Utwórz listę osób, z którymi ostatnio pisał użytkownik/administrator
    last_contacts = []
    for message in messages:
        if message.sender != request.user and message.sender not in last_contacts:
            last_contacts.append(message.sender)
        elif message.receiver != request.user and message.receiver not in last_contacts:
            last_contacts.append(message.receiver)

    # Wyświetlaj nazwę użytkownika/administratora, który wysłał ostatnią wiadomość, aby użytkownik mógł szybko zidentyfikować
    # Ostatnia wiadomość będzie wiadomością z najnowszym znacznikiem czasu
    last_message = messages[-1] if messages else None
    last_sender = last_message.sender if last_message else None

    # Sprawdź, czy są jakieś nieprzeczytane wiadomości
    unread_messages = Message.objects.filter(receiver=request.user, is_read=False)

    return render(request, 'chat/chat_with_contact.html',
                  {'receiver': receiver, 'messages': messages, 'last_sender': last_sender,
                   'unread_messages': unread_messages})
