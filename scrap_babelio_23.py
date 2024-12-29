# On scrap le top 23 de 2023 de babelio

import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL de la page à scrapper
babelio_top_2023 = "https://www.babelio.com/article/2543/Les-23-livres-les-plus-populaires-de-2023"

# on fait la requête HTTP vers la page
response = requests.get(babelio_top_2023)

# On utilise l'encodage détecté par requests
response.encoding = response.apparent_encoding

if response.status_code == 200:  # Vérifie que le site autorise le scraping
    soup = BeautifulSoup(response.text, 'html.parser')

    # Liste pour stocker les données extraites
    babelio_data = []

    # On trouve toutes les sections contenant les livres
    titles_sections = soup.find_all('span', class_='titre_global')
    for section in titles_sections:
        # On extrait le titre
        title_tag = section.find('a')
        title = title_tag.text.strip() if title_tag else None

        # On extrait l'auteur
        author_text = section.text.split("de")[-1].strip() if "de" in section.text else None
        author = author_text.split("\n")[0] if author_text else None

        # Ajouter aux données si titre et auteur sont présents
        if title and author:
            babelio_data.append([title, author])

    # On convertie les données en DataFrame
    df_babelio_data = pd.DataFrame(babelio_data, columns=['Titre', 'Auteur'])

    # Ajout de la colonne indicatrice "top_babelio"
    df_babelio_data['top_babelio'] = 1

    # On affiche le DataFrame
    print(df_babelio_data)

    # On enregistre les données dans un fichier CSV
    df_babelio_data.to_csv('babelio_top_23.csv', index=False, encoding='utf-8-sig')  # UTF-8-SIG pour compatibilité Excel
else:
    print(f"Erreur {response.status_code} lors de la requête.")

