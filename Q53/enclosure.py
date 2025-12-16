from animal import Animal


class Enclosure:

    def __init__(self, name: str):
        self.name = name
        self.animal_l = []
        self.day_nb = 0
        self.date = 0
        self.fence_status = True # la clôture est en bon état

    def __str__(self):
        """
        à écrire
        """
        pass

    def add_animal(self, animal: Animal):
        """
        ajoute l'animal dans l'enclos
        :param animal: objet concret de classe Animal
        :return:
        """
        pass

    def del_animal(self, animal_name):
        """
        supprime cet animal, pour cause de décès ou de fuite
        :param animal_name: str, le nom de l'animal (pas l'objet)
        :return:
        """
        pass

    def increase_date(self):
        """
        à écrire
        """
        pass

    def give_food(self, animal_name, food):
        """
        à écrire
        """
        pass

    def do_this_six_hours_later(self):
        """
        à écrire
        vérifie l'état des animaux six heures après le nourrissage

        ATTENTION
        Eviter une boucle sur des objets si ceux-ci doivent être supprimés dans la boucle;
        à cause de la gestion des références.  A la place, travailler sur une copie de la liste [:],
        ou (mieux) faire une boucle sur un attribut des objets (ex: sur le nom de l'animal),
        afin d'éviter de créer une nouvelle référence à l'objet dans la boucle.
        """
        pass

    def break_fence(self):
        """
        à écrire
        """
        pass

