# File: dadjokes/views.py
# Author: María Díaz Garrido
# Description: Class-based views for the dadjokes app. 

from django.shortcuts import render

# Create your views here.
import random
from django.shortcuts import get_object_or_404, render
from .models import Joke, Picture

def random_page(request):
    joke = Joke.objects.order_by('?').first()
    picture = Picture.objects.order_by('?').first()
    context = {'joke': joke, 'picture': picture}
    return render(request, 'dadjokes/index.html', context)

def jokes_list(request):
    jokes = Joke.objects.all()
    return render(request, 'dadjokes/jokes_list.html', {'jokes': jokes})

def joke_detail(request, pk: int):
    joke = get_object_or_404(Joke, pk=pk)
    return render(request, 'dadjokes/joke_detail.html', {'joke': joke})

def pictures_list(request):
    pictures = Picture.objects.all()
    return render(request, 'dadjokes/pictures_list.html', {'pictures': pictures})

def picture_detail(request, pk: int):
    picture = get_object_or_404(Picture, pk=pk)
    return render(request, 'dadjokes/picture_detail.html', {'picture': picture})

#####################################################################################################################################
# REST API

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import Joke, Picture


class RandomJokeAPIView(APIView):
    """
    GET -> returns one random Joke (for /api/ and /api/random)
    """
    def get(self, request, *args, **kwargs):
        joke = Joke.objects.order_by('?').first()
        if not joke:
            return Response({"detail": "No jokes available."}, status=status.HTTP_404_NOT_FOUND)
        return Response(JokeSerializer(joke).data)


class JokesListCreateAPIView(generics.ListCreateAPIView):
    """
    GET -> list all jokes
    POST -> create a new joke (expects JSON: {text, contributor})
    """
    queryset = Joke.objects.all().order_by("-created_at")
    serializer_class = JokeSerializer


class JokeDetailAPIView(generics.RetrieveAPIView):
    """
    GET -> retrieve a joke by pk
    """
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer
    lookup_field = "pk"


class PicturesListAPIView(generics.ListAPIView):
    """
    GET -> list all pictures
    """
    queryset = Picture.objects.all().order_by("-created_at")
    serializer_class = PictureSerializer


class PictureDetailAPIView(generics.RetrieveAPIView):
    """
    GET -> retrieve a picture by pk
    """
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    lookup_field = "pk"
