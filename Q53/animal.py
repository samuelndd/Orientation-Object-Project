


class Animal:
    menu = []
    menualt = []
    family = ""

    def __init__(self, name: str, enclosure):
        self.name = name
        self.satiety = 5  # 0 = affamé, 10 = repu
        self.enclosure = enclosure
        self.is_escaped = False       # l'animal est dans l'enclos

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

    def eat(self, food) -> None:
        """
        à écrire
        l'animal est nourri ... si l'aliment proposé est conforme à ses attentes
        """
        pass

    def do_this_six_hours_later(self):
        """
        à écrire
        que fait l'animal six heures après qu'il a mangé ?
        """
        pass


class Lion:
    family = "lion"
    menu = ["viande"]
    menu_alt = ["pingouin", "girafe", "rongeur"]

    def do_this_six_hours_later(self):
        """
        à écrire
        """
        pass


class Girafe:
    family = "girafe"
    menu = ["feuilles", "herbes", "baies"]
    menu_alt = []

    def do_this_six_hours_later(self):
        """
        à écrire
        """
        pass

class Loup:
    """
    à écrire
    """
    pass

class Koala:
    """
    à écrire
    """
    pass


# ............
# ............
# ............
# ............

