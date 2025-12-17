import random
# from os import environ
from pprint import pprint
from enclosure import Enclosure

class Caretaker:
    aliments_disponibles = [
        "viande", "poisson", "crevette",
        "feuilles", "herbes", "fruits",
        "eucalyptus", "bambou", "graines",
        "baies", "miel"
    ]

    def __init__(self, name:str, enclosure:Enclosure ):
        self.name = name
        self.enclosure = enclosure
        self.schedule = {}
        self.nb_days = 0

    def set_schedule(self, nb_days : int = 5):
        """
        Le soigneur établit son planning de nourrissage
        mais comme il ne connait rien au métier,
        il choisit les aliments au hasard
        :param nb_days: nombre de jours à planifier
        :return: null
        A NE PAS MODIFIER
        """
        self.nb_days = nb_days
        for jour in range(1, self.nb_days + 1):
            self.schedule[jour] = {}
            for animal in self.enclosure.animal_l:
                feed = random.choice(self.aliments_disponibles)  
                # feed peut être incorrect par rapport au régime alimentaire prescrit
                qnt = random.randint(2, 5)
                self.schedule[jour][animal.name] = { feed : qnt }
        print("Planning de nourrissage :")
        pprint(self.schedule)

    def exec_schedule(self):
        for jour in range(1, self.nb_days + 1):
            self.enclosure.increase_date()
            print(f"\n--- Jour {jour} ---")
            # 1. incrementer la date
            # 2. boucler sur le planning de nourrissage, chaque animal est nourri
            # 3. réaction des animaux six heures plus tard
            # 4. état des lieux après une journée (cf output)
            print("--- Nourrissage---")
            for animal_name, food_dict in self.schedule[jour].items():
                food, quantity = next(iter(food_dict.items()))

                if not any(a.name == animal_name for a in self.enclosure.animal_l):
                    print(f"{self.name} : je ne trouve pas {animal_name} :")
                    continue

                self.enclosure.give_food(animal_name, food, quantity)
                print(f"{self.name} : j'ai nourri {animal_name} :")

            print("\n--- Six heures plus tard---")
            self.enclosure.do_this_six_hours_later()

            print(f"\n--- Bilan après {jour} jours---")
            for a in self.enclosure.animal_l:
                print(f"{a}")


