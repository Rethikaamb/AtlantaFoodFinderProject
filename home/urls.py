from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),

    path('map/', views.map_view, name='map_view'),
    path('forgotpassword', views.forgotpassword, name='forgotpassword'),
    path('account', views.account, name='account')

]
