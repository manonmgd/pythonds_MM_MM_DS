import pandas as pd

# On charge les données
df_top_books_fnac_2023 = pd.read_csv("best_sellers_fnac_2023_cleaned.csv")
df_babelio_top_23 = pd.read_csv("babelio_top_23.csv")
df_livraddict_prix_2024 = pd.read_csv("livraddict_prix_2024.csv")

# on normalise les titres pour ignorer la casse (on convertie en minuscules)
df_top_books_fnac_2023['Titre'] = df_top_books_fnac_2023['Titre'].str.lower()
df_babelio_top_23['Titre'] = df_babelio_top_23['Titre'].str.lower()
df_livraddict_prix_2024['Titre'] = df_livraddict_prix_2024['Titre'].str.lower()

# On fusionne les tables sur la colonne "Titre"
merged_df = df_top_books_fnac_2023.merge(df_babelio_top_23, on="Titre", how="outer")
merged_df = merged_df.merge(df_livraddict_prix_2024, on="Titre", how="outer")

# On crée une colonne unique "Auteur" en priorisant les colonnes existantes
"""
l'idée c'est de créer une colonne unique "Auteur" pour réunir toutes les information d'auteur dans une seule variable
on donne un ordre de priorité: Auteur, Auteur_x, Auteur_y
si une colonne contient une valeur manquante (NaN), elle est remplit par la valeur de la colonne suivante.
La méthode .combine_first() remplit les valeurs manquantes (NaN) de la colonne de gauche (merged_df['Auteur']) 
avec les valeurs correspondantes de la colonne de droite (merged_df['Auteur_x']).
"""
merged_df['Auteur'] = merged_df['Auteur'].combine_first(merged_df['Auteur_x']).combine_first(merged_df['Auteur_y'])

# On supprime les colonnes inutiles "Auteur_x" et "Auteur_y"
merged_df.drop(columns=['Auteur_x', 'Auteur_y'], inplace=True)

# On enregistre le résultat dans un fichier CSV
merged_df.to_csv("merged_books_data.csv", index=False)

#message de fin pour vérifier
Print("fusion terminée")