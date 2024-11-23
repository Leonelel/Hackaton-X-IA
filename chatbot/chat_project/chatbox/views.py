from django.shortcuts import render
from django.http import JsonResponse
from .signals import user_input_received

def index(request):
    if request.method == 'POST':
        user_input = request.POST.get('message', 'BABABBABABA')
        context = request.session.get('context', '')
        request.session['context'] = context + 'User: ' + user_input + '\n'

        # Emit the signal and capture the result
        signal_result = {}
        ans = user_input_received.send(sender=None, user_input=request.session['context'], result=signal_result)

        print(f"User input: {user_input}")  # Log for debugging
        request.session['context'] += 'Chatbot: ' + ans[0][1] + '\n'
        print(f"Context : {request.session['context']}")
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