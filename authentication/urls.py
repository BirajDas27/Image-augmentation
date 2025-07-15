from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('main', views.main, name="main"),
    path('grayscale', views.grayscale, name="grayscale"),
    path('verticalFlip', views.verticalFlip, name="verticalFlip"),
    path('horizontalFlip', views.horizontalFlip, name="horizontalflip"),
    path('rotate', views.rotate, name="rotate"),
    path('filter', views.filter, name="filter"),
    path('crop',views.crop, name="crop"),
]