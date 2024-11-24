from django.shortcuts import render, redirect
from django.http import JsonResponse
from .signals import user_input_received
import json

def index(request):
    if request.method == 'POST':
        user_input = request.POST.get('message', 'BABABBABABA')
        context = request.session.get('context', [])

        # Emit the signal and capture the result
        signal_result = {}
        signal_data = json.dumps({
            'context': context,
            'last_input': user_input,
            'cart': request.session.get('cart', [])
        })
        ans = user_input_received.send(sender=None, user_input=signal_data, result=signal_result)

        model_output = ans[0][1]['model_output']
        items = ans[0][1]['items']  # Liste des articles à ajouter au panier

        # Mettre à jour le contexte utilisateur
        context.append({'user': user_input, 'model': model_output})
        request.session['context'] = context

        # Ajouter tous les articles retournés dans le panier de la session
        if 'cart' not in request.session:
            request.session['cart'] = []

        for item in items:
            existing_item = next((cart_item for cart_item in request.session['cart'] if cart_item['name'] == item['name']), None)
            if existing_item:
                existing_item['quantity'] += item.get('quantity', 1)
            else:
                request.session['cart'].append({
                    'name': item['name'],
                    'price': item['price'],
                    'quantity': item.get('quantity', 1)
                })

        request.session.modified = True

        return JsonResponse({'response': model_output, 'question': user_input, 'items': items})

    if request.method == 'GET':
        reset(request)
    return render(request, 'chatbox/index.html')


def reset(request):
    # Clear all session variables
    request.session.flush()
    return redirect('index')


def add_to_cart(request):
    """Add an item to the cart with its name and price."""
    item_name = request.POST.get('item_name', '')
    item_price = request.POST.get('item_price', '')

    if 'cart' not in request.session:
        request.session['cart'] = []

    # Ajouter l'article avec son nom et son prix dans le panier
    existing_item = next((cart_item for cart_item in request.session['cart'] if cart_item['name'] == item_name), None)
    if existing_item:
        existing_item['quantity'] += 1
    else:
        request.session['cart'].append({'name': item_name, 'price': item_price, 'quantity': 1})

    request.session.modified = True

    return JsonResponse({'cart': request.session['cart']})


def get_cart(request):
    """Return the current cart and calculate the total price."""
    cart = request.session.get('cart', [])
    total = sum(float(item['price']) * item.get('quantity', 1) for item in cart) if cart else 0.0
    return JsonResponse({'cart': cart, 'total': total})


def clear_cart(request):
    """Clear all items from the cart."""
    request.session['cart'] = []
    request.session.modified = True
    return JsonResponse({'cart': request.session['cart']})


def remove_from_cart(request):
    """Remove an item from the cart based on its index."""
    index = int(request.POST.get('index', -1))
    if 'cart' in request.session and 0 <= index < len(request.session['cart']):
        del request.session['cart'][index]
        request.session.modified = True
    return JsonResponse({'cart': request.session.get('cart', [])})
