from enclosure import Enclosure
from animal import Lion, Girafe  # .....
from caretaker import Caretaker

if __name__ == '__main__':

    group_name = "POO_"     # introduire votre nom de groupe
    enclos1 = Enclosure(f"Zoo du groupe {group_name}")

    # Ajout des animaux
    enclos1.add_animal( Lion("Louis", enclos1) )
    enclos1.add_animal( Girafe("Aglaé", enclos1) )
    # .........

    # Un soigneur est engagé, qui s'occupe de l'enclos
    soigneur1 = Caretaker("Jean", enclos1)

    # Établir le planning (avec erreurs)
    soigneur1.set_schedule(5)

    # Exécuter le planning
    soigneur1.exec_schedule()

    print("\n--- End of simulation\n\n")

