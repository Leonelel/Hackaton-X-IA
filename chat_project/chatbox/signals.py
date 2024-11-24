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
model = "open-mistral-7b"
from mistralai import Mistral
import pandas as pd
from backend.k_closest import *
from backend.traduction import *
from backend.prompt import *
from backend.call import *
import json

# Conversion de la colonne 'embeddings' en tableaux numpy
# Chaque vecteur est représenté comme une chaîne de caractères dans le CSV
products = pd.read_csv('chatbox/data/products.csv')
products['embeddings'] = products['embeddings'].apply(lambda x: np.fromstring(x[1:-1], sep=','))


# Fonction pour récupérer le produit le plus proche en fonction de l'entrée utilisateur

# Receiver function to handle the signal
@receiver(user_input_received)
def process_user_input(sender, user_input, **kwargs):
    print(f"Processing user input: {user_input} \n")  # Log input for debugging
    # Example logic: calculate the square of a number
    client = Mistral(api_key=api_key)
    # Deserialize the user_input string
    data = json.loads(user_input)

    #Garde le contexte précédent
    context = data.get('context', '')
    last_input = data.get('last_input', '')
    cadis = data.get('cart', [])
    
    #Phrase traduite
    trad = traduction(last_input)
    print("phrase traduite "+ trad)
    
    
    #Index du plus proche point
    index_closest = get_closest(trad)
    
    #Liste de mots clés à chercher dans la base de données:
    key_words = call(get_prompt_liste(trad), "open-mistral-7b")
    print("les mots clés sont : "+ key_words)
    
    name = products.iloc[index_closest]["name"]
    name = traduction(name, langue='français')
    price = products.iloc[index_closest]["price"]

    prompt = get_prompt(last_input, name, context)

    chat_response = client.chat.complete(
         model = model,
         messages = [
             {
                 "role": "user",
                 "content": prompt,
             },
         ]
     )
    model_output = chat_response.choices[0].message.content

    return {'model_output': model_output, 'item': {'name': name , 'price': price}}