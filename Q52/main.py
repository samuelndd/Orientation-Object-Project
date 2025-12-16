import library


#
# Votre application se lance à partir d'ici (et de nulle part ailleurs)
#

# code à développer suivant les consignes
# par ex. :
# maBiblio.display_books_beginning_by_letter("z")
# maBiblio.dubble_pages_of_books_published_before(1950)
# maBiblio.search_book_between( 1800, 1900 )
# .......

# Création de l'unique instance de Library
maBiblio = library.Library("book_in.json")

# Affiche de l'état initial (consignes 1 et 2)
print(maBiblio)

print("CONSIGNE 3 ---------------------------------------------------------------------------")
#CONSIGNE 3 des livres aves les titres a 3 mots
maBiblio.books_3_mots()

print("CONSIGNE 4 ---------------------------------------------------------------------------")
# CONSIGNE 4 les livres avec le mot rose
maBiblio.books_rose()

print("CONSIGNE 5 ---------------------------------------------------------------------------")
#CONSIGNE 5 ajouter 20 pages aux livres de Guy de Maupassant
maBiblio.ajout_20_pages_a_maupassant()
print(maBiblio)

print("CONSIGNE 6 ---------------------------------------------------------------------------")
# CONSIGNE 6 emprunter les livres de Victor Hugo
maBiblio.emprunter_livres_victor_hugo()

print("CONSIGNE 7 ---------------------------------------------------------------------------")
# CONSIGNE 7 Calculez et affichez le nombre total des pages des 5 livres les plus longs
maBiblio.nbr_total_pages_5_books()

print("CONSIGNE 8 ---------------------------------------------------------------------------")
#CONSIGNE 8 modifications apportées aux livres
print(maBiblio)

print("CONSIGNE 9 ---------------------------------------------------------------------------")
# Sauvegardez la bibliothèque, avec les modifications, dans un fichier book_out.py.
maBiblio.sauvegarder_bibliotheque("book_out.json")



