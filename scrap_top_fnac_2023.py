import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# On crée une fonction pour scraper une page donnée
def scrape_titles_and_authors(url, month): # cette fonction prend pour argument l'url et le mois
    response = requests.get(url)
    response.encoding = "utf-8"  # pour garantir le bon encodage
    data = [] #on crée une liste vide où on va mettre les données scrappées

    if response.status_code == 200:  # On vérifie si la requête est un succès
        soup = BeautifulSoup(response.text, 'html5lib') #on précie la manière de parcourir le code

        # On recherche toutes les balises <h2> avec la classe "title-part"
        titles = soup.find_all('h2', class_='title-part')
        for title in titles:
            raw_text = title.text.strip()  # Texte brut pour manipulation

            # Debugging : Afficher le texte brut
            print(f"Texte brut extrait : {raw_text}")

            # On fait un regex pour extraire les informations car on a remarqué que les pages étaient structurées de la même façon classement-titre-auteur,co-auteur (edition)
            match = re.match(r'^(\d+)\s[–—]\s(.+?)\s[–—]\s(.+?)(?:,\s(.+?))?\s\((.+?)\)$', raw_text)
            if match:
                classement = match.group(1).strip()  # Classement
                titre = match.group(2).strip()  # Titre
                auteur_principal = match.group(3).strip()  # Auteur principal
                co_auteur = match.group(4).strip() if match.group(4) else None  # Co-auteur (facultatif)
                maison_edition = match.group(5).strip()  # Maison d'édition

                # Debugging : Afficher les informations extraites
                print(f"Classement : {classement}, Titre : {titre}, Auteur principal : {auteur_principal}, Co-auteur : {co_auteur}, Maison d'édition : {maison_edition}")

                # On ajoute les données dans la liste
                data.append([month, classement, titre, auteur_principal, co_auteur, maison_edition])
    else:
        print(f"Erreur lors du scraping de {month}: Status code {response.status_code}")

    return data

# Liste des URLs et des mois correspondants
urls_months = [
    ("https://leclaireur.fnac.com/selection/cp50350-top-10-les-best-sellers-du-mois-de-janvier-2023/", "Janvier"),
    ("https://leclaireur.fnac.com/selection/cp50709-top-10-les-best-sellers-du-mois-de-fevrier-2023/", "Février"),
    ("https://leclaireur.fnac.com/selection/cp43551-top-10-les-best-sellers-de-mars-2023/", "Mars"),
    ("https://leclaireur.fnac.com/selection/cp44047-top-10-les-best-sellers-davril-2023/", "Avril"),
    ("https://leclaireur.fnac.com/selection/cp48182-top-10-les-best-sellers-de-mai-2023/", "Mai"),
    ("https://leclaireur.fnac.com/selection/cp48395-top-10-les-best-sellers-de-juin-2023/", "Juin"),
    ("https://leclaireur.fnac.com/selection/cp40500-top-10-les-best-sellers-de-juillet-2023/", "Juillet"),
    ("https://leclaireur.fnac.com/selection/cp48936-top-10-les-best-sellers-du-mois-daout-2023/", "Août"),
    ("https://leclaireur.fnac.com/selection/cp49107-top-10-les-best-sellers-du-mois-de-septembre-2023/", "Septembre"),
    ("https://leclaireur.fnac.com/selection/cp49482-top-10-les-best-sellers-du-mois-doctobre-2023/", "Octobre"),
    ("https://leclaireur.fnac.com/selection/cp53758-top-10-les-best-sellers-du-mois-de-novembre-2023/", "Novembre"),
    ("https://leclaireur.fnac.com/selection/cp49831-top-10-les-best-sellers-du-mois-de-decembre-2023/", "Décembre"),
]

# On initialise la liste pour toutes les données
top_data_2023 = []

# On scrape chaque URL
for url, month in urls_months:
    print(f"Scraping pour le mois de {month}...")
    month_data = scrape_titles_and_authors(url, month)
    top_data_2023.extend(month_data)

# On convertit les données en DataFrame pandas
df_top_books_2023 = pd.DataFrame(top_data_2023, columns=["Mois", "Classement", "Titre", "Auteur", "Co-auteur", "Maison d'édition"])

# Création de la variable indicatrice "top_fnac_1" (tous les livres ont un classement)
df_top_books_2023['top_fnac_1'] = 1

# Comptage des occurrences des livres pour créer "top_fnac_2_plus"
counts = df_top_books_2023['Titre'].value_counts()
df_top_books_2023['top_fnac_2_plus'] = df_top_books_2023['Titre'].apply(lambda x: 1 if counts[x] > 1 else 0)

# Suppression des colonnes "Mois" et "Classement", et suppression des doublons
df_top_books_2023 = df_top_books_2023.drop(columns=["Mois", "Classement"]).drop_duplicates(subset=['Titre'])

# On affiche le DataFrame
print(df_top_books_2023)

# On sauvegarde dans un fichier CSV
df_top_books_2023.to_csv("best_sellers_fnac_2023_cleaned.csv", index=False, encoding="utf-8")
print("Données sauvegardées dans 'best_sellers_fnac_2023_cleaned.csv'.")
