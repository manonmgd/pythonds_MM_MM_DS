import pandas as pd

# On charge les données
df_top_books_fnac_2023 = pd.read_csv("best_sellers_fnac_2023_cleaned.csv")
df_babelio_top_23 = pd.read_csv("babelio_top_23.csv")
df_livraddict_prix_2024 = pd.read_csv("livraddict_prix_2024.csv")

# Normalisation des titres (supprime les espaces inutiles et met en minuscules)
def normalize_title(title):
    return ' '.join(title.lower().strip().split())

df_fnac['Titre_normalized'] = df_fnac['Titre'].apply(normalize_title)
df_babelio['Titre_normalized'] = df_babelio['Titre'].apply(normalize_title)

# Fusion avec similarité
def find_closest_match(row, target_df, threshold=90):
    """
    Trouve le titre le plus proche en termes de similarité.
    Si aucun titre ne dépasse le seuil, retourne None.
    """
    match, score = process.extractOne(
        row['Titre_normalized'], 
        target_df['Titre_normalized'], 
        scorer=fuzz.ratio
    )
    return match if score >= threshold else None

# Ajouter les correspondances
df_fnac['Match_babelio'] = df_fnac.apply(
    lambda row: find_closest_match(row, df_babelio), axis=1
)

# Marquer les correspondances trouvées
df_fnac['top_babelio'] = df_fnac['Match_babelio'].notna().astype(int)

# Supprimer les colonnes intermédiaires si nécessaire
df_fnac = df_fnac.drop(columns=['Titre_normalized', 'Match_babelio'])
df_babelio = df_babelio.drop(columns=['Titre_normalized'])

# Exporter le résultat
df_fnac.to_csv("merged_top_books.csv", index=False, encoding="utf-8")
print("Merge réalisé et exporté dans 'merged_top_books.csv'")
