from django.db import models


class Pets(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    breed = models.CharField(max_length=50)

    def __str__(self):
        return self.name
