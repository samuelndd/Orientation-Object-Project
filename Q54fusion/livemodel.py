"""
livemodel.py

Rôle :
- Stocker les données du jeu (grille de cellules)
- Contenir TOUTE la logique de calcul (voisins, règles, step)
- Aucune dépendance Tkinter (sinon couplage fort)

Consignes :
- MVC : model sans Tkinter ✅
- Indices standards : 0..n-1 ✅
- Strategy : Random/Canon/Empty ✅
- Observer : Counter (cells vivantes) ✅
- Iterator : Grid.__iter__ ✅
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterator, Optional


# ============================================================
# 1) CELLULES : classe abstraite + héritage + polymorphisme
# ============================================================

class Cell(ABC):
    """
    Classe abstraite : on n’instancie pas Cell directement.

    Contrat :
    - alive : bool
    - next_alive(neighbors) : calcule le prochain état
    """

    @property
    @abstractmethod
    def alive(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def next_alive(self, alive_neighbors: int) -> bool:
        raise NotImplementedError


@dataclass(frozen=True)
class AliveCell(Cell):
    """Cellule vivante."""

    @property
    def alive(self) -> bool:
        return True

    def next_alive(self, alive_neighbors: int) -> bool:
        # survit si 2 ou 3 voisins vivants
        return alive_neighbors in (2, 3)


@dataclass(frozen=True)
class DeadCell(Cell):
    """Cellule morte."""

    @property
    def alive(self) -> bool:
        return False

    def next_alive(self, alive_neighbors: int) -> bool:
        # naît si exactement 3 voisins vivants
        return alive_neighbors == 3


class CellFactory:
    """
    Factory : centralise la création des cellules.
    """

    @staticmethod
    def create(alive: bool) -> Cell:
        return AliveCell() if alive else DeadCell()


# ============================================================
# 2) STRATEGY : configurations (surplus initiative)
# ============================================================

class ConfigStrategy(ABC):
    @abstractmethod
    def apply(self, model: "LiveModel") -> None:
        raise NotImplementedError


class EmptyStrategy(ConfigStrategy):
    """Configuration vide (toutes mortes)."""

    def apply(self, model: "LiveModel") -> None:
        model.clear()


class RandomStrategy(ConfigStrategy):
    """Configuration aléatoire : X% vivantes."""

    def __init__(self, percentage: int = 25):
        self.percentage = percentage

    def apply(self, model: "LiveModel") -> None:
        import random

        model.clear()

        total = model.grid.rows * model.grid.cols
        target = int(total * self.percentage / 100)

        coords = [(r, c) for r, c, _cell in model.grid]
        if target > len(coords):
            target = len(coords)

        for (r, c) in random.sample(coords, k=target):
            model.grid.set_alive(r, c, True)

        model.reset_generation()


class CanonStrategy(ConfigStrategy):
    """Canon à planeurs (initiative)."""

    def apply(self, model: "LiveModel") -> None:
        model.clear()

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

        for r, c in canon_positions:
            if 0 <= r < model.grid.rows and 0 <= c < model.grid.cols:
                model.grid.set_alive(r, c, True)

        model.reset_generation()


# ============================================================
# 3) GRID : composition + Iterator
# ============================================================

class Grid:
    """
    Grid contient une matrice de Cell : composition.
    """

    def __init__(self, rows: int, cols: int) -> None:
        self.__rows = rows
        self.__cols = cols
        self.__cells: list[list[Cell]] = [
            [CellFactory.create(False) for _ in range(cols)]
            for _ in range(rows)
        ]

    @property
    def rows(self) -> int:
        return self.__rows

    @property
    def cols(self) -> int:
        return self.__cols

    def __iter__(self) -> Iterator[tuple[int, int, Cell]]:
        for r in range(self.__rows):
            for c in range(self.__cols):
                yield r, c, self.__cells[r][c]

    def get(self, r: int, c: int) -> Cell:
        return self.__cells[r][c]

    def set_alive(self, r: int, c: int, alive: bool) -> None:
        self.__cells[r][c] = CellFactory.create(alive)

    def toggle(self, r: int, c: int) -> None:
        self.set_alive(r, c, not self.get(r, c).alive)

    def clear(self) -> None:
        for r, c, _ in self:
            self.set_alive(r, c, False)

    def alive_neighbors(self, r: int, c: int) -> int:
        count = 0
        for rr in range(r - 1, r + 2):
            for cc in range(c - 1, c + 2):
                if rr == r and cc == c:
                    continue
                if 0 <= rr < self.__rows and 0 <= cc < self.__cols:
                    if self.__cells[rr][cc].alive:
                        count += 1
        return count

    def step(self) -> None:
        next_alive_matrix: list[list[bool]] = [
            [False for _ in range(self.__cols)]
            for _ in range(self.__rows)
        ]

        for r, c, cell in self:
            n = self.alive_neighbors(r, c)
            next_alive_matrix[r][c] = cell.next_alive(n)

        for r in range(self.__rows):
            for c in range(self.__cols):
                self.__cells[r][c] = CellFactory.create(next_alive_matrix[r][c])


# ============================================================
# 4) LIVE MODEL : paramètres + Observer + Strategy
# ============================================================

class LiveModel:
    """
    LiveModel contient :
    - grid
    - running
    - speed_ms
    - generation
    - strategy (config initiale)
    - counter (observer)
    """

    def __init__(self, rows: int, cols: int, cell_px: int = 10) -> None:
        self.__grid = Grid(rows, cols)
        self.__running = False
        self.__speed_ms = 80
        self.__generation = 0
        self.__cell_px = cell_px

        self.__strategy: Optional[ConfigStrategy] = None
        self.__counter = None

    # --- Accesseurs ---
    @property
    def grid(self) -> Grid:
        return self.__grid

    @property
    def running(self) -> bool:
        return self.__running

    @property
    def speed_ms(self) -> int:
        return self.__speed_ms

    @speed_ms.setter
    def speed_ms(self, value: int) -> None:
        if value <= 0:
            raise ValueError("speed_ms doit être > 0")
        self.__speed_ms = value

    @property
    def generation(self) -> int:
        return self.__generation

    @property
    def cell_px(self) -> int:
        return self.__cell_px

    # --- Observer ---
    def set_counter(self, counter) -> None:
        self.__counter = counter
        self.__notify_counter()

    def __notify_counter(self) -> None:
        if self.__counter:
            self.__counter.count_all(self)

    # --- Strategy ---
    def set_strategy(self, strategy: ConfigStrategy) -> None:
        self.__strategy = strategy

    def apply_strategy(self) -> None:
        if self.__strategy:
            self.__strategy.apply(self)
            self.__generation = 0
            self.__notify_counter()

    # --- Actions ---
    def start(self) -> None:
        self.__running = True

    def stop(self) -> None:
        self.__running = False

    def toggle_cell(self, r: int, c: int) -> None:
        self.__grid.toggle(r, c)
        self.__notify_counter()

    def clear(self) -> None:
        self.__grid.clear()
        self.__generation = 0
        self.__notify_counter()

    def reset_generation(self) -> None:
        self.__generation = 0

    def randomize(self, density: float = 0.25) -> None:
        import random

        for r, c, _ in self.__grid:
            self.__grid.set_alive(r, c, random.random() < density)

        self.__generation = 0
        self.__notify_counter()

    def alive_count(self) -> int:
        count = 0
        for _r, _c, cell in self.__grid:
            if cell.alive:
                count += 1
        return count

    def step(self) -> None:
        self.__grid.step()
        self.__generation += 1
        self.__notify_counter()

    # surplus utile
    def pixel_to_grid(self, pixel_x: int, pixel_y: int) -> tuple[int, int]:
        col = pixel_x // self.__cell_px
        row = pixel_y // self.__cell_px
        return row, col
