import pandas as pd 
import os
from mistralai import Mistral

## modèle big : open-mistral-7b
def call(prompt, model="mistral-small-latest"):
    
    api_key = "Ayt9pyjjA1Y2Tltpu85aUyJXu6EcflT8"

    client = Mistral(api_key=api_key)
    chat_response = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
                "content": prompt,
            },
        ]
    )
    return chat_response.choices[0].message.content