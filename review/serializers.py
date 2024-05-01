from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'content', 'timestamp', 'likes', 'dislikes']
        read_only_fields = ['id', 'user', 'timestamp']
