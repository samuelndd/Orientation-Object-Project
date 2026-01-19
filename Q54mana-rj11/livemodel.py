import random
from abc import ABC, abstractmethod

# ============================================================================
# PATTERN STRATEGY : Stratégies de configuration
# ============================================================================


class ConfigStrategy(ABC):
    """Classe abstraite pour les différentes stratégies de config"""

    @abstractmethod
    def apply(self, model):
        """Applique la stratégie sur le modèle"""
        pass

class RandomStrategy(ConfigStrategy):
    """Config aléatoire avec un pourcentage de cellules vivantes"""

    def __init__(self, percentage=25):
        self.percentage = percentage

    def apply(self, model):
        """Place aléatoirement des cellules vivantes"""
        model.reset_all_cells()
        total_cells = model.matrix_width * model.matrix_height
        alive_count = int(total_cells * self.percentage / 100)
        cells_list = list(model.get_all_cells())
        alive_cells = random.sample(cells_list, alive_count)
        for cell in alive_cells:
            cell.set_alive(True)

class CanonStrategy(ConfigStrategy):
    """Config avec un canon à planeurs"""

    def apply(self, model):
        """Place le caon à planeurs classique"""
        model.reset_all_cells()
        # Positions du canon à planeurs
        canon_positions = [
            (0, 5), (0, 6), (1, 5), (1, 6),
            (10, 5), (10, 6), (10, 7),
            (11, 4), (11, 8),
            (12, 3), (12, 9),
            (13, 3), (13, 9),
            (14, 6),
            (15, 4), (15, 8),
            (16, 5), (16, 6), (16, 7),
            (17, 6),
            (20, 3), (20, 4), (20, 5),
            (21, 3), (21, 4), (21, 5),
            (22, 2), (22, 6),
            (24, 1), (24, 2), (24, 6), (24, 7),
            (34, 3), (34, 4),
            (35, 3), (35, 4)
        ]
        for x, y in canon_positions:
            cell = model.get_cell(x, y)
            if cell:
                cell.set_alive(True)

class EmptyStrategy(ConfigStrategy):
    """Config vide (toutes les cellules sot mortes)"""

    def apply(self, model):
        """Vide toute la grille"""
        model.reset_all_cells()

# ============================================================================
# PATTERN OBSERVER : La cellule observable
# ============================================================================


class LiveCell:
    """
    une cellule du jeu de la vie
    vivante/morte.. nb de voisins
    """

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y
        self._state = False
        self._nb_neighbours = 0
        self._observers = []    # Liste des observers (pattern Observer)

    # Properties (accesseurs en lecture)
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def state(self):
        return self._state

    @property
    def nb_neighbours(self):
        return self._nb_neighbours      # retourne l'attribut privé

    def is_alive(self) -> bool:
        """Retourne True si la cellule est vivante"""
        return self._state

    def set_alive(self, alive: bool):
        """Change l'état de la cellule et notifie les observers"""
        old_state = self._state
        self._state = alive
        # Notifier les observers si l'état a changé
        if old_state != alive:
            self._notify_observers()

    def set_nb_neighbours(self, count: int):
        """Définit le nombre de voisins vivants"""
        self._nb_neighbours = count

    def toggle(self):
        """Inverse l'état de la cellule (vivant <-> morte)"""
        self.set_alive(not self._state)

    # Pattern Observer
    def attach_observer(self, observer):
        """Attache un observer à cette cellule"""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach_observer(self, observer):
        """Détache un observer de cette cellule"""
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify_observers(self):
        """Notifie tous les observers qu'il y a eu un changement"""
        for observer in self._observers:
            observer.update(self)

    def __str__(self):
        state_str = "vivante" if self._state else "morte"
        return f"Cell{self._x}, {self._y}) - {state_str}"


# ============================================================================
# PATTERN SINGLETON : Modèle unique
# ============================================================================


class LiveModel:
    """
    Modèle principal du jeu de la vie (SINGLETON)
    gère la grille de cellules et les règles du jeu
    """

    # Attribut de classe pour stocker l'unique instance
    _instance = None

    @classmethod
    def get_instance(cls, canvas_width=500, canvas_height=500, cell_size=10):
        """Récupère l'instance unique du modèle (pattern Singleton)"""
        if cls._instance is None:
            cls._instance = cls(canvas_width, canvas_height, cell_size)
        return cls._instance

    def __init__(self, canvas_width: int, canvas_height: int, cell_size: int):
        """
        Constructeur (devrait être appelé qu'une seule fois via get_instance)
        :param canvas_width:
        :param canvas_height:
        :param cell_size:
        """
        # protection Singleton
        if LiveModel._instance is not None:
            raise Exception("Cette classe est un Singleton ! Utilisez get_instance()")

        self._canvas_width = canvas_width
        self._canvas_height = canvas_height
        self._cell_size = cell_size

        self._matrix_width = canvas_width // cell_size
        self._matrix_height = canvas_height // cell_size

        self._cells_matrix = []
        self._generation = 0
        self._running = False

        # Stratégie actuelle (pattern Strategy)
        self._current_strategy = None

        # Référence au compteur (observer)
        self._counter = None

        self._init_matrix()

    @property
    def canvas_width(self):
        return self._canvas_width

    @property
    def canvas_height(self):
        return self._canvas_height

    @property
    def cell_size(self):
        return self._cell_size

    @property
    def matrix_width(self):
        return self._matrix_width

    @property
    def matrix_height(self):
        return self._matrix_height


    @property
    def generation(self):
        return self._generation

    @property
    def running(self):
        return self._running

    # Méthodes publiques
    def set_counter(self, counter):
        """Définit le compteur (observer) et l'attache à toutes les cellules"""
        self._counter = counter
        for cell in self.get_all_cells():
            cell.attach_observer(counter)

    def set_strategy(self, strategy: ConfigStrategy):
        """Définit la stratégie de configuration actuelle"""
        self._current_strategy = strategy

    def apply_strategy(self):
        """Apllique la stratégie de configuration actuelle"""
        if self._current_strategy:
            self._current_strategy.apply(self)
            self._generation = 0
            # Recompter les cellules après config
            if self._counter:
                self._counter.count_all(self)

    def get_cell(self, x: int, y: int) -> LiveCell:
        """Récupère une cellule à une position donnée"""
        if 0 <= x < self._matrix_width and 0 <= y < self._matrix_height:
            return self._cells_matrix[y][x]
        return None

    def get_all_cells(self):
        """Générateur qui yield toutes les cellules"""
        for row in self._cells_matrix:
            for cell in row:
                yield cell

    def toggle_cell(self, x: int, y: int):
        """Inverse l'état d'une cellule (pour le clic utilisateur)"""
        cell = self.get_cell(x, y)
        if cell:
            cell.toggle()
            # Recompter après modification manuelle
            if self._counter:
                self._counter.count_all(self)

    def reset_all_cells(self):
        """Remet toutes les cellules à l'état mort"""
        for cell in self.get_all_cells():
            cell.set_alive(False)
            cell.set_nb_neighbours(0)

    def start(self):
        """Démarre la simulation"""
        self._running = True

    def pause(self):
        """Met en pause la simulation"""
        self._running = False

    def reset(self):
        """Reset complet : génération à 0, tout éteint"""
        self._running = False
        self._generation = 0
        self.reset_all_cells()
        if self._counter:
            self._counter.count_all(self)

    def count_alive_cells(self) -> int:
        """Compte le nombre de cellules vivantes"""
        count = 0
        for cell in self.get_all_cells():
            if cell.is_alive():
                count += 1
        return count

    def pixel_to_grid(self, pixel_x: int, pixel_y: int) -> tuple:
        """Convertit des coorndonnées pixel en coordonnées grille"""
        grid_x = pixel_x // self._cell_size
        grid_y = pixel_y // self._cell_size
        return (grid_x, grid_y)

    def next_generation(self):
        """
        Clacule la prochaine génération selon les règles du jeu de la vie

        Règles de Conway :
        - Naissance : cellule morte avec exactement 3 voisins vivants
        - Survie : cellule vivante avec 2 ou 3 voisins vivants
        - Mort : sinon
        """

        # 1. Compter les voisins de chaque cellule
        self._count_all_neighbours()

        # 2. Calculer le nouvel état de chauqe cellule
        new_states = []
        for cell in self.get_all_cells():
            neighbours = cell.nb_neighbours

            if cell.is_alive():
                # Cellule vivante : survit avec 2 ou 3 voisins
                new_state = neighbours in [2, 3]
            else:
                # Cellule morte : nait avec exactement 3 voisins
                new_state = neighbours == 3

            new_states.append((cell, new_state))

        # 3. Appliquer les nouveauc états
        for cell, new_state in new_states:
            cell.set_alive(new_state)

        self._generation += 1

        # 4. Recompter les cellules vivantes
        if self._counter:
            self._counter.count_all(self)

    def _init_matrix(self):
        """Initialise la matrice de cellules"""
        for y in range(self._matrix_height):
            row = []
            for x in range(self._matrix_width):
                cell = LiveCell(x, y)
                # Si un compteur existe déja, l'attacher
                if self._counter:
                    cell.attach_observer(self._counter)
                row.append(cell)
            self._cells_matrix.append(row)

    def _count_all_neighbours(self):
        """Compte les voisins vivants pour chaque cellule"""
        for cell in self.get_all_cells():
            count = self._count_neighbours(cell.x, cell.y)
            cell.set_nb_neighbours(count)

    def _count_neighbours(self, x: int, y: int) -> int:
        """Compte les voisins vivants autour d'une cellule"""
        count = 0
        # Parcourir les 8 voisins
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue    # On ne compte pas la cellule ell-même

                # Coordonnées du voisin (avec wrap-around pour les bords)
                nx = (x + dx) % self._matrix_width
                ny = (y + dy) % self._matrix_height

                if self._cells_matrix[ny][nx].is_alive():
                    count += 1
        return count

    def __str__(self):
        return f"LiveModel({self._matrix_width}x{self._matrix_height}, gen={self._generation})"





