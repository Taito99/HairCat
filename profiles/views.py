from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(user_profile)
        return Response(serializer.data)


@login_required
def user_profile(request):
    user_profile = Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': user_profile})
