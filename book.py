class Book:
    """
    ébauche de classe Book, à développer suivant les consignes
    """
    def __init__(self, titre, auteur, annee_publication, nombre_pages):
        self.__titre = titre    # Attribut privé
        self.__auteur = auteur  # Attribut privé
        self.__annee_publication = annee_publication    # Attribut privé
        self.__nombre_pages = nombre_pages  # Attribut privé
        self.__is_available = True    # CORRECT 8 (Livre disponible par défaut)

    # Getters pour avoir le contrôle d'accès aux données
    def get_titre(self):
        return self.__titre

    def get_auteur(self):
        return self.__auteur

    def get_annee_publication(self):
        return self.__annee_publication

    def get_nombre_pages(self):
        return self.__nombre_pages

    # NEW : setter pour le nombre de pages (utilisé par la consigne 5)
    def set_nombre_pages(self, nombre_pages):
        self.__nombre_pages = nombre_pages

    def get_is_available(self):
        return self.__is_available

    # Pour se Setter j'avais des eureur que je comprene pas alos je aussi demande a l'ia de l'aides
    # et sa aides a pour la dispo (important pour lire le JSON)
    def set_is_available(self, disponible: bool):
        self.__is_available = disponible

    def __str__(self):
        statut = "Disponible" if self.__is_available else "Emprunté"
        return (f"Titre: {self.__titre}, Auteur: {self.__auteur}, "
                f"Année: {self.__annee_publication}, Pages: {self.__nombre_pages}, "
                f"Statut: {statut}")

    def emprunter(self):
        if self.__is_available:
            self.__is_available = False
            return f"Le livre '{self.__titre}' a été emprunté."
        else:
            return f"Le livre '{self.__titre}' est déjà emprunté."

    def retourner(self):
        if not self.__is_available:
            self.__is_available = True    # CORRECT (Livre redevient disponible)
            return f"Le livre '{self.__titre}' a été retourné."
        else:
            return f"Le livre '{self.__titre}' n'était pas emprunté."


if __name__ == '__main__':
    #
    # Votre code éventuel de test ou d'appel à la classe Book s'écrit ici (et nulle part ailleurs)
    #
    livre1 = Book("Le Petit Prince", "Antoine de Saint-Exupéry", 1943, 96)
    print(livre1)
    print(livre1.emprunter())
    print(livre1)
    print(livre1.retourner())
    print(livre1)

