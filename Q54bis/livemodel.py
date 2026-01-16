"""
livemodel.py


Rôle :
- Stocker les données du jeu (grille de cellules)
- Contenir TOUTE la logique de calcul (voisins, règles, step)
- Aucune dépendance Tkinter (sinon couplage fort)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterator


# ============================================================
# 1) CELLULES : classe abstraite + héritage + polymorphisme
# ============================================================

class Cell(ABC):
    """
    Cell = classe abstraite (ABC) : on ne crée pas "Cell()" directement.

    Pourquoi une classe abstraite ?
    - Elle force les classes enfants à implémenter les mêmes méthodes.
    - Elle simplifie le code : Grid.step() n'a PAS besoin de savoir
      si la cellule est vivante ou morte, il appelle juste next_alive().
    """

    @property
    @abstractmethod
    def alive(self) -> bool:
        """
        Propriété abstraite : chaque type de cellule doit dire si elle est vivante.
        """
        raise NotImplementedError

    @abstractmethod
    def next_alive(self, alive_neighbors: int) -> bool:
        """
        Calcule l'état "vivant ou mort" à la prochaine génération.
        Ici on implémente les règles de Conway.

        Pourquoi mettre ça ici ?
        -> Polymorphisme : AliveCell et DeadCell n'ont pas la même règle.
        """
        raise NotImplementedError


@dataclass(frozen=True)
class AliveCell(Cell):
    """
    (oral hérite de Cell)
    Cellule vivante.
    frozen=True => objet immuable : une fois créé, il ne change pas.
    Avantage : moins de bugs, logique plus propre.
    """

    @property
    def alive(self) -> bool:
        return True

    def next_alive(self, alive_neighbors: int) -> bool:
        """
        Règle Conway pour cellule vivante :
        - survit si 2 ou 3 voisins vivants
        - sinon meurt
        """
        return alive_neighbors in (2, 3)


@dataclass(frozen=True)
class DeadCell(Cell):
    """
    Cellule morte.
    """

    @property
    def alive(self) -> bool:
        return False

    def next_alive(self, alive_neighbors: int) -> bool:
        """
        Règle Conway pour cellule morte :
        - naît si exactement 3 voisins vivants
        - sinon reste morte
        """
        return alive_neighbors == 3


# création centralisée des cellules
class CellFactory:
    """
    Design Pattern Factory : on centralise la création d'objets.

    Pourquoi c'est utile ?
    - Si plus tard on ajoutes d'autres types de cellules
      tu modifies la factory, pas tout le code.
    - Grid n'a pas besoin de connaître les classes concrètes.
    """

    @staticmethod
    def create(alive: bool) -> Cell:
        """
        Exemple de méthode "statique" (pas besoin d'instance).
        """
        return AliveCell() if alive else DeadCell()


# 3) GRID : composition (la grille contient des cellules)
class Grid:
    """
    Composition : Grid "possède" une matrice de Cell.
    Une grille n'existe pas sans ses cellules.

    Indices :
    - rows : nombre de lignes
    - cols : nombre de colonnes
    """

    def __init__(self, rows: int, cols: int) -> None:
        # _rows et _cols sont protégés (convention) : pas publics
        self._rows = rows
        self._cols = cols

        # Matrice 2D (liste de listes) de Cell
        # Tout démarre mort.
        self._cells: list[list[Cell]] = [
            [CellFactory.create(False) for _ in range(cols)]
            for _ in range(rows)
        ]

    #Accesseurs
    @property
    def rows(self) -> int:
        """Nombre de lignes"""
        return self._rows

    @property
    def cols(self) -> int:
        """Nombre de colonnes"""
        return self._cols

    # Iterator
    def __iter__(self) -> Iterator[tuple[int, int, Cell]]:
        """
        Iterator : permet de faire
        for r, c, cell in grid:
            ...

        Pourquoi c'est utile ?
        - évite de répéter des doubles boucles partout
        - rend le code plus lisible
        """
        for r in range(self._rows):
            for c in range(self._cols):
                yield r, c, self._cells[r][c]

    # Méthodes publiques
    def get(self, r: int, c: int) -> Cell:
        """Retourne la cellule à (r,c)."""
        return self._cells[r][c]

    def set_alive(self, r: int, c: int, alive: bool) -> None:
        """
        Remplace l'objet Cell par un AliveCell ou DeadCell.
        On utilise la Factory pour ne pas dépendre des classes concrètes.
        """
        self._cells[r][c] = CellFactory.create(alive)

    def toggle(self, r: int, c: int) -> None:
        """
        Inverse l'état (vivant <-> mort).
        """
        self.set_alive(r, c, not self.get(r, c).alive)

    def clear(self) -> None:
        """
        Met toutes les cellules à mortes.
        """
        for r, c, _ in self:
            self.set_alive(r, c, False)

    def alive_neighbors(self, r: int, c: int) -> int:
        """
        Compte les voisins vivants autour de (r,c).
        Ici : pas de wrapping (les bords ont moins de voisins).
        """
        count = 0

        # On parcourt le carré 3x3 autour de la cellule.
        for rr in range(r - 1, r + 2):
            for cc in range(c - 1, c + 2):
                # On ignore la cellule elle-même
                if rr == r and cc == c:
                    continue

                # Vérification des limites
                if 0 <= rr < self._rows and 0 <= cc < self._cols:
                    if self._cells[rr][cc].alive:
                        count += 1

        return count

    def step(self) -> None:
        """
        Avance d'une génération.
        """

        # next_alive_matrix[r][c] dira si la cellule sera vivante après step
        next_alive_matrix: list[list[bool]] = [
            [False for _ in range(self._cols)]
            for _ in range(self._rows)
        ]

        for r, c, cell in self:
            n = self.alive_neighbors(r, c)

            # Ici c'est LE polymorphisme :
            # - si cell est AliveCell, il applique la règle des vivantes
            # - si cell est DeadCell, il applique la règle des mortes
            next_alive_matrix[r][c] = cell.next_alive(n)

        # Application : remplacement des cellules (via Factory)
        for r in range(self._rows):
            for c in range(self._cols):
                self._cells[r][c] = CellFactory.create(next_alive_matrix[r][c])


# 4) LIVE MODEL : paramètres globaux du jeu (running, vitesse...)
class LiveModel:
    """
    ORAL
    LiveModel = l'objet principal du modèle.
    Il contient la Grid et les paramètres (vitesse, running, génération).
    """

    def __init__(self, rows: int, cols: int) -> None:
        self._grid = Grid(rows, cols)
        self._running = False
        self._speed_ms = 80
        self._generation = 0

    #ORAL
    @property
    def grid(self) -> Grid:
        """Accès à la grille (lecture seule)."""
        return self._grid

    #ORAL
    @property
    def running(self) -> bool:
        return self._running

    #ORAL
    @property
    def speed_ms(self) -> int:
        return self._speed_ms

    #ORAL
    @speed_ms.setter
    def speed_ms(self, value: int) -> None:
        """
        Setter avec validation :
        - évite vitesse négative/0 => bug after()
        """
        if value <= 0:
            raise ValueError("speed_ms doit être > 0")
        self._speed_ms = value

    #ORAL
    @property
    def generation(self) -> int:
        return self._generation

    # Méthodes publiques
    def start(self) -> None:
        self._running = True

    def stop(self) -> None:
        self._running = False

    def toggle_cell(self, r: int, c: int) -> None:
        self._grid.toggle(r, c)

    def clear(self) -> None:
        self._grid.clear()
        self._generation = 0

    def step(self) -> None:
        self._grid.step()
        self._generation += 1
