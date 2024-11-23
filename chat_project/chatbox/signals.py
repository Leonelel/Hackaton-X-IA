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
import os
from mistralai import Mistral
import pandas as pd

products = pd.read_csv('chatbox/data/products.csv')
products['embeddings'] = products['embeddings'].apply(lambda x: np.fromstring(x[1:-1], sep=','))


def euclidean_distances(vector, matrix):
  tab = []
  for i in range(len(matrix)):
    tab.append(np.linalg.norm(vector - matrix[i]))
  tab = np.array(tab)
  return tab

def k_nearest_neighbors_with_indices(reference_vector, vectors, k):
    reference_vector = np.array(reference_vector)
    vectors = np.array(vectors)

    distances = euclidean_distances(reference_vector, vectors).flatten()

    nearest_indices = np.argsort(distances)[:k]

    nearest_vectors = vectors[nearest_indices]
    nearest_distances = distances[nearest_indices]

    return nearest_indices

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

    index_closest = get_closest(user_input)


    prompt = f"Tu es un assistant pour vendre essentiellement des produits alimentaires mais egalement des produits qu'on trouve dans des grandes surfaces comme carrefour, ici la demande du user est ({user_input}) et il se trouve que tu as le produit {products.iloc[index_closest]['name']} a lui proposer tu devras donc repondre au client de manière adéquat dans la même langue que sa requête, de confirmer ou non l'ajout du produit {products.iloc[index_closest]['name']} dans sa liste de course."

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