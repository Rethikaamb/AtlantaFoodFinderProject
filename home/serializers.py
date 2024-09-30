from rest_framework import serializers
from .models import Favorite, Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer()  # Nested serializer to include restaurant details

    class Meta:
        model = Favorite
        fields = ['user', 'restaurant']