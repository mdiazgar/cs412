# File: dadjokes/urls.py
# Author: María Díaz Garrido
# Description: URL routes for the dadjokes app. 
    
from django.urls import path
from . import views

app_name = 'dadjokes'

html_urlpatterns = [
    path('', views.random_page, name='home'),
    path('random', views.random_page, name='random'),
    path('jokes', views.jokes_list, name='jokes_list'),
    path('joke/<int:pk>', views.joke_detail, name='joke_detail'),
    path('pictures', views.pictures_list, name='pictures_list'),
    path('picture/<int:pk>', views.picture_detail, name='picture_detail'),
]

api_urlpatterns = [
    path('', views.RandomJokeAPIView.as_view(), name='api_home'),
    path('random', views.RandomJokeAPIView.as_view(), name='api_random'),
    path('jokes', views.JokesListCreateAPIView.as_view(), name='api_jokes'),
    path('joke/<int:pk>', views.JokeDetailAPIView.as_view(), name='api_joke_detail'),
    path('pictures', views.PicturesListAPIView.as_view(), name='api_pictures'),
    path('picture/<int:pk>', views.PictureDetailAPIView.as_view(), name='api_picture_detail'),
]
