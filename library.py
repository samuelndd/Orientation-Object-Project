import json
import book


class Library:
    def __init__(self,__file_in):
        self.__file_in = __file_in
        self.__library_l = []  # Liste VIDE au départ
        self.__contenu_json()  # On charge ensuite les livres

    def __contenu_json(self):
        """Charge les livres depuis le fichier JSON"""
        with open(self.__file_in, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.__library_l = []  # on repart d'une liste vide

            # Pour chaque dictionnaire du JSON, on crée un objet Book
            for d in data:
                # création de l'objet Book à partir des clés du JSON
                b = book.Book(          # ICI : on appelle la classe Book
                    d["title"],  # titre
                    d["author"],  # auteur
                    d["publication_year"],  # année de publication
                    d["page_count"]  # nombre de pages
                )

                # on copie aussi la dispo depuis le JSON
                # on met à jour la dispo via le setter
                b.is_available = d["is_available"]

                # on ajoute l'objet Book dans la liste de la bibliothèque
                self.__library_l.append(b)

    def __str__(self):

        """
         Affiche les livres triés par nombre de pages décroissant
         """
        # Tri du plus grand au plus petit on utilisent get
        livres_tries = sorted(
            self.__library_l,key=lambda b: b.get_nombre_pages(),reverse=True)

        result = f"Bibliothèque a {len(self.__library_l)} livres\n"
        result += f"{'Titre':<50} {'Auteur':<30} {'Pages':<8} {'Année':<8} {'Disponible':<12}\n"
        result += "=" * 120 + "\n"

        # Afficher chaque livre via les GETTERS
        for bk in livres_tries:
            statut = "Oui" if bk.get_is_available() else "Non"
            result += (
                f"{bk.get_titre():<50} "
                f"{bk.get_auteur():<30} "
                f"{bk.get_nombre_pages():<8} "
                f"{bk.get_annee_publication():<8} "
                f"{statut:<12}\n"
            )

        return result

    #CONSIGNE 3 : livres dont le titre contient 3 mots
    def books_3_mots(self):
        """
        Affichage d'information spécifique :
        Affichez les informations des livres dont le titre contient exactement 3 mots, triés par ordre alphabétique du titre.
        Remarque : Format tabulaire; champs à afficher : title, author, page_count, publication_year, is_available
        """

        # Filtrer les livres dont le titre contient exactement 3 mots
        livres_3_mots = [
            b for b in self.__library_l
            if len(b.get_titre().split()) == 3
        ]

        # Tri alphabétique sur le titre
        livres_3_mots = sorted(
            livres_3_mots, key=lambda b: b.get_titre().lower()
        )

        print("Voici les livres avec 3 mots")

        print(f"{'Titre':<50} {'Auteur':<30} {'Pages':<8} {'Année':<8} {'Disponible':<12}")
        print("=" * 120)

        # Lignes du tableau
        """
            Pour cette boucles je demande a l'ai de me generer un code qui m'aides a faire 
            un tableaux et je me suis baser sur mon binome qui a fait un codes plus ou moins simulaire 
         """
        for bk in livres_3_mots:
            statut = "Oui" if bk.get_is_available() else "Non"
            print(
                f"{bk.get_titre():<50} "
                f"{bk.get_auteur():<30} "
                f"{bk.get_nombre_pages():<8} "
                f"{bk.get_annee_publication():<8} "
                f"{statut:<12}"
            )


     # CONSIGNE 4 : livres avec le titre rose
    def books_rose(self):
        """
         Recherche
        Trouvez et affichez les livres dont le titre contient le mot 'rose'
        (insensible à la casse), triés par ordre alphabétique du titre.
        Format tabulaire; champs : title, author, page_count, publication_year, is_available
         """
        mot_trouvez = "rose"

        # Filtrer les livres pour rose
        livres_rose = []
        for b in self.__library_l:
            """
            On travaille en minuscule cette partie je savais pas somment faire pour faire
            que des recherche en miniscule alors je demande a l'ia et il ma fourni 
            titre_min = b.get_titre().lower()
            et apres le code ne marchais pas alors il ma aussi proposer sa # On découpe le titre en mots
            mots_titre = titre_min.split()
            """
            # On travaille en minuscule
            titre_min = b.get_titre().lower()
            # On découpe le titre en mots
            mots_titre = titre_min.split()
            if mot_trouvez in mots_titre:
                livres_rose.append(b)

         # Tri alphabétique sur le titre
        livres_rose = sorted(livres_rose, key=lambda b: b.get_titre().lower())

        print(" Yo les boooks avec rose")


        print(f"{'Titre':<50} {'Auteur':<30} {'Pages':<8} {'Année':<8} {'Disponible':<12}")
        print("=" * 120)

            # la comme les boucles precedents sa creer le tableaux
        for bk in livres_rose:
            statut = "Oui" if bk.get_is_available() else "Non"
            print(
                f"{bk.get_titre():<50} "
                f"{bk.get_auteur():<30} "
                f"{bk.get_nombre_pages():<8} "
                f"{bk.get_annee_publication():<8} "
                f"{statut:<12}"
            )


    # CONSIGNE 5 : Ajoutez 20 pages à tous les livres écrits par Guy de Maupassant
    def ajout_20_pages_a_maupassant(self):
        """
        Modification d'attributs :
        Ajoute 20 pages à tous les livres écrits par Guy de Maupassant.
        """
        print(" vous n'êtes pas contents plus 20")

        for b in self.__library_l:
            if b.get_auteur() == "Guy de Maupassant":
                # On lit le nombre de pages actuel, on ajoute 20, puis on réécrit via le setter
                aout_pages = b.get_nombre_pages() + 20
                b.set_nombre_pages(aout_pages)



    # CONSIGNE 6 : Empruntez les livres écrits par Victor Hugo
    def emprunter_livres_victor_hugo(self):
        """
         Manipulation de méthodes
        Empruntez les livres écrits par Victor Hugo.
        """
        print(" Empruntez les livres écrits par Victor Hugo.")
        for b in self.__library_l:
            if b.get_auteur() == "Victor Hugo":
                # On appelle la méthode emprunter() du livre
                ok = b.emprunter()
                print(ok)



if __name__ == '__main__':

    Bibliotheque = Library("book_in.json")

    print(" CONSIGNES 1 Et 2")
    print(Bibliotheque)  # Utilise __str__

    print("CONSIGNE 3")
    Bibliotheque.books_3_mots() # consigne 3

    print("CONSIGNE 4 ")
    Bibliotheque.books_rose()  # Affichage consigne 4

    print("CONSIGNE 5 +20 PAGES POUR GUY DE MAUPASSANT ")
    Bibliotheque.ajout_20_pages_a_maupassant()
    print(Bibliotheque)

    print("CONSIGNE 6 EMPRUNT DES LIVRES DE VICTOR HUGO ")
    Bibliotheque.emprunter_livres_victor_hugo()



