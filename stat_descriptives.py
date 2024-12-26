#On importe la bibliothèque pandas
import pandas as pd
import matplotlib.pyplot as plt

#On charge la table dont on a besoin\n",
final_data = pd.read_csv("final_merged_books_data.csv", encoding="utf-8")

# ------------ Analyse des prix littéraires -------------
print("\n--- Analyse des prix littéraires ---")

prix_counts = final_data['prix_19_20'].value_counts()
prix_proportions = final_data['prix_19_20'].value_counts(normalize=True) * 100

print("Nombre de livres ayant reçu un prix littéraire :")
print(prix_counts)
print("\nProportion de livres ayant reçu un prix littéraire (%):")
print(prix_proportions)

# presque 1/3 des livres dans notre base a reçu un prix littéraire

# Visualisation des prix littéraires
prix_counts.plot(kind='bar', title='Livres avec ou sans prix littéraire', ylabel='Nombre de livres', xlabel='Prix littéraire (1=oui, 0=non)')
plt.show()

# ------------ Analyse des tops -------------
print("\n--- Analyse des tops ---")

# Comptage et proportions pour chaque top
tops = ['top_fnac_1', 'top_fnac_2_plus', 'top_babelio', 'top_livraddict', 'any_top_indicator']
for top in tops:
    print(f"\nAnalyse pour {top}:")
    counts = final_data[top].value_counts()
    proportions = final_data[top].value_counts(normalize=True) * 100
    print(f"Nombre de livres :\n{counts}")
    print(f"Proportions (%):\n{proportions}")

"""
Sur les 229 livres
78 des livres sont dans au moins un top fnac du mois
28 sont dans 2 top fnac ou plus (on eté plusieurs mois d'affilé dans le top fnac)
25 sont dans le top babelio 2023
85 sont dans le top livraddict 2023

59 sont dans au moins un des top fnac, babelio ou livraddict
"""

# Visualisation
title = "nombre de livres par top"
counts.plot(kind='bar', title=f'Présence dans {top}', ylabel='Nombre de livres', xlabel=f'{top} (1=oui, 0=non)')
plt.show()

# ------------ Prix et présence dans les tops -------------
"""
on croise prix_19_20 avec any_top_indicator 
pour afficher la proportion de livres primés présents ou non dans les tops
"""

print("\n--- Prix et présence dans les tops ---")

prix_et_any_top = pd.crosstab(final_data['prix_19_20'], final_data['any_top_indicator'], normalize='index') * 100

print("Proportion de livres primés présents ou non dans les tops (%):")
print(prix_et_any_top)

prix_et_any_top.plot(kind='bar', stacked=True, title='Prix littéraire et présence dans les tops', ylabel='Proportion (%)', xlabel='Prix littéraire (1=oui, 0=non)')
plt.show()

"""
Parmi les livres primés (prix_19_20 = 1), seulement 7.81% sont 
présents dans un top, tandis que 92.19% ne figurent dans aucun top. 
Cela suggère que les livres primés ne sont pas nécessairement plus représentés 
dans les tops par rapport aux livres non primés.
"""

# ------------ Fréquence des auteurs -------------
print("\n--- Fréquence des auteurs ---")

auteur_counts = final_data['Auteur'].value_counts()

print("Nombre de livres par auteur :")
print(auteur_counts)

auteur_counts.head(10).plot(kind='bar', title='Top 10 des auteurs par nombre de livres', ylabel='Nombre de livres', xlabel='Auteur')
plt.show()

"""
Les auteurs Sarah Rivens et Mr Tan se démarquent avec 4 livres chacun, 
suivis par Sibylle Grimbert et Neige Sinno avec 3 livres. Cependant, la majorité des 204 auteurs 
n'ont écrit qu'un seul livre, illustrant une forte diversité mais une faible répétition dans 
les contributions des auteurs.
"""

# ------------ Livres présents dans plusieurs tops -------------
print("\n--- Livres présents dans plusieurs tops ---")
tops_columns = ['top_fnac_1', 'top_babelio', 'top_livraddict']
final_data['multiple_tops'] = (final_data[tops_columns].sum(axis=1) >= 2).astype(int)
multiple_tops_counts = final_data['multiple_tops'].value_counts()
multiple_tops_proportions = final_data['multiple_tops'].value_counts(normalize=True) * 100

print("Nombre de livres présents dans au moins deux tops :")
print(multiple_tops_counts)
print("\nProportion de livres présents dans au moins deux tops (%):")
print(multiple_tops_proportions)

multiple_tops_counts.plot(kind='bar', title='Livres présents dans au moins deux tops', ylabel='Nombre de livres', xlabel='Présence dans plusieurs tops (1=oui, 0=non)')
plt.show()

"""
Seulement 17 livres (7,42%) sont présents dans au moins deux tops, 
tandis que la grande majorité (212 livres, 92,58%) n’apparaissent que 
dans un seul top ou aucun. Cela montre que peu de livres réussissent à 
se démarquer de manière significative dans plusieurs classements.
"""