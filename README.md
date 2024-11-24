# Hackaton-X-IA

# Motivations:

La valeur ajoutée de notre application réside dans le gain de temps qu'elle offre, particulièrement significatif lorsque la liste de courses est longue. Par exemple, cela devient crucial lorsqu'il s'agit de faire les courses pour 60 personnes.

De plus, comme le montrent les pâtes au cordon bleu, il nous arrive parfois de manquer d'inspiration. C'est pourquoi notre shopping asstistant va révolutionner votre manière de faire vos courses ! RetailX propose automatiquement des aliments qui complètent vos recettes, afin d'émerveiller vos papilles !

En cas de levée de fonds (1 million d'euros), l'impact final serait de permettre au projet de se développer à plus grande échelle. Ainsi, tous les supermarchés pourraient intégrer notre chatbot dans leur système de courses en ligne !

### Fonctionnalités:
 - Gestion (semi)-automatique du panier.
 - Recommendations éventuelles sur la demande de l'utilisateur.
 - Chatbot plein de bonnes volonté


# Approche Technique

## Données
Le programme repose sur une base de données contenant les produits alimentaires de Carrefour Espagne. Cette base de données représente les éléments disponibles pour les suggestions et les réponses faites à l'utilisateur.

Le dataset est préalablement reformaté pour permettre une recherche assistée par génération (RAG, Retrieval-Augmented Generation), en utilisant des embeddings générés par **Mistral**. Cette étape garantit une représentation vectorielle optimisée des données pour les requêtes utilisateur.

## Déroulé Technique

### 1. Analyse du prompt utilisateur
Lorsque l'utilisateur envoie un prompt, un mécanisme de **function calling** est activé pour :
- Identifier les produits recherchés par l'utilisateur.
- Proposer des recommandations adaptées.
- Faciliter la structuration et la spécificité des réponses attendues.

#### Avantages :
- Permet de contrôler le format des réponses de manière précise.
- Gère les cas où aucun produit ne correspond à la demande ou lorsque l'utilisateur ne formule pas de requête explicite (retourne des listes vides dans ces cas).

---

### 2. Recherche de produits pertinents
Le système effectue une recherche dans le dataset en exploitant les embeddings. Cela permet d'identifier les produits les plus pertinents par rapport à la requête.

#### Avantages :
- Approche naturelle pour implémenter le RAG.
- Réponses précises basées sur les produits réellement disponibles.
- Garantit une expérience utilisateur cohérente avec les données stockées.

---

### 3. Mise à jour automatique du panier
Les produits identifiés comme désirés sont ajoutés directement au panier de l'utilisateur.

#### Avantages :
- Fluidifie l'interaction en simulant un comportement naturel.
- Réduit les étapes nécessaires pour compléter une transaction.

---

### 4. Intégration avec MistralAI
Un appel est effectué vers **MistralAI** avec un prompt enrichi qui contient :
- Le contexte de la conversation en cours.
- La liste des produits pertinents et le panier actuel de l'utilisateur.

L'objectif est de générer une réponse IA la plus naturelle possible, tout en s'adaptant à la situation et aux données disponibles.

#### Avantages :
- Optimise la qualité des réponses en exploitant un contexte riche.
- Renforce la pertinence et la personnalisation des échanges.

---

### 5. Récupération et affichage de la réponse
La réponse générée est affichée à l'utilisateur, avec un soin particulier apporté à sa lisibilité et à sa satisfaction.


# Mode d'emploi

## Run l'application:
 - run <code> pip install -r requirements.txt </code>
 - télécharger le fichier *products.csv* et le déplacer dans le dossier *chatbox/data*
 - se mettre dans le dossier où il y a *manage.py* et ouvrir l'invite de commande
 - executer <code> python manage.py runserver </code>


## Parties principales du code :
 - le fichier *index.html* dans *chatbox/templates/chatbox/* : Tout le front-end
 - les fichiers *views.py* et *signals.py* dans *chatbox/* : Tout le début du back-end, notamment le routing et l'appel au back-end
 - les fichiers dans *backend/* : L'essentiel, les appels au modèle, recherche dans le tableau etc...

## Base de donnée de produits : 
  - (brut) https://www.kaggle.com/datasets/thegurusteam/carrefour-es-product-pricing
  - (modifiée) https://drive.google.com/drive/folders/1mNLmqEcR0YqtYqWaVQkWnnedY6BrWDjV
