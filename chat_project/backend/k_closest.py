import numpy as np
import pandas as pd


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
def k_nearest_neighbors_with_indices(reference_vector, vectors, k):
    reference_vector = np.array(reference_vector)
    vectors = np.array(vectors)

    distances = euclidean_distances(reference_vector, vectors).flatten()

    nearest_indices = np.argsort(distances)[:k]
    return nearest_indices