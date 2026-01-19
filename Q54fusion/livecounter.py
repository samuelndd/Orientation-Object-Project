"""
livecounter.py

Compteur (Observer simplifié) + Singleton optionnel.

Objectifs :
- Consigne 6 : compter le nombre de cellules vivantes.
- Justifier "Observer" : le modèle appelle counter.count_all(self) après step / toggle / config.
- Justifier "Singleton" : __new__ renvoie toujours la même instance (optionnel à l’oral).
"""

from __future__ import annotations
from typing import Any


class LiveCounter:
    """
    Compteur de cellules vivantes.

    - alive_count : nombre de cellules vivantes actuel.
    - count_all(model) : recalcul complet (fiable, simple au début).
    """

    _instance = None  # Singleton optionnel

    def __new__(cls):
        # Singleton (optionnel)
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._alive_count = 0
        return cls._instance

    @property
    def alive_count(self) -> int:
        return self._alive_count

    def reset(self) -> None:
        self._alive_count = 0

    def count_all(self, model: Any) -> None:
        """
        Recompte toutes les cellules vivantes dans le modèle.

        Notre modèle fournit :
        - model.grid itérable -> for r,c,cell in model.grid
        """
        count = 0
        for _r, _c, cell in model.grid:
            if cell.alive:
                count += 1
        self._alive_count = count

    def __str__(self) -> str:
        return f"LiveCounter: {self._alive_count} cellules vivantes"
