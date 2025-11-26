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

#CONSIGNE 3 affiche des livres aves les titres a 3 mots
maBiblio.books_3_mots()

# CONSIGNE 4 les livres avec le mot 'rose'
maBiblio.books_3_mots()


# état final
print(maBiblio)


