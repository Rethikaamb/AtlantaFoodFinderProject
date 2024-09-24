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

        if User.objects.filter(username=username):
            messages.error(request, "Username already taken")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "Email already associated with an account")
            return redirect('home')

        if len(username) > 15:
            messages.error(request, "Username must be less than 15 characters")

        if pass1 != pass2:
            messages.error(request, "Passwords must match")

        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric")

        #THE FOLLOWING EXISTS IN CASE WE EVER WANT TO SEND VERIFICATION/WELCOME EMAILS
        #CURRENTLY, THE SETTINGS OF THE GOOGLE ACCOUNT ARE NOT LIKING THE DJANGO LOGIN, SO IT IS NOT CURRENTLY IN OPERATION
        user = User.objects.create_user(username, email, pass1)
        user.first_name = fname
        user.last_name = lname

        user.save()

        messages.success(request, "Account successfully created")

        subject = "Welcome to Atl Food Finder - Account Creation"
        message = "Hello, " + user.first_name + "!\n" + "Welcome to Atl Food Finder. Thanks for visiting our site. We have also sent you a confirmation email to validate your address. You must do this in order to activate your account.\n\n Thank you,\n 2340 Team 29"
        from_email = settings.EMAIL_HOST_USER
        to_email = [user.email]
        send_mail(subject, message, from_email, to_email, fail_silently=True)

        return redirect('login')

    return render(request, "home/signup.html")

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['pass1']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            log_in(request, user)
            fname = user.first_name
            return render(request, "map.html", {'fname': fname})
        else:
            messages.error(request, "Invalid username or password")
            return redirect('home')

    return render(request, "home/login.html")

def logout(request):
    log_out(request)
    messages.success(request, "Logged out successfully")
    user = authenticate(request, username="false", password="false")
    return redirect('home')

def map_view(request):
    return render(request, 'map.html', {'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY})