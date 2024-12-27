#On importe la bibliothèque pandas
import pandas as pd
import matplotlib.pyplot as plt

#On charge les tables dont on a besoin\n",
books_data = pd.read_csv("livraddict_prix_2024.csv", encoding="utf-8")
youtube_data = pd.read_csv("youtube_livre_2019_2023.csv", encoding="utf-8")

# ------------ Analyse des vidéos youtubes sur les livres -------------
print("\n--- Analyse des vidéos youtube sur les livres ---")

# Convertir la colonne 'description' en type string
youtube_data['description'] = youtube_data['description'].astype(str)

# Initialiser une nouvelle liste pour stocker les résultats
result = []

# Fonction pour vérifier si une liste est une sous-liste dans une autre


# Itérer sur chaque liste de la colonne 'col1' de df1
for index1, row1 in books_data.iterrows():
    count_list = []  # Liste pour stocker les résultats de cette ligne

    # Itérer sur chaque liste de la colonne 'col2' de df2
    for index2, row2 in youtube_data.iterrows():
        # Vérifier si la liste de df1 (row1['col1']) est une sous-liste de la liste de df2 (row2['col2'])
        if row1['Titre'] in row2['description']: # Fonction pour vérifier si une liste est une sous-liste dans une autre
            count_list.append(1)  # Si elle est incluse, compter une occurrence
        else:
            count_list.append(0)  # Sinon, aucune occurrence
# Ajouter la liste de df1, les résultats dans la nouvelle liste, et la somme des occurrences
    result.append([row1['Titre'], sum(count_list)])  # Ajouter la somme et la liste de df1

# Créer la nouvelle DataFrame contenant les résultats
colonnes=['df1_list', 'somme']#+[f"youtube_data_list_{i}" for i in range(len(youtube_data))]
result_df = pd.DataFrame(result, columns = colonnes )

# Afficher le DataFrame final
# print(result_df)

# Filtrer les lignes où 'somme' est différente de 0
filtered_df = result_df[result_df['somme'] != 0]

# Afficher le DataFrame filtré
print(filtered_df)

# --- Analyse des vidéos youtube sur les livres avec prix_litteraires.csv et youtube_livre_2019_2023.csv ---
# df1_list  somme
# 38   À la ligne      1
# 39   À la ligne      1
# 123  À la ligne      1

# --- Analyse des vidéos youtube sur les livres avec livraddict_prix_2024.csv et youtube_livre_2019_2023.csv ---
# df1_list  somme
# 49    Babel      1
