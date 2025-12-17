


class Animal:
    menu = []
    menu_alt = []
    family = ""
    satiety_drop = 1



    def __init__(self, name, enclosure):
        self._name = name
        self._satiety = 5   # 0 = affamé, 10 = repu
        self._enclosure = enclosure
        self._is_escaped = False      # l'animal est dans l'enclos






        # méthodes magiques
    def __str__(self):
        return (f"{self._name} : {self.status} (satiété:{self._satiety})")

        # propriétés publiques
    @property
    def name(self) -> str:
        return self._name

    @property
    def satiety(self) -> int:
        return self._satiety

    @property
    def is_escaped(self) -> bool:
        return self._is_escaped

    @property
    def is_dead(self) -> bool:
        return self._satiety < 0

    @property
    def status(self):
        """
        à ne pas modifier (en principe)
        """
        out = "indéfini"
        if self.is_escaped:
            out = "échappé"
        else:
            match self.satiety:
                case v if v >= 7:
                    out = "repus"
                case v if 7 > v >= 4:
                    out = "faim"
                case v if 4 > v >= 0:
                    out = "très faim"
                case v if v < 0:
                    out = "mort"
        return out

    def eat(self, food: str, quantity: int) -> None:
        """Traite la nourriture apportée par le soigneur."""
        if food in self.menu:
            self._satiety += quantity
            print(f"{self._name} mange {quantity} de {food}.")
        else:
            print(f"{self._name} refuse de manger {food}.")
        """
        à écrire
        l'animal est nourri ... si l'aliment proposé est conforme à ses attentes
        """



    def do_this_six_hours_later(self):
        """
        à écrire
        que fait l'animal six heures après qu'il a mangé ?
        """
    #méthodes protégées
    def _apply_satiety_drop(self):
        self._satiety -= self.satiety_drop

    def _si_cloture_defoncee(self, msg_when_escape):
        if not self._enclosure.fence_status:
            print(f"{msg_when_escape}")
            self._is_escaped = True
            print(f" ALERT:{self._name} il va s'échappe.")
            self._enclosure.del_animal(self._name)

    def _cloture_defoncee(self, msg):
        print(f"{msg}")
        self._enclosure.break_fence()
        self._is_escaped = True
        print(f"ALERT:{self._name}  il va s'échappe.")
        self._enclosure.del_animal(self._name)

    def _manger_certains_animaux(self):
        """Pour les prédateurs: tente de tuer un animal compatible (menualt)."""
        prey = self._enclosure.find_prey_for(self, self.menu_alt)
        if prey is None:
            print(f"Aucun animal de l'enclos ne peut satisfaire {self._name}.")
            return

        print(f" ALERT:{prey.name} is going to be killed by {self._name}.")
        self._enclosure.kill_animal(prey.name)




class Elephant(Animal):
    family = "éléphant"
    menu = ["herbes", "fruits"]
    menu_alt = []
    satiety_drop = 3

    def do_this_six_hours_later(self):
        self._apply_satiety_drop()

        match self.status:
            case "repus":
                print(f"{self.name} barrit de contentement et arrose son dos.")
            case "faim":
                print(f"{self.name} cherche de la nourriture autour de lui.")
            case "très faim":
                self._cloture_defoncee(
                    f"{self.name} casse la clôture de l'enclos et s'enfuit."
                )
            case "mort":
                print(f"ALERT: {self.name} is dead or escaped (sat:{self.satiety}).")
                self._enclosure.del_animal(self.name)



class Ours(Animal):
    family = "ours"
    menu = ["poisson", "baies", "miel"]
    menu_alt = []
    satiety_drop = 2

    def do_this_six_hours_later(self) -> None:
        self._apply_satiety_drop()

        match self.status:
            case "repus":
                print(f"{self.name} grogne de contentement.")
            case "faim":
                print(f"{self.name} cherche de la nourriture autour de lui.")
            case "très faim":
                self._cloture_defoncee(
                    f"{self.name} casse la clôture de l'enclos et s'enfuit."
                )
            case "mort":
                print(f"ALERT: {self.name} is dead or escaped (sat:{self.satiety}).")
                self._enclosure.del_animal(self.name)



class Gorille(Animal):
    family = "gorille"
    menu = ["feuilles", "herbes", "fruits"]
    menu_alt = []
    satiety_drop = 2

    def do_this_six_hours_later(self) -> None:
        self._apply_satiety_drop()

        match self.status:
            case "repus":
                print(f"{self.name} joue avec les jeunes gorilles.")
            case "faim":
                print(f"{self.name} se déplace en quete de plantes.")
            case "très faim":
                self._cloture_defoncee(
                    f"{self.name} casse la clôture de l'enclos et s'enfuit."
                )
            case "mort":
                print(f"ALERT: {self.name} is dead or escaped (sat:{self.satiety}).")
                self._enclosure.del_animal(self.name)



class Lion(Animal):
    family = "lion"
    menu = ["viande"]
    menu_alt = ["pingouin", "girafe"]
    satiety_drop = 1

    def do_this_six_hours_later(self):
        self._apply_satiety_drop()
        """
        à écrire
        """
        match self.status:
            case "repus":
                print(f"{self.name} fait la sieste.")
            case "faim":
                print(f"{self.name} rugit.")
            case "très faim":
                print(f"{self.name} veut manger un autre animal dans l'enclos.")
                self._manger_certains_animaux()
            case "mort":
                print(f"ALERT: {self.name} is dead or escaped (sat:{self.satiety}).")
                self._enclosure.del_animal(self.name)



class Serpent(Animal):
    family = "serpent"
    menu = ["viande"]
    menu_alt = ["pingouin", "koala", "loup"]
    satiety_drop = 1

    def do_this_six_hours_later(self):
        self._apply_satiety_drop()
        """
        à écrire
        """
        match self.status:
            case "repus":
                print(f"{self.name} s'enroule en boulet et dort pendant deux jours.")
            case "faim":
                print(f"{self.name} reste immobile.")
            case "très faim":
                print(f"{self.name} chasse un autre animal dans l'enclos et le mange.")
                self._manger_certains_animaux()
            case "mort":
                print(f"ALERT: {self.name} is dead or escaped (sat:{self.satiety}).")
                self._enclosure.del_animal(self.name)



class Loup(Animal):
    family = "loup"
    menu = ["viande"]
    menu_alt = ["pingouin", "koala", "serpent"]
    satiety_drop = 2

    def do_this_six_hours_later(self):
        self._apply_satiety_drop()

        match self.status:
            case "repus":
                print(f"    {self.name} fait la sieste.")
            case "faim":
                print(f"    {self.name} hurle.")
            case "très faim":
                print(f"    {self.name} chasse un autre animal dans l'enclos et le mange.")
                self._manger_certains_animaux()
            case "mort":
                print(f"    ALERT: {self.name} is dead or escaped (sat:{self.satiety}).")
                self._enclosure.del_animal(self.name)
    """
    à écrire
    """



class Pingouin(Animal):
    family = "pingouin"
    menu = ["poisson", "crevette"]
    menu_alt = []
    satiety_drop = 1

    def do_this_six_hours_later(self) :
        self._apply_satiety_drop()

        match self.status:
            case "repus":
                print(
                    f"{self.name} elle fait la sieste."
                )
            case "faim":
                print(
                    f"{self.name} elle broute un peu herbe au sol."
                )
            case "très faim":
                self._si_cloture_defoncee(f"{self.name} la cloture de l'enclos est cassée, elle s'enfuit.")
            case "mort":
                print(f"ALERT:{self.name} is dead or escaped (sat:{self.satiety}).")
                self._enclosure.del_animal(self.name)
    """
    à écrire
    """



class Girafe(Animal):
    family = "girafe"
    menu = ["feuilles"]
    menu_alt = []
    satiety_drop = 2

    def do_this_six_hours_later(self) :
        self._apply_satiety_drop()

        match self.status:
            case "repus":
                print(
                    f"{self.name} elle fait la sieste."
                )
            case "faim":
                print(
                    f"{self.name} broute un peu herbe au sol."
                )
            case "très faim":
                self._si_cloture_defoncee(f"{self.name} s'enfuit.")
            case "mort":
                print(f"ALERT:{self.name} is dead or escaped (sat:{self.satiety}).")
                self._enclosure.del_animal(self.name)

    """
    à écrire
    """


class Koala(Animal):
    family = "koala"
    menu = ["eucalyptus"]
    menu_alt = []
    satiety_drop = 3

    def do_this_six_hours_later(self) :
        self._apply_satiety_drop()

        match self.status:
            case "repus":
                print(
                    f"{self.name} s'endort immédiatement dans son eucalyptus, repu et heureux."
                )
            case "faim":
                print(
                    f"{self.name} mâchouille lentement une feuille d'eucalyptus en regardant autour de lui."
                )
            case "très faim":
                self._si_cloture_defoncee(f"{self.name} s'enfuit.")
            case "mort":
                print(f"ALERT:{self.name} is dead or escaped (sat:{self.satiety}).")
                self._enclosure.del_animal(self.name)
    """
    à écrire
    """



# ............
# ............
# ............
# ............

