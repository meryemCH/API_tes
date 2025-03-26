import requests
import pandas as pd
import matplotlib.pyplot as plt
import time
from datetime import datetime

# URL de l'API CoinGecko
url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,litecoin&vs_currencies=usd'

# Définir l'intervalle (en secondes)
interval = 10  

while True:
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        # Convertir en DataFrame
        df = pd.DataFrame.from_dict(data, orient='index')
        df.reset_index(inplace=True)
        df.columns = ['Crypto', 'Price (USD)']
        
        # Ajouter un timestamp
        df['Timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 🎯 Sauvegarde en CSV (ajout sans écraser)
        df.to_csv("crypto_prices.csv", mode='a', index=False, header=False)
        print(f"Données sauvegardées ({df['Timestamp'][0]}) ✅")
        
        # 🎨 Création du graphique
        plt.figure(figsize=(8, 5))
        plt.bar(df['Crypto'], df['Price (USD)'], color=['gold', 'blue', 'gray'])
        plt.xlabel("Cryptomonnaie")
        plt.ylabel("Prix en USD")
        plt.title("Prix des cryptomonnaies (CoinGecko)")
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Affichage du graphique
        plt.show()

    else:
        print(f"Erreur: {response.status_code}")

    # ⏳ Attente avant la prochaine collecte
    print(f"Attente {interval} secondes avant la prochaine mise à jour...\n")
    time.sleep(interval)