from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Pets, UserPet
from .serializers import PetsSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_pet(request):
    if isinstance(request.data, list):
        serializer = PetsSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = PetsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pet_detail(request, pk):
    pet = get_object_or_404(Pets, pk=pk)

    if pet.owner == request.user or request.user.pets.filter(pk=pet.pk).exists():
        serializer = PetsSerializer(pet)
        return Response(serializer.data)
    else:
        return Response({"detail": "You do not have permission to view this pet."},
                        status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_pet(request, pk):
    if request.method == 'GET':
        pet = get_object_or_404(Pets, pk=pk)
        if pet.owner != request.user:
            return Response({"detail": "You do not have permission to view this pet."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = PetsSerializer(pet)
        return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_pet(request, pk):
    if request.method == 'PUT':
        pet = get_object_or_404(Pets, pk=pk)
        serializer = PetsSerializer(pet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_pet(request, pk):
    if request.method == 'DELETE':
        pet = get_object_or_404(Pets, pk=pk)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_pet_to_profile(request):
    if request.method == 'POST':
        user = request.user
        pet_id = request.data.get('pet_id')  # Id zwierzęcia, które użytkownik chce dodać

        # Sprawdzenie, czy podane zwierzę istnieje
        try:
            pet = Pets.objects.get(id=pet_id)
        except Pets.DoesNotExist:
            return Response({"detail": "Podane zwierzę nie istnieje."}, status=status.HTTP_400_BAD_REQUEST)

        # Sprawdzenie, czy użytkownik już nie posiada tego zwierzęcia w swoim profilu
        if UserPet.objects.filter(user=user, pet=pet).exists():
            return Response({"detail": "To zwierzę jest już przypisane do twojego profilu."}, status=status.HTTP_400_BAD_REQUEST)

        # Tworzenie powiązania między użytkownikiem a zwierzęciem
        UserPet.objects.create(user=user, pet=pet)
        return Response({"detail": "Zwierzę zostało dodane do twojego profilu."}, status=status.HTTP_201_CREATED)
