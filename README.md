# Hackaton-X-IA

## Run l'application:

 - se mettre dans le dossier où il y a *requirements.txt* et ouvrir l'invite de commande
 - executer <code> pip install -r requirements.txt </code>
 - télécharger le fichier *products.csv* et le déplacer dans le dossier *chatbox/data*
 - se mettre dans le dossier où il y a *manage.py* et ouvrir l'invite de commande
 - executer <code> python manage.py runserver </code>


## Parties principales du code :
 - le fichier *index.html* dans *chatbox/templates/chatbox/* : Tout le front-end
 - les fichiers *views.py* et *signals.py* dans *chatbox/* : Tout le début du back-end, notamment le routing et l'appel au back-end
 - les fichiers dans *backend/* : L'essentiel, les appels au modèle, recherche dans le tableau etc...

## Base de donnée de produits : 
  https://www.kaggle.com/datasets/thegurusteam/carrefour-es-product-pricing

## Pitch :
Notre application permet de passer une commande d'alimentaire en intéraction avec un chatbot.

### Fonctionnalités:
 - Gestion (semi)-automatique du panier.
 - Recommendations éventuelles sur la demande de l'utilisateur.
 - Chatbot géré par MistralAi.

