import numpy as np
import pandas as pd
from backend.call import *

#leonel est homo
# Fonction pour calculer les distances euclidiennes : 
# entrées: vecteur de base, matrice de vecteurs
# return : tableau numpy des distances du vecteur à chaque point
def euclidean_distances(vector, matrix):
  tab = []
  for i in range(len(matrix)):
    tab.append(np.linalg.norm(vector - matrix[i]))
  tab = np.array(tab)
  return tab

# Fonction pour trouver les k plus proches voisins

def article_propose(reference_vector, vectors):
  return k_nearest_neighbors_with_indices(reference_vector, vectors, 1)[0]

def get_closest(user_input):
  embeddings_batch_response = call_embed(user_input)
  products = pd.read_csv('chatbox/data/products.csv')
  products['embeddings'] = products['embeddings'].apply(lambda x: np.fromstring(x[1:-1], sep=','))

  k_neighbors = k_nearest_neighbors_with_indices(embeddings_batch_response.data[0].embedding, products["embeddings"],1)
  return k_neighbors[0]


def k_nearest_neighbors_with_indices(reference_vector, vectors, k):
  reference_vector = np.array(reference_vector)
  vectors = np.array(vectors)

  distances = euclidean_distances(reference_vector, vectors).flatten()

  nearest_indices = np.argsort(distances)[:k]
  return nearest_indices
  
def k_indices(liste, vectors):
  tab =[]
  for i in liste:
    tab.append(k_nearest_neighbors_with_indices(i,vectors,1)[0])
  return tab
            
def get_lists(raw_lists):
  main_list = [get_closest(elt) for elt in raw_lists['liste_produits']]
  rec_list = [get_closest(elt) for elt in raw_lists['liste_recos']]
  return (main_list, rec_list)
  