import requests
from bs4 import BeautifulSoup
import pandas as pd

"""Avant de commencer
pip install requests
pip install beautifulsoup4
pip install pandas
pip install html5lib
"""

# On créer une fonction pour scraper une page donnée en ciblant uniquement la section France
def scrape_wikipedia_page_france(year):
    url = f"https://fr.wikipedia.org/wiki/Prix_litt%C3%A9raires_{year}"
    response = requests.get(url)
    response.encoding = "utf-8"  # On garantit le bon encodage
    data = []

    if response.status_code == 200:  # On vérifie si la requête est un succès
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html5lib')

        # On recherche la section France
        france_section = soup.find('h2', string="France")
        if france_section:
            # La liste <ul> qui suit contient les prix pour la France
            france_list = france_section.find_next('ul')

            if france_list:
                # On recherche tous les <li> dans la liste
                prizes = france_list.find_all('li')

                # On extrait les données
                for prize in prizes:
                    # Nom du prix
                    prize_name = prize.find('a')
                    prize_name = prize_name.text.strip() if prize_name else None

                    # Auteur
                    author = prize.find_all('a')
                    author = author[1].text.strip() if len(author) > 1 else None

                    # Titre
                    title = prize.find('i')
                    title = title.text.strip() if title else None

                    # On ajoute les résultats si les données sont complètes
                    if prize_name and author and title:
                        data.append([year, prize_name, author, title])
        else:
            print(f"Section 'France' non trouvée pour l'année {year}")
    else:
        print(f"Erreur lors du scraping de l'année {year}: Status code {response.status_code}")

    return data

# On initialise une liste pour contenir toutes les données
all_data = []

# On Scrappe les pages de 2003 à 2023 uniquement pour la section France
for year in range(2003, 2024):
    print(f"Scraping pour l'année {year}...")
    year_data = scrape_wikipedia_page_france(year)
    all_data.extend(year_data)

# On convertie en DataFrame pandas
df_prix_france = pd.DataFrame(all_data, columns=["Année", "Prix", "Auteur", "Titre"])

# On sauvegarde dans un fichier CSV
df_prix_france.to_csv("prix_litteraires_france_2003_2023.csv", index=False, encoding="utf-8")
print("Scraping terminé. Données sauvegardées dans 'prix_litteraires_france_2003_2023.csv'.")