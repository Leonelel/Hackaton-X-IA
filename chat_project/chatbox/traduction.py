import pandas as pd 
import os
from mistralai import Mistral
from backend.call import *

def traduction(chaine_de_caractere, langue='espagnol'):
    prompt = "Traduis moi la phrase en "+ langue + ":'"+ chaine_de_caractere + f"'. le return doit etre uniquement la phrase en {langue}. "
    trad = call(prompt)
    return trad
    
