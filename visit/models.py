from django.db import models
from pets.models import Pets
from users.models import CustomUser


# Create your models here.
class Visit(models.Model):
    pet = models.ForeignKey(Pets, on_delete=models.CASCADE, related_name='visits')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='visits')
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} - {self.pet.name} - {self.owner.username}"
