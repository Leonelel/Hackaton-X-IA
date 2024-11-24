import pandas as pd
import functools

import os
from mistralai import Mistral
import json


api_key = "Ayt9pyjjA1Y2Tltpu85aUyJXu6EcflT8"
model = "open-mistral-7b"

def get_vectors_prod_et_reco(user_input, user_input_reco):
  tab = []
  tab1 = []
  model = "mistral-embed"
  client_loc = Mistral(api_key=api_key)

  for t in user_input:
    embeddings_batch_response = client_loc.embeddings.create(
      model=model,
      inputs=[t],
    )
    tab.append(embeddings_batch_response.data[0].embedding)

  for t in user_input_reco:
    embeddings_batch_response = client_loc.embeddings.create(
      model=model,
      inputs=[t],
    )
    tab1.append(embeddings_batch_response.data[0].embedding)

  return tab, tab1


def prod_lists(products, context, last_input):
  data = products
# Assuming we have the following data
# Create DataFrame
  df = pd.DataFrame(data)
  to_send = []
  for el in context:
    to_send.append({'role':'user', 'content':el['user']})
    to_send.append({'role':'assistant', 'content':el['model']})
  to_send.append({'role':'user', 'content':last_input}) 
  print("COUCOU BANDE DE NOUILLES")

  tools = [
      {
          "type": "function",
          "function": {
              "name": "get_vectors_prod_et_reco",
              "description": "Transforms two lists of grocery products into vectors. The first list is a list of products desired by the customer. For example, if the customer wants ingredients to bake a cake, its argument should look like [\"eggs\", \"flour\",\"sugar\"]. The second list is a list of recommended products",
              "parameters": {
                  "type": "object",
                  "properties": {
                      "user_input": {
                          "type": "array",
                          "description": "Liste des produits spécifiquement demandés par l'utilisateur.",
                      },
                      "user_input_reco": {
                          "type": "array",
                          "description": "Liste des produits recommandés en fonction des besoins de l'utilisateur.",
                      }
                  },
                  "required": ["user_input", "user_input_reco"],  # Spécifie que ces deux paramètres sont obligatoires
              },
          },
      },
  ]

  names_to_functions = {
    'get_vectors_prod_et_reco': functools.partial(get_vectors_prod_et_reco, df=df)
  }

  tab = []
  client = Mistral(api_key=api_key)

  for t in tools:
    response = client.chat.complete(
        model = model,
        messages = to_send,
        tools = tools,
        tool_choice = "any",
    )
    tab.append(response)

  # Extraction des données 'user_input' et 'user_input_reco' depuis les réponses
  user_inputs = []
  user_input_recos = []

  for response in tab:
      # Parcours des choix dans la réponse
      for choice in response.choices:  # Accéder directement à l'attribut `choices`
          # Accéder aux appels d'outils dans chaque choix
          tool_calls = choice.message.tool_calls  # Utilisation directe des attributs
          for tool_call in tool_calls:
              # Récupérer les arguments de l'appel d'outil
              arguments = tool_call.function.arguments
              try:
                  # Charger les arguments comme un dictionnaire
                  arguments_dict = json.loads(arguments)
                  # Vérifier et extraire les valeurs nécessaires
                  if "user_input" in arguments_dict:
                      user_inputs.extend(arguments_dict["user_input"])
                  if "user_input_reco" in arguments_dict:
                      user_input_recos.extend(arguments_dict["user_input_reco"])
              except json.JSONDecodeError:
                  continue
  ret = {'liste_produits': user_inputs,'liste_recos': user_input_recos} 
  print(ret) 
  # Résultats finaux
  return ret