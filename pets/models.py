from django.db import models


class Pets(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    breed = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/', default='default/no_image_available.jpg')

    def __str__(self):
        return self.name
