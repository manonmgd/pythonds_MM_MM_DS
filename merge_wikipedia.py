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
df_intermediaire = pd.merge(
    prix_litteraires_data, 
    merged_books_data, 
    on="Titre",  # Fusion sur la colonne "Titre"
    how="outer"  # Conserve tous les livres des deux DataFrames
)

# On crée une seule colonne "Auteur" en priorisant "Auteur_y" puis "Auteur_x"
df_intermediaire['Auteur'] = df_intermediaire['Auteur_y'].combine_first(df_intermediaire['Auteur_x'])

# Extraction de "Co_auteur1" et modification de "Auteur"
def extraire_co_auteur(auteur):
    if isinstance(auteur, str):
        # Utilisation d'une expression régulière pour extraire la partie après "et"
        match = re.search(r"\bet\b\s*(.*)", auteur)
        if match:
            return match.group(1).strip()
    return None

# Créer une nouvelle colonne "Co_auteur1"
df_intermediaire['Co_auteur1'] = df_intermediaire['Auteur'].apply(extraire_co_auteur)

# Supprimer "et" et ce qui suit dans "Auteur"
df_intermediaire['Auteur'] = df_intermediaire['Auteur'].str.replace(r"\bet\b.*", "", regex=True).str.strip()

# Supprimer les colonnes inutiles "Auteur_x" et "Auteur_y"
df_intermediaire.drop(columns=['Auteur_x', 'Auteur_y'], inplace=True)


#on regarde les différentes variables
print(df_intermediaire.columns)


"""
A partir d'ici je vais reprendre avec la nouvelle table bibli donc il faudra le placer après le merge bibli
"""

# On transforme en variables binaires prix_19_20, top_babelio, top_fnac_1, top_fnac_2_plus
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

#on va nettoyer un a un les problèmes persistants qui sont liés à des titres écrits de façon différente
"""
il y a des moments où on a des des problèmes de fusion donc on voudrait modifier à la main les données, 
l'idée est de fusionner les deux titres en double avec leurs données (on garde le titre du premier, 
pour les variables vides si une des deux n'a pas la variable vide on garde celle pas vide et pour celles qui valent 0 ou 1 
on garde celle qui vaut 1). 
"""
# Paires à fusionner
pairs = [
    ("astérix tome 40 : l’iris blanc", "astérix, tome 40 : l’iris blanc"),
    ("beyond the story : 10 ans de souvenirs de bts (beyond the story: 10-year record of bts)", "beyond the story, 10 ans de souvenirs de bts"),
    ("bleak", "bleak, 3 histoires d’horreur volume 2"),
    ("captive t1", "captive, tome 1"),
    ("elles, tome 3 : plurielle(s)", "elles, tome 3 : plurielle(s)"),
    ("la femme de ménage", "la femme de ménage, tome 1 (the housemaid, book 1)"),
    ("la nuit où les étoiles ses sont éteintes t1", "la nuit où les étoiles ses sont éteintes, tome 1"),
    ("les cahiers d’esther, tome 8 : histoires de mes 17 ans", "les cahiers d’esther, tome8 : histoires de mes 17 ans"),
    ("les sept surs, tome 8 : atlas, l'histoire de pa salt", "les sept sœurs : atlas, l’histoire de pa salt"),
    ("lou ! sonata, tome 2", "lou, tome 2 : sonata"),
    ("mortelle adèle et les reliques du chat lune, tome 4", "mortelle adèle, tome 4 : v.i.b"),
]

# Fonction pour fusionner deux lignes
def merge_rows(row1, row2):
    merged = []
    for col in df_final.columns:
        if col == "Titre":
            merged.append(row2[col])  # Toujours garder le titre du deuxième
        elif col in ["top_fnac_1", "prix_19_20", "top_fnac_2_plus", "top_babelio", "top_livraddict", "any_top_indicator"]:
            # Pour les colonnes binaires, on garde 1 si l'un des deux a 1
            merged.append(max(row1[col], row2[col]))
        else:
            # Garder la valeur non nulle si elle existe
            merged.append(row1[col] if pd.notnull(row1[col]) else row2[col])
    return merged

# Créer une nouvelle table avec les données fusionnées
merged_data = []

for pair in pairs:
    title1, title2 = pair
    rows1 = df_final[df_final["Titre"] == title1]
    rows2 = df_final[df_final["Titre"] == title2]

    if not rows1.empty and not rows2.empty:
        row1 = rows1.iloc[0]
        row2 = rows2.iloc[0]
        merged_data.append(merge_rows(row1, row2))
    else:
        print(f"Warning: One of the titles not found for pair: {pair}")

# Convertir les données fusionnées en DataFrame
merged_df = pd.DataFrame(merged_data, columns=df_final.columns)

# Mettre à jour le DataFrame de base avec les données fusionnées
for row in merged_data:
    title = row[df_final.columns.get_loc("Titre")]
    df_final = df_final[df_final["Titre"] != title]  # Supprimer les anciennes entrées correspondantes
    df_final = pd.concat([df_final, pd.DataFrame([row], columns=df_final.columns)], ignore_index=True)

# Sauvegarder le DataFrame mis à jour dans le fichier CSV
df_final.to_csv("df_final_updated.csv", index=False, encoding='utf-8')

print("Fusion terminée et fichier mis à jour sauvegardé sous 'df_final_updated.csv'.")
