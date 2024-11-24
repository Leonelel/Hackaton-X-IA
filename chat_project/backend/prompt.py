## ICI tous les prompts


def get_prompt(input, produit, contexte=''):
    prompt = f"Tu es un assistant pour vendre essentiellement des produits alimentaires mais egalement des produits qu'on trouve dans des grandes surfaces comme carrefour, ici la demande du user est ({input}) et il se trouve que tu as le produit {produit} a lui proposer tu devras donc repondre au client de manière adéquat dans la même langue que sa requête, de confirmer ou non l'ajout du produit {produit} dans sa liste de course."

    return prompt

def get_prompt_liste(input, contexte=''):
    prompt = f"je vais te donner une phrase et tu vas devoir me renvoyer uniquement les aliments contenus dans la phrase sous la forme d'une liste python, c'est à dire ['...','...'] par exemple. La phrase est '"+input+"'. Si la demande est une recette, n'hésite pas à ajouter à la liste les ingrédients nécéssaire pour cette recette en ESPAGNOL. Dans ce cas il faut que tu retournes UNIQUEMENT une reponse de la forme liste python."
    return prompt