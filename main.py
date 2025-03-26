import requests
import pandas as pd
import matplotlib.pyplot as plt
import time
from datetime import datetime

# URL de l'API CoinGecko
coingecko_url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,litecoin&vs_currencies=usd'

# URL de l'API Binance (modèle pour toutes les cryptos)
binance_url_template = 'https://api.binance.com/api/v3/ticker/price?symbol={}USDT'

# Définir l'intervalle (en secondes)
interval = 10  

# Cryptos à comparer
cryptos = ['BTC', 'ETH', 'LTC']  # Symboles pour Binance

while True:
    # 📡 Récupérer les données de CoinGecko
    coingecko_response = requests.get(coingecko_url)

    # 📡 **Récupérer les données de Binance**
    binance_data = {}
    for crypto in cryptos:
        binance_response = requests.get(binance_url_template.format(crypto))
        if binance_response.status_code == 200:
            binance_data[crypto.lower()] = float(binance_response.json()['price'])

    # Vérifier que la requête CoinGecko a bien réussi
    if coingecko_response.status_code == 200:
        coingecko_data = coingecko_response.json()
        
        # Convertir en DataFrame pour CoinGecko
        df = pd.DataFrame.from_dict(coingecko_data, orient='index')
        df.reset_index(inplace=True)
        df.columns = ['Crypto', 'Price (CoinGecko USD)']
        
        # Ajouter les données de Binance
        df['Price (Binance USD)'] = df['Crypto'].apply(lambda x: binance_data.get(x, 'N/A'))
        
        # Ajouter un timestamp
        df['Timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 🎯 Sauvegarde en CSV (ajout sans écraser)
        df.to_csv("crypto_prices.csv", mode='a', index=False, header=False)
        print(f"Données sauvegardées ({df['Timestamp'][0]}) ✅")

        # 🎨 Création du graphique
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Largeur des barres
        width = 0.35  
        
        # Position des barres
        x = range(len(df))

        # Barres pour CoinGecko et Binance
        ax.bar([i - width / 2 for i in x], df['Price (CoinGecko USD)'], width, label='CoinGecko', color='gold')
        ax.bar([i + width / 2 for i in x], df['Price (Binance USD)'], width, label='Binance', color='blue')

        # Ajouter des labels et un titre
        ax.set_xlabel('Cryptomonnaie')
        ax.set_ylabel('Prix en USD')
        ax.set_title('Comparaison des prix des cryptomonnaies (CoinGecko vs Binance)')
        ax.set_xticks(x)
        ax.set_xticklabels(df['Crypto'])
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        ax.legend()

        # Affichage du graphique
        plt.show()

    else:
        print(f"Erreur CoinGecko: {coingecko_response.status_code}")

    # ⏳ Attente avant la prochaine collecte
    print(f"Attente {interval} secondes avant la prochaine mise à jour...\n")
    time.sleep(interval)
