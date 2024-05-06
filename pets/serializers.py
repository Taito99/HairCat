from rest_framework import serializers
from .models import Pets


class PetsSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(max_length=None, allow_empty_file=True, allow_null=True, required=False)

    class Meta:
        model = Pets
        fields = ['id', 'name', 'breed', 'age', 'profile_picture']


    def create(self, validated_data):
        return Pets.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.breed = validated_data.get('breed', instance.breed)
        instance.age = validated_data.get('age', instance.age)
        instance.save()
        return instance
