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

# Receiver function to handle the signal
@receiver(user_input_received)
def process_user_input(sender, user_input, **kwargs):
    # Deserialize the user_input string
    data = json.loads(user_input)

    #On récupère toutes les données utiles : context, last_input, cart
    context = data.get('context', '')
    last_input = data.get('last_input', '')
    cart = data.get('cart', [])

    ##########
    ####
    ### ines produits = function(context, last_input)
    ### ---------> return dict{'liste_1':...., }
    #########
    raw_lists = ...
    ####ici je convertis pour tous les objets en celui que je trouve dans la base de donnée
    ###

    # main_list_indexes, rec_list_indexes = get_lists(raw_lists)
    # main_list = [{'name': traduction(products.iloc[index]["name"], 'français'), 'price': products.iloc[index]["price"]} for index in main_list_indexes]
    # rec_list = [{'name': traduction(products.iloc[index]["name"], 'français'), 'price': products.iloc[index]["price"]} for index in rec_list_indexes]
    # liste_principale = [elt['name'] for elt in main_list]
    # liste_complementaire = [elt['name'] for elt in rec_list]

    ########### ici peut être garder la main list et juste la str ?????? 
    # prompt_chat = get_prompt_chat(last_input, context, str(liste_principale), str(liste_complementaire), str(cart))
    # model_output = call(prompt_chat)


###############################################################"
# "
    index_closest = get_closest(user_input)
    
    name = products.iloc[index_closest]["name"]
    name = traduction(name, langue='français')
    price = products.iloc[index_closest]["price"]
    main_list = [{'name': name, 'price': price}]
    prompt = get_prompt(last_input, name, context)
    model_output=call(prompt)
###################################################################
    return {'model_output': model_output, 'items': main_list}