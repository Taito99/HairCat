from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Pets
from .serializers import PetsSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_pet(request):
    # Uwaga: upewnij się, że żądanie jest obsługiwane jako multipart dla obrazów.
    serializer = PetsSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pet_detail(request, pk):
    pet = get_object_or_404(Pets, pk=pk)
    if request.user.pets.filter(pk=pet.pk).exists():
        serializer = PetsSerializer(pet)
        return Response(serializer.data)
    else:
        return Response({"detail": "You do not have permission to view this pet."},
                        status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_pets(request):
    pets = request.user.pets.all()
    serializer = PetsSerializer(pets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_pet(request, pk):
    pet = get_object_or_404(Pets, pk=pk)
    if not request.user.pets.filter(pk=pet.pk).exists():
        return Response({"detail": "You do not have permission to update this pet."},
                        status=status.HTTP_403_FORBIDDEN)
    serializer = PetsSerializer(pet, data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_pet(request, pk):
    pet = get_object_or_404(Pets, pk=pk)
    if not request.user.pets.filter(pk=pet.pk).exists():
        return Response({"detail": "You do not have permission to delete this pet."},
                        status=status.HTTP_403_FORBIDDEN)
    pet.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
