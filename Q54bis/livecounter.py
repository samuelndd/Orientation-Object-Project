"""
livecounter.py
Compteur de générations (Singleton optionnel).
But : montrer un design pattern "justifié" (défense orale).

REMARQUE :
- Pour l’instant tu comptes déjà via LiveModel.generation et alive_count()
- Le Singleton est surtout pour la démonstration "pattern" à l’oral.
"""

class LiveCounter:
    _instance = None

    def __new__(cls):
        # Singleton : une seule instance possible
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._value = 0
        return cls._instance

    @property
    def value(self) -> int:
        return self._value

    def reset(self) -> None:
        self._value = 0

    def inc(self) -> None:
        self._value += 1
