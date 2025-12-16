import random
# from os import environ
from pprint import pprint
from enclosure import Enclosure


class Caretaker:
    aliments_disponibles = ["viande", "poisson", "feuilles", "herbes", "fruits", "eucalyptus", "bambou", "graines", "baies", "miel" ]

    def __init__(self, name:str, enclosure:Enclosure ):
        """
        à écrire
        """
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
        pprint(self.schedule)

    def exec_schedule(self):
        """
        à écrire
        """
        for jour in range(1, self.nb_days + 1):
            # 1. incrementer la date
            # 2. boucler sur le planning de nourrissage, chaque animal est nourri
            # 3. réaction des animaux six heures plus tard
            # 4. état des lieux après une journée (cf output)
            pass


