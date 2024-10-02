from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),

    path('map/', views.map_view, name='map_view'),
    path('forgotpassword', views.forgotpassword, name='forgotpassword'),
    path('api/save-restaurant/', views.save_restaurant, name='save_restaurant'),
    path('api/favorites/list/', views.list_favorites, name='list_favorites'),
    path('api/favorites/add/', views.add_favorite, name='add_favorite'),
    path('api/favorites/remove/<str:restaurantID>/', views.remove_favorite, name='remove_favorite'),

    path('api/restaurants/favorites/', views.get_favorite_restaurants, name='get_favorite_restaurants'),
    path('account', views.account, name='account')
]