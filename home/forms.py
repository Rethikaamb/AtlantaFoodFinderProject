from django import forms

class RestaurantSearchForm(forms.Form):
    query = forms.CharField(label='Search for restaurants', max_length=100)
    rating = forms.ChoiceField(
        label='Minimum Rating',
        choices=[(0, 'Any'), (1, '1+'), (2, '2+'), (3, '3+'), (4, '4+'), (5, '5')],
        required = False
    )
    distance=forms.ChoiceField(
        label='Maximum Distance',
        choices=[(1609,'1 mile'), (4828, '3 miles'), (8046, '5 miles'), (16093, '10 miles'), (20233, '25 miles')],
        required = False
    )