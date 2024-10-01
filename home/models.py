from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    place_id = models.CharField(max_length=255, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    rating = models.FloatField(null=True, blank=True)
    types = models.TextField()

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    restaurantID = models.CharField(max_length=255, default='0')
    place_name = models.CharField(max_length=255, default='0')


    def __str__(self):
        return f"{self.user.username} - {self.restaurantID} - {self.place_name}"