from rest_framework import serializers
from .models import Pets


class PetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pets
        fields = ['id', 'name', 'breed', 'age', 'owners']
        extra_kwargs = {'owners': {'read_only': True}}  # Ustaw 'owners' jako pole tylko do odczytu

    def create(self, validated_data):
        pet = Pets.objects.create(**validated_data)
        # Dodaj zalogowanego użytkownika jako właściciela
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            pet.owners.add(request.user)
        pet.save()
        return pet

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.breed = validated_data.get('breed', instance.breed)
        instance.age = validated_data.get('age', instance.age)
        instance.save()
        # Możesz również zaktualizować właścicieli, jeśli jest to wymagane
        return instance
