from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, verbose_name="First Name")
    last_name = models.CharField(max_length=100, blank=True, verbose_name="Last Name")
    pets = models.ManyToManyField('pets.Pets', related_name='owners', blank=True, verbose_name="Owned Pets")

    def __str__(self):
        return f"Profile of {self.user.username}"
