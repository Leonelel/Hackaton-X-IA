from django.shortcuts import render
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
            'last_input': user_input
        })
        ans = user_input_received.send(sender=None, user_input=signal_data, result=signal_result)

        request.session['context'] += 'Chatbot: ' + ans[0][1] + '\n'
        # Return the result to the frontend
        return JsonResponse({'response': ans[0][1], 'question': user_input})

    return render(request, 'chatbox/index.html')

from django.shortcuts import redirect
from django.contrib import messages

def reset(request):
    # Clear all session variables
    request.session.flush()

    # Optional: Add a success message
    messages.success(request, "The session has been reset.")

    # Redirect to the main page
    return redirect('index')