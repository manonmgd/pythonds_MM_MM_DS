# Projet Python

**Projet réalisé dans le cadre du cours "Python pour la data science" de la 2e année du cursus ingénieur de l'ENSAE**

Réalisé par [@marieensae](https://github.com/marieensae), [@manonmgd](https://github.com/manonmgd), [@dianesaint](https://github.com/dianesaint)

L'intégralité de l'analyse est disponible [ici](https://github.com/manonmgd/pythonds_MM_MM_DS/blob/main/analyse_de_donn%C3%A9es.ipynb)

Depuis une quinzaine d'années, les réseaux sociaux les plus connus voient se développer des communautés littéraires : Booktube, Bookstagram et plus récemment Booktok. Dans ce projet nous avons voulus explorer l'impact de YouTube (via Booktube) sur les tendances de consommation de livres en 2023 en croisant plusieurs sources de données.


## Prérequis

Tout d'abord, lancer la commande `pip install -r requirements.txt` afin d'installer les packages nécessaires. 

> Rajouter explication de comment configurer l'api ytb


## Méthodologie 

Nous exploitons des données issues de scrapping pour analyser la consommation réelle de livres. Cela inclut les classements mensuels du top 10 des ventes de la Fnac en 2023, le top 23 des livres les plus lus sur Babelio, ainsi que les 100 ouvrages les plus empruntés dans une bibliothèque parisienne. En parallèle, nous avons collecté des informations sur les prix littéraires, en distinguant d'une part les prix institutionnels français des cinq dernières années (provenant de Wikipédia), et d'autre part les livres primés par les internautes sur le réseau social littéraire Livraddict. Enfin, nous avons croiser ces données avec des informations issues de l'API YouTube pour évaluer si les livres populaires en 2023 (qu'ils soient appréciés ou simplement consommés) ont été mis en avant sur la communauté Booktube.

Le scrapper, à chaque fois scrapp et stock dans un fichier csv:
- 23 livres dans la base `babelio.csv`
- 70 livres dans la base `best_sellers_fnac_2023_cleaned.csv`
- 87 livres dans la base `les_livres_les_plus_empruntes_a_paris.csv`
- 86 dans `livraddict_prix_2024.csv`
- 265 livres dans `prix_litteraires.csv`

Une fois les bases de données fusionnées il nous reste 492 livres dans la base `base_finale.csv`

##