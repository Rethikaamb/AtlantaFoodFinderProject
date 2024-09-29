from django import forms

class RestaurantSearchForm(forms.Form):
    query = forms.CharField(label='Search for restaurants', max_length=100)