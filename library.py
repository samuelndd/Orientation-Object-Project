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
                b = book.Book(
                    d["title"],  # titre
                    d["author"],  # auteur
                    d["publication_year"],  # année de publication
                    d["page_count"]  # nombre de pages
                )

                # on copie aussi la dispo depuis le JSON
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

        result = f"=== Bibliothèque ({len(self.__library_l)} livres) ===\n"
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




if __name__ == '__main__':
    print("Test de Library")
    Bibliothèque = Library("book_in.json")
    print(Bibliothèque)  # Utilise __str__