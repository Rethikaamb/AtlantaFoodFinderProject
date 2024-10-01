import requests
from django.contrib.auth import authenticate, user_logged_in
from django.contrib.auth import login as log_in
from django.contrib.auth import logout as log_out
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from AtlantaFoodFinder import settings
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Favorite
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import Restaurant
from home.forms import RestaurantSearchForm

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Favorite, Restaurant
from .serializers import FavoriteSerializer, RestaurantSerializer


# Create your views here.
def home(request):
    if User.is_authenticated and not User.is_active:
        return redirect('map/')
    return render(request, "home/index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

         # Validate the email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email address.")

        if User.objects.filter(username=username):
            messages.error(request, "Username already taken")

        elif User.objects.filter(email=email):
            messages.error(request, "Email already associated with an account")

        elif len(username) > 15 or len(username) < 5 :
            messages.error(request, "Username must be less than 15 characters and greater than 5")

        elif len(pass1) < 5 or len(pass1) > 15:
            messages.error(request, "Password must be greater than 5 characters and less than 15")

        elif pass1 != pass2:
            messages.error(request, "Passwords must match")

        elif not username.isalnum():
            messages.error(request, "Username must be alphanumeric")

        elif not pass1.isalnum():
            messages.error(request, "Password must be alphanumeric")

        else:
            # THE FOLLOWING EXISTS IN CASE WE EVER WANT TO SEND VERIFICATION/WELCOME EMAILS
            # CURRENTLY, THE SETTINGS OF THE GOOGLE ACCOUNT ARE NOT LIKING THE DJANGO LOGIN, SO IT IS NOT CURRENTLY IN OPERATION
            user = User.objects.create_user(username, email, pass1)
            user.first_name = fname
            user.last_name = lname
            user.email = email

            user.save()

            messages.success(request, "Account successfully created")

            subject = "Welcome to Atl Food Finder - Account Creation"
            message = "Hello, " + user.first_name + "!\n" + "Welcome to Atl Food Finder. Thanks for visiting our site. We have also sent you a confirmation email to validate your address. You must do this in order to activate your account.\n\n Thank you,\n 2340 Team 29"
            from_email = settings.EMAIL_HOST_USER
            to_email = [user.email]
            send_mail(subject, message, from_email, to_email, fail_silently=True)

            return redirect('login')

    return render(request, "home/signup.html")
    # return redirect("home/signup.html")

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['pass1']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            log_in(request, user)
            fname = user.first_name
            return redirect('map/')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, "home/login.html")

def logout(request):
    log_out(request)
    messages.success(request, "Logged out successfully")
    user = authenticate(request, username="false", password="false")
    return redirect('home')


from django.http import JsonResponse

from django.http import JsonResponse

def map_view(request):
    search_results = []
    form = RestaurantSearchForm()

    if request.method == "POST":
        form = RestaurantSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            rating_filter = form.cleaned_data.get('rating', '0')
            distance_filter = int(form.cleaned_data.get('distance', '20233'))
            user_lat = float(request.POST.get('user_lat'))
            user_lng = float(request.POST.get('user_lng'))

            api_key = settings.GOOGLE_MAPS_API_KEY
            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&location={user_lat},{user_lng}&radius={distance_filter}&key={api_key}"
            response = requests.get(url)
            results = response.json().get('results', [])

            search_results = []
            for place in results:
                if place.get('rating', 0) >= float(rating_filter):
                    place_data = {
                        'place_id': place['place_id'],
                        'name': place['name'],
                        'vicinity': place.get('vicinity', ''),
                        'rating': place.get('rating', 'N/A'),
                        'types': place.get('types', []),
                        'geometry': place['geometry'],
                    }
                    if 'photos' in place and place['photos']:
                        place_data['photo_reference'] = place['photos'][0]['photo_reference']
                    search_results.append(place_data)

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'search_results': search_results})

    return render(request, 'map.html', {
        'form': form,
        'search_results': search_results,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    })
def forgotpassword(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_pass1 = request.POST.get('pass1')
        new_pass2 = request.POST.get('pass2')

        if username and new_pass1 and new_pass2:  #all fields filled in
            try:
                user = User.objects.get(username=username)
                # Check if new pass is the same as old
                if check_password(new_pass1, user.password):
                    messages.error(request, "New password cannot be the same as the old password.")
                elif len(new_pass1) < 5 or len(new_pass1) > 15:
                    messages.error(request, "New password must be greater than 5 characters and less than 15")
                elif not new_pass1.isalnum():
                    messages.error(request, "Password must be alphanumeric")
                elif new_pass1 == new_pass2:
                    user.password = make_password(new_pass1)
                    user.save()
                    messages.success(request, "Success! You will get redirected shortly.")
                    return redirect('login')
                else:
                    messages.error(request, "Passwords do not match.")
            except User.DoesNotExist:
                messages.error(request, "User does not exist.")
        else:
            messages.error(request, "All fields are required.")
    return render(request, 'home/forgotpassword.html')

# Add a restaurant to favorites
@api_view(['POST'])
def add_favorite(request):
    if request.user.is_authenticated:
        user = request.user
        restaurant_id = request.data.get('restaurant_id')

        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            favorite, created = Favorite.objects.get_or_create(user=user, restaurant=restaurant)
            if created:
                return Response({"message": "Restaurant added to favorites"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Restaurant is already in favorites"}, status=status.HTTP_200_OK)
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant does not exist"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
# Remove a restaurant from favorites
@api_view(['DELETE'])
def remove_favorite(request, restaurant_id):
    if request.user.is_authenticated:
        user = request.user
        try:
            favorite = Favorite.objects.get(user=user, restaurant_id=restaurant_id)
            favorite.delete()
            return Response({"message": "Favorite removed"}, status=status.HTTP_200_OK)
        except Favorite.DoesNotExist:
            return Response({"error": "Favorite does not exist"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

# List all favorite restaurants for the logged-in user
@api_view(['GET'])
def list_favorites(request):
    if request.user.is_authenticated:
        user = request.user
        favorites = Favorite.objects.filter(user=user)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)
    else:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)


# Get only the favorite restaurants for the logged-in user
@api_view(['GET'])
def get_favorite_restaurants(request):
    if request.user.is_authenticated:
        user = request.user
        favorite_restaurants = Favorite.objects.filter(user=user).values_list('restaurant', flat=True)
        restaurants = Restaurant.objects.filter(id__in=favorite_restaurants)
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)
    else:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def save_restaurant(request):
    if request.method == 'POST':
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




def account(request):
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user)
    else:
        favorites = []

    return render(request, "account.html", {"favorites": favorites})

def add_favorite(request, restaurant_id):
    if request.method == "POST" and request.user.is_authenticated:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        Favorite.objects.get_or_create(user=request.user, restaurant=restaurant)
        return HttpResponseRedirect(reverse('account'))  # Redirect to account page