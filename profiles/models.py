from django.db import models
from users.models import CustomUser


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, verbose_name="First Name")
    last_name = models.CharField(max_length=100, blank=True, verbose_name="Last Name")
    pets = models.ManyToManyField('pets.Pets', related_name='owners_profile')

    def __str__(self):
        return f"Profile of {self.user.username}"
