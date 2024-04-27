from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Pets
from .serializers import PetsSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_pet_list(request):
    if request.method == 'POST':
        serializer = PetsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pet_detail(request, pk):
    if request.method == 'GET':
        pet = get_object_or_404(Pets, pk=pk)
        if request.user.pets.filter(pk=pet.pk).exists():
            serializer = PetsSerializer(pet)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_pet_list(request):
    pets = request.user.pets.all()
    serializer = PetsSerializer(pets, many=True)
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
