import pandas as pd 
import os
from mistralai import Mistral
from backend.call import *

def traduction(chaine_de_caractere):
    prompt = "Traduis moi la phrase en espagnol:'"+ chaine_de_caractere + "'. le return doit etre uniquement la phrase en espagnol. "
    trad = call(prompt)
    return trad
    
    