# chatbox/signals.py
from django.dispatch import Signal

# Define a custom signal
user_input_received = Signal()

import numpy as np

from django.dispatch import receiver
from .signals import user_input_received
from mistralai import Mistral
import sys
api_key = "Ayt9pyjjA1Y2Tltpu85aUyJXu6EcflT8"
model = "mistral-small-latest"
from mistralai import Mistral
import pandas as pd
from backend.k_closest import *
from backend.traduction import *
from backend.prompt import *
import json

# Conversion de la colonne 'embeddings' en tableaux numpy
# Chaque vecteur est représenté comme une chaîne de caractères dans le CSV
products = pd.read_csv('chatbox/data/products.csv')
products['embeddings'] = products['embeddings'].apply(lambda x: np.fromstring(x[1:-1], sep=','))


# Fonction pour récupérer le produit le plus proche en fonction de l'entrée utilisateur
def get_closest(user_input):
    model = "mistral-embed"
    client_loc = Mistral(api_key=api_key)

    embeddings_batch_response = client_loc.embeddings.create(
        model=model,
        inputs=[user_input],
    )

    k_neighbors = k_nearest_neighbors_with_indices(embeddings_batch_response.data[0].embedding, products["embeddings"], 1)
    print("LINDEX " + products.iloc[k_neighbors[0]]["name"])
    return k_neighbors[0]

# Receiver function to handle the signal
@receiver(user_input_received)
def process_user_input(sender, user_input, **kwargs):
    print(f"Processing user input: {user_input} \n")  # Log input for debugging
    # Example logic: calculate the square of a number
    client = Mistral(api_key=api_key)
    # Deserialize the user_input string
    data = json.loads(user_input)

    
    context = data.get('context', '')
    last_input = data.get('last_input', '')
    
    trad = traduction(last_input)
    print("phrase traduite "+ trad)
    
    index_closest = get_closest(trad)

    prompt = get_prompt(last_input, products.iloc[index_closest]["name"], context)

    chat_response = client.chat.complete(
         model = model,
         messages = [
             {
                 "role": "user",
                 "content": prompt,
             },
         ]
     )
    result = chat_response.choices[0].message.content
    print(result)

    kwargs['result'] = result
    return result