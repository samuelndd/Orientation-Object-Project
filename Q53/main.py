from enclosure import Enclosure
from animal import Elephant, Loup, Lion, Pingouin, Koala   # .....
from caretaker import Caretaker

import random
random.seed(0)


if __name__ == '__main__':
    group_name = "POO_"     # introduire votre nom de groupe
    enclos1 = Enclosure(f"Zoo du groupe {group_name}")

    # Ajout des animaux
    enclos1.add_animal(Elephant("Babar", enclos1))   # ANIMAL DE TAILLE GRANDE
    enclos1.add_animal(Loup("Akela", enclos1))       # taille moyenne (consigne 4)
    enclos1.add_animal( Lion("Louis", enclos1,) )
    enclos1.add_animal(Pingouin("Waddle", enclos1))
    enclos1.add_animal(Koala("Kiki", enclos1))       # autre animal


    # .........

    # Un soigneur est engagé, qui s'occupe de l'enclos
    soigneur1 = Caretaker("Jean", enclos1)

    # Établir le planning (avec erreurs)
    soigneur1.set_schedule(5)

    # Exécuter le planning
    soigneur1.exec_schedule()

    print("\n--- End of simulation\n\n")

