"""
Dans ce code on essaie de merge les tables qu'on a (merged_books_data.csv) avec les données scrappées de wikipedia
"""
import pandas as pd
import re

# On charge les fichiers
merged_books_data = pd.read_csv("merged_books_data.csv", encoding="utf-8")
prix_litteraires_data = pd.read_csv("prix_litteraires.csv", encoding="utf-8")

#On rajoute une variable indicatrice dans la table des prix
prix_litteraires_data['prix_19_20'] = 1
print(prix_litteraires_data.head(10))

# On nettoie la colonne "Titre" pour le deuxième DataFrame en mettant tout en minuscule
prix_litteraires_data['Titre'] = prix_litteraires_data['Titre'].str.strip().str.lower()

# On fusionne les deux DataFrames sur "Titre" en conservant tous les livres des deux tables
df_final = pd.merge(
    prix_litteraires_data, 
    merged_books_data, 
    on="Titre",  # Fusion sur la colonne "Titre"
    how="outer"  # Conserve tous les livres des deux DataFrames
)

# On crée une seule colonne "Auteur" en priorisant "Auteur_y" puis "Auteur_x"
df_final['Auteur'] = df_final['Auteur_y'].combine_first(df_final['Auteur_x'])

# Extraction de "Co_auteur1" et modification de "Auteur"
def extraire_co_auteur(auteur):
    if isinstance(auteur, str):
        # Utilisation d'une expression régulière pour extraire la partie après "et"
        match = re.search(r"\bet\b\s*(.*)", auteur)
        if match:
            return match.group(1).strip()
    return None

# Créer une nouvelle colonne "Co_auteur1"
df_final['Co_auteur1'] = df_final['Auteur'].apply(extraire_co_auteur)

# Supprimer "et" et ce qui suit dans "Auteur"
df_final['Auteur'] = df_final['Auteur'].str.replace(r"\bet\b.*", "", regex=True).str.strip()

# Supprimer les colonnes inutiles "Auteur_x" et "Auteur_y"
df_final.drop(columns=['Auteur_x', 'Auteur_y'], inplace=True)


#on regarde les différentes variables
print(df_final.columns)

#on transforme en variables binaires prix_19_20, top_babelio, top_fnac_1, top_fnac_2_plus
variables_binaires = ['prix_19_20', 'top_fnac_1', 'top_fnac_2_plus', 'top_babelio', 'top_livraddict']

for var in variables_binaires:
    # on vérifie si la colonne existe dans le DataFrame pour éviter des erreurs
    if var in df_final.columns:
        df_final[var] = df_final[var].apply(lambda x: 1 if x == 1 else 0)

# Affichage pour vérifier qu'on a bien des variables binaires
print(df_final[variables_binaires].head(10))

# On crée une nouvelle variable binaire qui vaut 1 si un livre est au moins dans un des top et 0 sinon
df_final['any_top_indicator'] = (
    (df_final['top_fnac_1'] == 1) |
    (df_final['top_babelio'] == 1) |
    (df_final['top_livraddict'] == 1)
).astype(int)

# on affiche pour vérification
print(df_final[['top_fnac_1', 'top_babelio', 'top_livraddict', 'any_top_indicator']].head(10))


# Afficher le résultat de la transformation
print(df_final.head(10))

# Sauvegarder dans un fichier CSV
df_final.to_csv("final_merged_books_data.csv", index=False, encoding="utf-8")
print("Données fusionnées sauvegardées dans 'final_merged_books_data.csv'.")
