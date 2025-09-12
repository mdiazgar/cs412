from random import choice
from django.shortcuts import render

PERSON = "Daenerys Targaryen"   

QUOTES = [
    "I'm not going to stop the wheel. I'm going to break the wheel.",
    "I will take what is mine with fire and blood.",
    "Do you know what kept me standing through all those years in exile? Faith. Not in any gods, not in myths and legends, in myself. In Daenerys Targaryen.",
    "I will answer injustice with justice.",
    "The next time you raise a hand to me will be the last time you have hands.",
    "Woman? Is that meant to insult me? I would return the slap if I took you for a man.",
    "Dracarys."
]

IMAGES = [
    "https://i0.wp.com/maepolzine.com/wp-content/uploads/2019/05/Daenerys-Targaryen-Hair-S1.jpg?fit=970%2C546&ssl=1",
    "https://static.wikia.nocookie.net/iceandfire/images/c/c0/7dff25854a409a596b954d04f6c3a98d.jpg/revision/latest/scale-to-width/360?cb=20250608221439",
    "https://behindthechair.com/wp-content/uploads/2017/10/halloween-how-to-daenerys-targaryen-braids.jpg",
    "https://i.ebayimg.com/images/g/h4EAAOSwgrlgTFF6/s-l1200.jpg",
    "https://www.hollywoodreporter.com/wp-content/uploads/2017/11/got-110-h_2017.jpg?w=1296&h=730&crop=1"
    
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

