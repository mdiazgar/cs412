from random import choice
from django.shortcuts import render

PERSON = "Daenerys Targaryen"   

QUOTES = [
    "I'm not going to stop the wheel. I'm going to break the wheel.",
    "I will take what is mine with fire and blood.",
    "Do you know what kept me standing through all those years in exile? Faith. Not in any gods, not in myths and legends, in myself. In Daenerys Targaryen.",
]

IMAGES = [
    "https://placehold.co/800x500?text=Einstein+1",
    "https://placehold.co/800x500?text=Einstein+2",
    "https://placehold.co/800x500?text=Einstein+3",
]

def quote(request):
    """Main page & /quote, show one random quote + one random image"""
    context = {
        "person": PERSON,
        "quote": choice(QUOTES),
        "image_url": choice(IMAGES),
    }
    return render(request, "quotes/quote.html", context)

def show_all(request):
    """Show all quotes and all images"""
    context = {
        "person": PERSON,
        "quotes": QUOTES,
        "images": IMAGES,
    }
    return render(request, "quotes/show_all.html", context)

def about(request):
    """About page"""
    context = {
        "person": "Daenerys Targaryen",
        "creator": "Maria Diaz",
    }
    return render(request, "quotes/about.html", context)

