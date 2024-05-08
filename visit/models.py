from django.db import models
from django.conf import settings
from pets.models import Pets


class Visit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='visits')
    pet = models.ForeignKey(Pets, on_delete=models.CASCADE, related_name='visits')
    date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=(('planned', 'Planned'), ('cancelled', 'Cancelled')),
                                  default='planned')
    notes = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"Visit for {self.user.username} on {self.date}"
