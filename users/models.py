from django.db import models
from django.contrib.auth.models import AbstractUser
from pets.models import Pets


class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True, verbose_name="Birth Date")
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Address")
    city = models.CharField(max_length=255, null=True, blank=True, verbose_name="City")
    phone_number = models.CharField(max_length=9, null=False, blank=False, verbose_name="Phone")
    pets = models.ManyToManyField(Pets, related_name='owners')

    def __str__(self):
        return self.username
