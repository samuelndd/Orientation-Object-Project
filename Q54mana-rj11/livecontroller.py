from livemodel import LiveModel, RandomStrategy, CanonStrategy, EmptyStrategy
from livecounter import LiveCounter

class LiveController:
    """
    Controler principal (MVC)
    gère la logique de l'application et fait le lien entre modèle et vue
    """

    def __init__(self, canvas_width: int = 500, canvas_height: int = 500, cell_size: int = 10):
        # Créer le modèle (SINGLETON)
        self._model = LiveModel.get_instance(canvas_width, canvas_height, cell_size)
        self._view = None

        # Créer le compteur (OBSERVER)
        self._counter = LiveCounter()
        self._model.set_counter(self._counter)

        # Créer les stratégies (STRATEGY)
        self.gui_random_strategy = RandomStrategy(25)
        self._canon_strategy = CanonStrategy()
        self._empty_strategy = EmptyStrategy()

        # Configuration initiale (vide)
        self._model.set_strategy(self._empty_strategy)
        self._model.apply_strategy()

        # Paramètres
        self._matrix_width = self._model.matrix_width
        self._matrix_height = self._model.matrix_height
        self._refresh_delay = 100   # millisecondes entre chaque génération
        self._flag = False          # True = simulation en cours

    def set_view(self, view):
        """Lie la vue au contrôleur"""
        self._view = view

    @property
    def model(self):
        return self._model

    @property
    def refresh_delay(self):
        return self._refresh_delay

# ========================================================================
# Méthodes GUI - Appelées par les boutons de la vue
# ========================================================================

    def gui_go(self):
        """démarrer la simulation"""
        if not self._flag:
            self._model.start()
            self._flag = True
            self.play()

    def gui_stop(self):
        """Arreter la simulation"""
        self._model.pause()
        self._flag = False

    def gui_reset(self):
        """ Reset complet : tout remettre à zéro"""
        self._flag = False
        self._model.reset()
        if self._view:
            self._view.update_display()

    def gui_step(self):
        """ Avancer d'une génération (mode pas-à-pas"""
        self._flag = False  # Arrêter la simulation auto
        self._model.pause()
        self._next_generation()
        if self._view:
            self._view.update_display()

    def gui_canon(self):
        """ Appliquer la config canon (STRATEGY)"""
        self._flag = False
        self._model.pause()
        self._model.set_strategy(self._canon_strategy)
        self._model.apply_strategy()
        if self._view:
            self._view.update_display()

    def gui_random(self):
        """Appliquer la config aléatoire (STRATEGY)"""
        self._flag = False
        self._model.pause()
        self._model.set_strategy(self.gui_random_strategy)
        self._model.apply_strategy()
        if self._view:
            self._view.update_display()

    def gui_empty(self):
        """Vider la grille (STRATEGY)"""
        self._flag = False
        self._model.pause()
        self._model.set_strategy(self._empty_strategy)
        self._model.apply_strategy()
        if self._view:
            self._view.update_display()

    def gui_change_speed(self, speed_str: str):
        """Changer la vitesse de simulation"""
        try:
            speed = int(speed_str)
            if speed > 0:
                self._refresh_delay = speed
                print(f"Vitesse changée : {speed} ms")
            else:
                print(" La vitesse doit être positive")
        except ValueError:
            print("Vitesse invalide (entrer un nombre")

    def gui_cell_click(self, pixel_x: int, pixel_y: int, button: int):
        """
        gestion du clic sur une cellule
        :param pixel_x: Position X en pixels
        :param pixel_y: Position Y en pixels
        :param button: 1=clic gauche, 3=clic droit
        """
        # Convertir pixels -> coordonnées grille
        grid_x, grid_y = self._model.pixel_to_grid(pixel_x, pixel_y)

        # Récupérer la cellule
        cell = self._model.get_cell(grid_x, grid_y)

        if cell:
            if button == 1:
                # clic gauche : toggle (inverse l'état)
                cell.set_alive(True)    # Active uniquement
                # cell.toggle()       # active et désactive la cellule avec un clic droit
            elif button == 3:
                # clic droit : tuer
                cell.set_alive(False)

            # Mettre à jour l'affichage
            if self._view:
                self._view.update_display()

# ========================================================================
# Méthodes de simulation
# ========================================================================

    def play(self):
        """
        Boucle principale de simulation
        Appelée automatiquement toutes les X millisecondes
        """
        print(f" play() appelé - flag={self._flag}")
        if self._flag:  # Si la simulation est en cours
            # Calculer la génération suivante
            self._next_generation()

            # Mettre a jour l'affichage
            if self._view:
                self._view.update_display()
                # Programmer la prochaine itération
                # self._view.get_root.ai().update()   ######@@@@@@@@@  Force tkinter à redessiner !
                self._view.schedule_next_iteration(self._refresh_delay, self.play)

    def _next_generation(self):
        """
        Calcule la prochaine génération
        1. Compte les voisins
        2. Applique les règles de Conway
        """
        # self._count_neighbours()
        # self._apply_conway_rules()
        self._model.next_generation()

    def _count_neighbours(self):
        """
        Compte les voisins vivants pour chaque cellule
        CORRECTION DU BUG : count est maintenant à la bonne place
        """
        for cell in self._model.get_all_cells():
            x = cell.x
            y = cell.y
            count = 0

            # Parcourir les 8 voisins
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue    # On ne compte pas la cellule elle-même

                    nx = x + dx
                    ny = y + dy

                    # Récupère le voisin
                    neighbour = self._model.get_cell(nx, ny)
                    if neighbour and neighbour.is_alive():
                        count += 1

            cell.set_nb_neighbours(count)

    def _apply_conway_rules(self):
        """
        Applique les règles de Conway

        Règles :
        - Naissance : cellule morte avec exactement 3 voisins vivants
        - Survie : cellule vivante avec 2 ou 3 voisins vivants
        - Mort : sinon
        """
        changes = []

        # Calculer les changements pour toutes les cellules
        for cell in self._model.get_cells():
            nb = cell.nb_neighbours
            alive = cell.is_alive()

            # Règle 1 : Naissance (3 voisins)
            if nb == 3:
                if not alive:
                    changes.append((cell, True))

            # Règle 2 : Survie (2 voisins)
            elif nb == 2:
                pass    # La cellule garde son état

            # Règle 3 : Mort (autres cas)
            else:
                if alive:
                    changes.append((cell, False))

            # Appliquer tous les changements en même temps
            for cell, new_state in changes:
                cell.set_alive(new_state)

            self._model._generation += 1

            # Incrémenter le compteut de génération
            # (Note : normalement fait dans le modèle via next_generation())
            # Mais ici on le fait manuellement car on gène la logique dans le contôleur

            if self._view:
                self._view.update_display()
                self._view.schedule_next_iteration(self._refresh_delay, self.play)

    def _count_neighbours(self):
        for cell in self._model.get_all_cells():
            x = cell.x
            y = cell.y
            count = 0

            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue

                    nx = x + dx
                    ny = y + dy

                    neighbours = self._model.get_cell(nx, ny)
                    if neighbours and neighbours.is_alive():
                        count += 1

            cell.set_nb_neighbours(count)

    def _apply_conway_rules(self):
        changes = []

        for cell in self._model.get_all_cells():
            nb = cell.nb_neighbours
            alive = cell.is_alive()

            if nb == 3:
                if not alive:
                    changes.append((cell, True))

            elif nb == 2:
                pass

            else:
                if alive:
                    changes.append((cell, False))

        for cell, new_state in changes:
            cell.set_alive(new_state)

