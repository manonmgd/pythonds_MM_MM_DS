import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL de la page à scrapper
livraddict_top_2023 = "https://www.livraddict.com/prix-livraddict/2024/"

# Requête HTTP vers la page
response = requests.get(livraddict_top_2023)
response.encoding = 'utf-8'

# On vérfie que le site autorise le scraping et on scrap si oui
if response.status_code == 200:  
    soup = BeautifulSoup(response.text, 'html.parser')

    # Liste pour stocker les données extraites
    livraddict_data = []

    # On parcourt toutes les catégories
    categories = soup.find_all('div', class_='categorie_prix portlet light')
    for category in categories:
        # On extrait le nom de la catégorie et supprime "catégorie" devant si présent
        category_name = category.find('h2').text.strip()
        if "catégorie" in category_name.lower():
            category_name = category_name.lower().replace("catégorie", "").strip().capitalize()

        # On parcourt les livres de la catégorie
        books = category.find_all('div', style=lambda x: x and "margin-bottom:10px" in x)
        for book in books:
            # On extrait le titre du livre
            title_tag = book.find('h3').find('a')
            title = title_tag.find('strong').text.strip() if title_tag else None

            # On extrait l'auteur du livre
            author = title_tag.contents[-1].strip() if title_tag else None

            # On ajoute les informations à la liste créée
            if title and author:
                livraddict_data.append([category_name, title, author])

    # On convertit les données en DataFrame
    df_livraddict_data = pd.DataFrame(livraddict_data, columns=['Catégorie', 'Titre', 'Auteur'])

    # On ajoute une colonne indicatrice "top_livraddict"
    df_livraddict_data['top_livraddict'] = 1

    # On affiche le DataFrame
    print(df_livraddict_data)

    # On enregistre les données dans un fichier CSV
    df_livraddict_data.to_csv('livraddict_prix_2024.csv', index=False, encoding='utf-8')
else:
    print(f"Erreur {response.status_code} lors de la requête.")
