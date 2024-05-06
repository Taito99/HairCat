from django.db import models
from django.contrib.auth.models import User


class Pets(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    breed = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='pet_profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.name



class UserPet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pets, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s pet: {self.pet.name}"
