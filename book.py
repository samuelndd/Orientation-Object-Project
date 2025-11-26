class Book:
    """
    ébauche de classe Book, à développer suivant les consignes
    """

    def __init__(self, titre, auteur, annee_publication, nombre_pages):
        self.__titre = titre
        self.__auteur = auteur
        self.__annee_publication = annee_publication
        self.__nombre_pages = nombre_pages
        self.__is_available = False



    def get_titre(self):
        return self.__titre

    def get_auteur(self):
        return self.__auteur

    def get_annee_publication(self):
        return self.__annee_publication

    def get_nombre_pages(self):
        return self.__nombre_pages

    def get_is_available(self):
        return self.__is_available


    # --------- AFFICHAGE ---------
    def __str__(self):
        return (f"Titre: {self.__titre}, Auteur: {self.__auteur}, "
                f"Année: {self.__annee_publication}, Pages: {self.__nombre_pages}, "
                f"Emprunté: {'Oui' if not self.__is_available else 'Non'}")



    #emprunter / retourner
    def emprunter(self):
        if self.__is_available:
            self.__is_available = False
            return f"Le livre '{self.__titre}' a été emprunté."
        else:
            return f"Le livre '{self.__titre}' est déjà emprunté."

    def retourner(self):
        if not self.__is_available:
            self.__is_available = True
            return f"Le livre '{self.__titre}' a été retourné."
        else:
            return f"Le livre '{self.__titre}' n'était pas emprunté."


if __name__ == '__main__':
    #
    # Votre code éventuel de test ou d'appel à la classe Book s'écrit ici (et nulle part ailleurs)
    #
    pass


