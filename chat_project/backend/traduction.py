import pandas as pd 
import os
from mistralai import Mistral


def traduction(chaine_de_caractere):
    
    api_key = "Ayt9pyjjA1Y2Tltpu85aUyJXu6EcflT8"
    model = "mistral-small-latest"

    client = Mistral(api_key=api_key)
    chat_response = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
                "content": "Traduis moi la phrase en espagnol:'"+ chaine_de_caractere + "'. le return doit etre uniquement la phrase en espagnol. ",
            },
        ]
    )
    return chat_response.choices[0].message.content
    
    