import requests
import pandas as pd

# URL de l'API CoinGecko pour obtenir les prix des cryptos
url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,litecoin&vs_currencies=usd'

response = requests.get(url)

# Vérifier que la requête a bien réussi
if response.status_code == 200:
    data = response.json()
    # Créer un DataFrame pandas pour faciliter l'analyse
    df = pd.DataFrame.from_dict(data, orient='index')
    print("Données récupérées :")
    print(df)  # Affiche les prix des cryptos

else:
    print(f"Erreur: {response.status_code}")
