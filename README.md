# Projet Python

**Projet réalisé dans le cadre du cours "Python pour la data science" de la 2e année du cursus ingénieur de l'ENSAE**

Réalisé par [@marieensae](https://github.com/marieensae), [@manonmgd](https://github.com/manonmgd), [@dianesaint](https://github.com/dianesaint)

L'intégralité de l'analyse est disponible [ici](https://github.com/manonmgd/pythonds_MM_MM_DS/blob/main/analyse_de_donn%C3%A9es.ipynb)

Chaque année, les livres reçoivent des centaines de prix littéraires, témoins de leur qualité, de leur impact ou de leur originalité. Cependant, ces distinctions ne sont pas les seuls moteurs de la popularité des ouvrages : l'influence des réseaux sociaux, comme YouTube à travers sa communauté "Booktube", joue un rôle croissant dans la mise en avant de certains livres auprès du grand public. Ce projet vise à identifier les déterminants de la popularité des livres en combinant l'étude des prix littéraires et l'analyse de l'impact des influenceurs sur YouTube.

<div style="
    font-family: 'Arial', sans-serif; 
    text-align: center; 
    padding: 10px; 
    background-color:rgb(210, 199, 255); 
    color: black; 
    border-radius: 5px; 
    font-size: 1.5em;
">
    <strong>Prérequis</strong>
</div>


Tout d'abord, lancer la commande `pip install -r requirements.txt` afin d'installer les packages nécessaires. 

### Creation d'un projet sur Google Cloud Console

**Pour utiliser, la YouTube Data API v3 qui nous servira par la suite, il est nécessaire de créer un projet sur Google Cloud Console.**

Etape 1 : Créer un projet sur Google Cloud Console
-Aller sur [la Google Cloud Console](https://console.cloud.google.com).
-Créer un nouveau projet en cliquant sur "Select a project" puis "New Project".
-Donner un nom à votre projet et cliquer sur "Create".

Etape 2 : Activer l'API YouTube Data
-Aller dans le "API & Services" > "Library" dans la Google Cloud Console.
-Chercher YouTube Data API v3 et cliquez dessus.
-Cliquer sur "Enable" pour activer l'API.

Etape 3 : Créer des identifiants pour l'API
- Aller dans "API & Services" > "Credentials".
- Cliquer sur "Create Credentials" et choisir "API key".
- L'API key générée apparaîtra. Copier cette clé, vous en aurez besoin pour effectuer des requêtes.

<div style="
    font-family: 'Arial', sans-serif; 
    text-align: center; 
    padding: 10px; 
    background-color:rgb(210, 199, 255); 
    color: black; 
    border-radius: 5px; 
    font-size: 1.5em;
">
    <strong>Méthodologie </strong>
</div>


<div style="
    font-family: 'Arial', sans-serif; 
    text-align: center; 
    padding: 10px; 
    background-color:rgb(210, 199, 255); 
    color: black; 
    border-radius: 5px; 
    font-size: 1.5em;
">
    <strong> Récupération et traitement des données </strong>
</div>

Le détail de la création de la base de donnée se trouve dans [ce fichier](https://github.com/manonmgd/pythonds_MM_MM_DS/blob/main/cr%C3%A9ation_base.ipynb)

Nous exploitons des données issues de scrapping et d'API pour analyser la consommation réelle de livres. Cela inclut les  classements mensuels du top 10 des ventes de la Fnac en 2023, le top 23 des livres les plus lus sur Babelio, ainsi que les 100 ouvrages les plus empruntés dans une bibliothèque parisienne. En parallèle, nous avons collecté des informations sur les prix littéraires, en distinguant d'une part les prix institutionnels français des cinq dernières années (provenant de Wikipédia), et d'autre part les livres primés par les internautes sur le réseau social littéraire Livraddict. Enfin, nous avons croisé ces données avec des informations issues de l'API YouTube pour évaluer si les livres populaires en 2023 (qu'ils soient appréciés ou simplement consommés) ont été mis en avant sur la communauté Booktube.

Le scrapper, à chaque fois scrapp et stock dans un fichier csv:
- 23 livres dans la base `babelio.csv`
- 70 livres dans la base `best_sellers_fnac_2023_cleaned.csv`
- 86 dans `livraddict_prix_2024.csv`
- 265 livres dans `prix_litteraires.csv`

Dans l'API de la bibliothèque nous avons récupéré les 100 emprunts les plus fréquents auxquels nous avons retiré les DVD. Nous avons donc 87 livres dans la base `les_livres_les_plus_empruntes_a_paris.csv`

Une fois les bases de données fusionnées il nous reste 492 livres dans la base `base_finale.csv`

Dans l'API youtube, on a pu récupéré les titres, descriptions, sous-titres et dates de publication de vidéos youtube portant sur des livres. On s'est intéressé aux vidéos publiées entre 2019 et 2023 et aux vidéos portant sur des livres sortis en 2023 pour créer des bases de données de vidéos youtube. On a ensuite cherché les titres et noms d'auteurs des livres (de nos bases de données de livres créées précédemment) dans les descriptions et sous-titres des vidéos (de nos bases de données de vidéos youtube). On a ainsi pu noter les nombres d'occurrences dans les différentes bases de données de vidéos pour les différentes bases de données de livres afin d'estimer le nombre de vidéos youtube portant sur les livres de nos bases de données de livre.
Nous avons également utilisé l'API youtube afin de récupérer les descriptions et sous-titres des videos qui pourraient mentionner les livres de notre base. La `base_finale_with_youtube.csv` contient donc les mêmes données que la base_finale.csv` enrichie des données de youtube. 

## Visualisation et analyse descriptive

Le détail de la partie visualisation et analyse descripte se trouve dans [ce fichier](https://github.com/manonmgd/pythonds_MM_MM_DS/blob/main/analyse_de_donn%C3%A9es.ipynb)

Dans cette partie, nous effecctuons les statistiques descriptives afin de décrire les données disponibles et commencer à croiser certaines variables que nous utiliserons ensuite pour la modélisation. On regarde si les livres populaires sont mieux représentés ou non dans les listes de prix littéraires ou dans les classements de qualité faits par les internautes.On regarde la place des livres primés dans les différents top. On s'intéresse également à la proportion de livres mentionnées sur Youtube en fonction des différents top et prix. 

## Modélisation


## Conclusion

