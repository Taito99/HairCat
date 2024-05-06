from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'content', 'timestamp', 'likes', 'dislikes']
        read_only_fields = ['id', 'user', 'timestamp']  # Użytkownik i timestamp są tylko do odczytu

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user  # Dodajemy użytkownika z kontekstu
        return Review.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.likes = validated_data.get('likes', instance.likes)
        instance.dislikes = validated_data.get('dislikes', instance.dislikes)
        instance.save()
        return instance
