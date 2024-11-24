import numpy as np
import pandas as pd
from backend.call import *
products = pd.read_csv('chatbox/data/products.csv')
products = products.iloc[:1000, :]
products['embeddings'] = products['embeddings'].apply(lambda x: np.fromstring(x[1:-1], sep=','))
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
  return nearest_neighbor_with_indice(reference_vector, vectors, 1)

def get_closest(user_input):
  embeddings_batch_response = call_embed(user_input)

  k_neighbors = nearest_neighbor_with_indice(embeddings_batch_response.data[0].embedding, products["embeddings"],1)
  return k_neighbors


def nearest_neighbor_with_indice(reference_vector, vectors, k):
  reference_vector = np.array(reference_vector)
  vectors = np.array(vectors)

  distances = euclidean_distances(reference_vector, vectors).flatten()

  nearest_indices = np.argmin(distances)
  return nearest_indices
  
def k_indices(liste, vectors):
  tab =[]
  for i in liste:
    tab.append(nearest_neighbor_with_indice(i,vectors,1))
  return tab
            
def get_lists(raw_lists):
  main_list = [get_closest(elt) for elt in raw_lists['liste_produits']]
  rec_list = [get_closest(elt) for elt in raw_lists['liste_recos']]
  return (main_list, rec_list)
  