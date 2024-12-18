import pandas as pd

# On charge les données
df_top_books_fnac_2023 = pd.read_csv("best_sellers_fnac_2023_cleaned.csv")
df_babelio_top_23 = pd.read_csv("babelio_top_23.csv")
df_livraddict_prix_2024 = pd.read_csv("livraddict_prix_2024.csv")

# On fusionne des bases de données sur la colonne "Titre"
# On utilise un merge progressif pour intégrer toutes les données
merged_data = df_top_books_fnac_2023.merge(df_babelio_top_23, on="Titre", how="outer")\
                                    .merge(df_livraddict_prix_2024, on="Titre", how="outer")

# Gestion des valeurs manquantes
# Vous pouvez choisir de remplacer les valeurs manquantes ou de les laisser telles quelles
merged_data.fillna("Non spécifié", inplace=True)

# Sauvegarde des données fusionnées dans un fichier CSV
merged_data.to_csv("merged_books_data_2023_2024.csv", index=False, encoding="utf-8")
print("Données fusionnées sauvegardées dans 'merged_books_data_2023_2024.csv'.")
