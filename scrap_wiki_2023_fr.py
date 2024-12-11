# on scrap les prix littéraires français en 2023

#on importe la bibliothèque requests
import requests
from bs4 import BeautifulSoup # on importe BeautifulSoup
import pandas as pd

#on crée la variable qui va contenir nos données
data_fr_2023 = [] 

#on définit l'url à scrapper
prix_23= "https://fr.wikipedia.org/wiki/Prix_litt%C3%A9raires_2023"

#on crée une variable response qui contient la réponse de notre requette
response_23= requests.get(prix_23)


#response.encoding = "utf-8" #pour afficher correctement les caractères sur le fichier html
response_23.apparent_encoding # pour éviter les utf8 différents entre chq site
response_23.encoding ="utf-8"

#on ajoute un check dans le code si jamais on ne peut pas scrapper
if response_23.status_code == 200: #vérifie que le site autorise à scrapper
    html_23=response_23.text
    print(html_23) #on affiche le contenu html du site pour vérifier
    # tout le code html s'est affiché on va le mettre dans un fichier
    f = open("prix23.html","w")
    f. write(html_23)
    f.close()

    soup = BeautifulSoup(html_23, 'html5lib') # on met la variable et on précise la manière de parcourir le code
    
    # Titre principal
    titre = soup.find("h1").text
    print("Titre:", titre)

    # Rechercher la section France
    france_section = soup.find('h2', id="France")
    if france_section:
        # La section <ul> qui suit contient les prix
        france_list = france_section.find_next('ul')

        if france_list:
            # Rechercher tous les <li> de cette section
            prizes = france_list.find_all('li')
            
            # On extrait les données
            for prize in prizes:
                # On trouve le prix
                prize_name = prize.find('a')
                prize_name = prize_name.text.strip() if prize_name else None

                # On trouve l'auteur
                author = prize.find_all('a')
                if len(author) > 1:
                    author = author[1].text.strip()  # Le deuxième lien est souvent l'auteur
                else:
                    author = None

                # On trouve le titre
                title = prize.find('i')
                title = title.text.strip() if title else None

                # On ajoute les résultats à la liste si les données sont complètes
                if prize_name and author and title:
                    data_fr_2023.append([prize_name, author, title])
    

        # On convertie en dataframe
        df_prix_fr_2023 = pd.DataFrame(data_fr_2023, columns=["Prix", "Auteur", "Titre"])

        # On affiche le dataframe
        print(df_prix_fr_2023)

        #On sauvegarde dans un fichier csv
        df_prix_fr_2023.to_csv("prix_litteraires.csv", index=False)
else:
    print("ERREUR:", response_23.status_code)


print("FIN")
