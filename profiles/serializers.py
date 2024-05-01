from rest_framework import serializers
from profiles.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'user', 'pets']
        extra_kwargs = {'user': {'write_only': True}}

    def create(self, validated_data):
        pets_data = validated_data.pop('pets', [])
        profile = Profile.objects.create(**validated_data)
        profile.pets.set(pets_data)
        return profile

# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
