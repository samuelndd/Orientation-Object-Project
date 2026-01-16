# livecounter.py
class LiveCounter:
    """Compteur simple de générations (utile plus tard)."""

    def __init__(self) -> None:  #initialise l'objet (définit les attributs d'instance)
        self.__generation: int = 0  # Attribut PRIVÉ : stocke le numéro de génération (commence à 0)

    def __str__(self) -> str:  # Méthode magique : représentation texte (utile pour debug)
        return f"LiveCounter(generation={self.__generation})"  # Retourne une phrase indiquant la génération actuelle






    @property  # permet de lire les attribut
    def generation(self) -> int:
        return self.__generation






    def reset(self) -> None:  # remet le compteur à zéro
        self.__generation = 0  # Fixe la génération à 0

    def inc(self) -> None:  # incrémente le compteur
        self.__generation += 1  # Ajoute 1 à la génération







if __name__ == "__main__":
    c = LiveCounter()  # Crée un compteur
    assert c.generation == 0  # Vérifie la valeur initiale (scénario nominal)
    c.inc()  # Incrémente une fois
    assert c.generation == 1  # Vérifie que l'incrément fonctionne
    print("livecounter.py OK")
