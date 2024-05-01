from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Ustawienie wymagania autoryzacji

    def get(self, request):
        user_profile = Profile.objects.get(user=request.user)  # Pobranie profilu użytkownika zalogowanego
        serializer = ProfileSerializer(user_profile)  # Serializacja profilu
        return Response(serializer.data)

from django.shortcuts import render
from .models import Profile

def user_profile(request):
    user_profile = Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': user_profile})

