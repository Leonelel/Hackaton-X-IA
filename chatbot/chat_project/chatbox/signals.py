# chatbox/signals.py
from django.dispatch import Signal

# Define a custom signal
user_input_received = Signal()

from django.dispatch import receiver
from .signals import user_input_received
import os
from mistralai import Mistral
import sys
api_key = "Ayt9pyjjA1Y2Tltpu85aUyJXu6EcflT8"
model = "mistral-small-latest"


# Receiver function to handle the signal
@receiver(user_input_received)
def process_user_input(sender, user_input, **kwargs):
    print(f"Processing user input: {user_input}")  # Log input for debugging
    # Example logic: calculate the square of a number
    client = Mistral(api_key=api_key)
    chat_response = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
                "content": user_input,
            },
        ]
    )
    result = chat_response.choices[0].message.content
    print(result)
    # Store the result in the kwargs for further processing
    kwargs['result'] = result
    return result