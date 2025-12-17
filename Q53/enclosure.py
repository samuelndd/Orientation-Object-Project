from __future__ import  annotations

from  typing import  Optional

from animal import Animal


class Enclosure:

    def __init__(self, name: str):
        self.name = name
        self.animal_l: list[Animal] = []
        self.day_nb = 0
        self.date = 0
        self.fence_status = True # la clôture est en bon état

    def __str__(self) -> str:
        if not self.animal_l:
            return f"{self.name} : enclos vide"
        return "\n".join(str(a) for a in self.animal_l)



    def add_animal(self, animal: Animal):
        self.animal_l.append(animal)
        """
        ajoute l'animal dans l'enclos
        :param animal: objet concret de classe Animal
        :return:
        """



    """
           supprime cet animal, pour cause de décès ou de fuite
           :param animal_name: str, le nom de l'animal (pas l'objet)
           :return:
           """
    def del_animal(self, animal_name:str):
        animal = self._find_animal(animal_name)
        if animal is None:
            return
        self.animal_l.remove(animal)
        print(f"DELETE : {animal.family} {animal.name} is dead or escaped.")




    def increase_date(self):
        self.day_nb += 1
        self.date = self.day_nb



    def give_food(self, animal_name, food, quantity):
        animal = self._find_animal(animal_name)
        if animal is None:
            return
        animal.eat(food, quantity)



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
        for name in [a.name for a in self.animal_l]:
            animal = self._find_animal(name)
            if animal is None:
                continue
            animal.do_this_six_hours_later()

    def break_fence(self):
        self.fence_status = False

    def find_prey_for(self, predator: Animal, allowed_families: list[str]) -> Optional[Animal]:
        for a in self.animal_l:
            if a.name == predator.name:
                continue
            if a.family in allowed_families:
                return a
        return None

    def kill_animal(self, prey_name: str) -> None:
        prey = self._find_animal(prey_name)
        if prey is None:
            return
        print(f"ALERT: {prey.name} is dead or escaped (sat:{prey.satiety}).")
        self.del_animal(prey.name)

    def _find_animal(self, animal_name: str) -> Optional[Animal]:
        for a in self.animal_l:
            if a.name == animal_name:
                return a
        return None
