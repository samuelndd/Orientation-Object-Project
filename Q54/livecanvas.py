# livecanvas.py
from __future__ import annotations  # Permet d'utiliser des annotations de type en avance

class LiveCanvasIterator:
    """
    Iterator (design pattern)
    - Parcourt une matrice bool (alive_matrix)  # True = vivant, False = mort
    - Retourne à chaque __next__() un triplet (row, col, alive)  # format pratique pour la View
    """

    def __init__(self, alive_matrix: list[list[bool]]) -> None:  #reçoit la matrice à parcourir
        self.__alive_matrix: list[list[bool]] = alive_matrix  #matrice bool
        self.__rows: int = len(alive_matrix)  # nombre de lignes
        self.__cols: int = len(alive_matrix[0]) if self.__rows > 0 else 0  #  nombre de colonnes
        self.__row_index: int = 0  # position courante en ligne
        self.__col_index: int = 0  # position courante en colonne

    def __iter__(self) -> LiveCanvasIterator:  # un iterator retourne toujours lui-même
        return self  # Permet : for x in iterator

    def __next__(self) -> tuple[int, int, bool]:  #donne l’élément suivant ou StopIteration
        if self.__row_index >= self.__rows:  # Si on a dépassé la dernière ligne
            raise StopIteration

        alive: bool = self.__alive_matrix[self.__row_index][self.__col_index]  # Lit l’état de la cellule courante
        row: int = self.__row_index  # Copie la ligne courante
        col: int = self.__col_index  # Copie la colonne courante

        self.__col_index += 1  # Passe à la colonne suivante

        if self.__col_index >= self.__cols:  # Si on a dépassé la dernière colonne
            self.__col_index = 0  # On revient à la colonne 0
            self.__row_index += 1  # Et on passe à la ligne suivante

        return row, col, alive  # Retourne un triplet exploitable par la View


class LiveCanvas:  # Objet "itérable" : encapsule la matrice et fournit l'iterator (pattern Iterator)
    """
    - Contient une matrice bool (alive_matrix)  # La "photo" du modèle
    - Fournit un iterator via __iter__()  # Design Pattern Iterator
    """

    # (Attributs de classe)  # Critère prof : attributs de classe en premier si existants
    # Aucun attribut de classe ici  # Donc rien à mettre

    def __init__(self, alive_matrix: list[list[bool]]) -> None:  # Constructeur : reçoit la matrice à afficher
        self.__alive_matrix: list[list[bool]] = alive_matrix  # Attribut privé : matrice bool stockée

    def __del__(self) -> None:  # Destructeur éventuel
        pass  # Rien de spécial ici

    def __str__(self) -> str:  # debug lisible
        rows: int = len(self.__alive_matrix)  # Calcule le nombre de lignes
        cols: int = len(self.__alive_matrix[0]) if rows > 0 else 0  # Calcule le nombre de colonnes
        return f"LiveCanvas(rows={rows}, cols={cols})"

    def __iter__(self) -> LiveCanvasIterator:
        return LiveCanvasIterator(self.__alive_matrix)  # Retourne un iterator dédié (pattern Iterator)
