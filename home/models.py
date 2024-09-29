from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# models.py

class FavoriteRestaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place_id = models.CharField(max_length=255, unique=True)  # Ensure unique place IDs
    name = models.CharField(max_length=255)  # Optional: Store the restaurant's name
    address = models.CharField(max_length=255)  # Optional: Store the address

    def __str__(self):
        return f"{self.name} - {self.user.username}"