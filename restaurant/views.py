from django.shortcuts import render, redirect
from decimal import Decimal
import time
import random
from django.http import HttpResponse

MENU = [
    {'key': 'tortilla', 'name': 'Tortilla de Patatas', 'price': Decimal('12.00')},
    {'key': 'croquetas', 'name': 'Croquetas de Jamon Iberico', 'price': Decimal('9.50')},
    {'key': 'salmorejo', 'name': 'Salmorejo Andaluz', 'price': Decimal('8.00')},
    {'key': 'paella', 'name': 'Paella con Conejo', 'price': Decimal('15.75')},
]

DAILY_SPECIALS = [
    {'key': 'sopa',  'name': 'Sopa de Estrellitas', 'price': Decimal('8.00'), 'desc': 'Family recipe for soup when someone is not feeling well'},
    {'key': 'tostada', 'name': 'Tostada con Fuet', 'price': Decimal('5.50'), 'desc': 'Our special breakfast with hand made bread, butter imported from Toledo and fuet from Barcelona'},
    {'key': 'migas', 'name': "Migas de Juan", 'price': Decimal('99.99'), 'desc': 'The famous migas cooked for hours by our very own Masterchef Junior participant Juan Diaz'},
    {'key': 'churros', 'name': 'San Gines Churros', 'price': Decimal('9.10'), 'desc': 'Most famous spanish breakfast these churros are imported from the best churreria in Madrid'},
    {'key': 'merienda', 'name': 'Merienda del Abuelo', 'price': Decimal('11.11'), 'desc': 'La merienda del abuelo, incluye su cafe con leche y bocadillos de jamon y bacon para todos los primos'}
]

def main(request):
    ctx = {
        'restaurant_name': 'Casa Lola',
        'location': 'Calle Brujidero 9, Cunit, España',
        'hours': [
            ('Mon–Thu', '9:00 – 22:00'),
            ('Fri–Sat', '9:00 – 23:00'),
            ('Sun',     '12:00 – 22:00'),
        ],
    }
    return render(request, 'restaurant/main.html', ctx)

def order(request):
    special = random.choice(DAILY_SPECIALS)
    ctx = {
        'menu': MENU,
        'special': special,
    }
    return render(request, 'restaurant/order.html', ctx)

def confirmation(request):
    if request.method != 'POST':
        return redirect('restaurant:order')

    name = request.POST.get('name', '').strip()
    phone = request.POST.get('phone', '').strip()
    email = request.POST.get('email', '').strip()
    instructions = request.POST.get('instructions', '').strip()

    items_ordered = []
    total = Decimal('0.00')
    
    menu_by_key = {m['key']: m for m in MENU}
    for key, item in menu_by_key.items():
        if request.POST.get(key):  
            items_ordered.append({'name': item['name'], 'price': item['price']})
            total += item['price']
    
        if request.POST.get('daily_special'):
            special_name = request.POST.get('special_name')
            special_price_str = request.POST.get('special_price')
            if special_name and special_price_str:
                price = Decimal(special_price_str)
                items_ordered.append({'name': special_name, 'price': price})
                total += price
    
    empty_order = (len(items_ordered) == 0)
    
    ready_in_minutes = random.randint(30, 60)
    ready_epoch = time.time() + ready_in_minutes * 60
    ready_time_str = time.strftime("%I:%M %p on %b %d, %Y", time.localtime(ready_epoch))
    
    ctx = {
        'name': name,
        'phone': phone,
        'email': email,
        'instructions': instructions,
        'items': items_ordered,
        'total': total,
        'empty order': empty_order,
        'ready_in_minutes': ready_in_minutes,
        'ready_time_str': ready_time_str,
    }
    return render(request, 'restaurant/confirmation.html', ctx)
