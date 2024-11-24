from django.shortcuts import render, redirect
from django.http import JsonResponse
from .signals import user_input_received
import json

def index(request):
    if request.method == 'POST':
        user_input = request.POST.get('message', 'BABABBABABA')
        context = request.session.get('context', '')
        request.session['context'] = context + 'User: ' + user_input + '\n'

        # Emit the signal and capture the result
        signal_result = {}
        signal_data = json.dumps({
            'context': request.session['context'],
            'last_input': user_input,
            'cart': request.session.get('cart', [])
        })
        ans = user_input_received.send(sender=None, user_input=signal_data, result=signal_result)
        model_output = ans[0][1]['model_output']
        item_name = ans[0][1]['item']['name']
        item_price = ans[0][1]['item']['price']

        request.session['context'] += 'Chatbot: ' + model_output + '\n'
        return JsonResponse({'response': model_output, 'question': user_input, 'item': {'name': item_name, 'price': item_price}})

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
    request.session['cart'].append({'name': item_name, 'price': item_price})
    request.session.modified = True

    return JsonResponse({'cart': request.session['cart']})


def get_cart(request):
    """Return the current cart and calculate the total price."""
    cart = request.session.get('cart', [])
    total = sum(float(item['price']) for item in cart) if cart else 0.0
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


