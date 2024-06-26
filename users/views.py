from django.contrib.auth.views import PasswordResetView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import UserSerializer


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        print(request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = None

        if '@' in username:
            try:
                user = CustomUser.objects.get(username=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    if request.method == 'POST':
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        """
        If the form is valid, send a reset link to the user.
        """
        opts = {
            'use_https': self.request.is_secure(),
            'email_template_name': 'registration/password_reset_email.html',
            'subject_template_name': 'registration/password_reset_subject.txt',
            'request': self.request,
        }
        form.save(**opts)

        # Here, you can send additional response if needed
        return Response({"message": "Password reset email has been sent."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stuff_list(request):
    # Filtrujemy użytkowników, którzy mają is_stuff=True
    users = CustomUser.objects.filter(is_staff=True)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
