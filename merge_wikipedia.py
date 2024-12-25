"""
Dans ce code on essaie de merge les tables qu'on a (merged_books_data.csv) avec les données scrappées de wikipedia
"""

import pandas as pd

# Chargement du fichier merged_books_data.csv
merged_books_data = pd.read_csv("merged_books_data.csv", encoding="utf-8")

# Nettoyage des colonnes "Titre" dans les deux DataFrames
df_top_books_2023['Titre'] = df_top_books_2023['Titre'].str.strip().str.lower()  # Nettoyer et convertir en minuscule
merged_books_data['Titre'] = merged_books_data['Titre'].str.strip().str.lower()  # Même nettoyage

# Fusion des deux DataFrames sur "Titre"
df_final = pd.merge(
    df_top_books_2023, 
    merged_books_data, 
    on="Titre",  # Fusion sur la colonne "Titre"
    how="left"   # Conserver tous les livres de df_top_books_2023, même sans correspondance
)

# Afficher le résultat de la fusion
print(df_final)

# Sauvegarde dans un fichier CSV
df_final.to_csv("final_merged_books_data.csv", index=False, encoding="utf-8")
print("Données fusionnées sauvegardées dans 'final_merged_books_data.csv'.")
