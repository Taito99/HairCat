from rest_framework import serializers
from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'user', 'pets']  # Dodajemy pola first_name, last_name, user, pets
        extra_kwargs = {'user': {'write_only': True}}  # Pole user będzie zapisywane ja

    def create(self, validated_data):
        pets_data = validated_data.pop('pets', [])  # Usuwamy pets z validated_data i przechowujemy je tymczasowo
        profile = Profile.objects.create(**validated_data)  # Tworzymy profil na podstawie pozostałych danych
        profile.pets.set(pets_data)  # Ustawiamy relację z zwierzętami
        return profile
