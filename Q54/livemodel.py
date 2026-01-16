# livemodel.py  # contient le MODEL (données + logique) dans le MVC
from __future__ import annotations  # Autorise l'utilisation d'annotations de type "en avance" (pratique pour typing)






class LiveCell:  # Déclare la Classe représentant une cellule logique (vivante ou morte) du jeu

    def __init__(self, alive: bool = False) -> None:  # crée une cellule, vivante ou morte
        self.__alive: bool = bool(alive)  #état vivant ou mort avec encapsulation

    def __str__(self) -> str:  # représente les texte dans la cellule
        return "Alive" if self.__alive else "Dead"






    @property
    def alive(self) -> bool:  # Getter : permet d'accéder à l'état vivant sans exposer l'attribut privé
        return self.__alive

    @alive.setter  #setter lié à la propriété alive
    def alive(self, value: bool) -> None:  # Setter : permet de modifier l'état vivant
        self.__alive = bool(value)  # Met à jour l'attribut privé avec un bool






    def set_alive(self, value: bool) -> None: # change l'état vivant ou mort de la cellule
        self.__alive = bool(value)  # Met à jour l'état privé






class LiveModel: # stocke la grille logique


    """
    stocke la grille LOGIQUE avec indices standards:
    grid[row][col] avec row=0..rows-1, col=0..cols-1
    """

    def __init__(self) -> None:  # initialisation d'un modèle vide
        self.__rows: int = 0  # nombre de lignes (0=pas créé)
        self.__cols: int = 0  # nombre de colonnes
        self.__grid: list[list[LiveCell]] = []  # la matrice

    def __str__(self) -> str:  # afficher l'état du Model
        if not self.is_ready():  # Si la grille n'est pas prête
            return "LiveModel(not ready)"  # On retourne une info simple
        return f"LiveModel(rows={self.__rows}, cols={self.__cols})"  # Sinon on retourne dimensions






    # "getters"
    @property  #nous permet d'accéder à rows comme un attribut (m.rows) au lieu d'une méthode (m.get_rows())
    def rows(self) -> int:  # Getter : renvoie le nombre de lignes
        return self.__rows  # Retourne l'attribut privé __rows

    @property  # constucteur
    def cols(self) -> int:  # Getter : renvoie le nombre de colonnes
        return self.__cols  # Retourne l'attribut privé __cols






    def create_grid(self, rows: int, cols: int) -> None:  # elle crée une grille vide de dimension rows x cols
        """Crée une nouvelle grille vide."""
        if rows <= 0 or cols <= 0:  # Vérification si les dimensions sont valides (on refuse 0 ou négatif)
            raise ValueError("rows et cols doivent être > 0")  #si dimensions invalides

        self.__rows = rows  # Stocke le nombre de lignes dans l'attribut privé
        self.__cols = cols  # Stocke le nombre de colonnes dans l'attribut privé
        self.__grid = [[LiveCell(False) for _ in range(cols)] for _ in range(rows)]  # Crée une matrice rows x cols de cellules

    def is_ready(self) -> bool:  # indique si la grille prete
        return self.__rows > 0 and self.__cols > 0 and len(self.__grid) == self.__rows  # True si rows/cols valides et grille construite

    def get_cell(self, row: int, col: int) -> LiveCell:  # renvoie l'objet LiveCell à la position (row, col)
        self.__check_bounds(row, col)  # Vérifie que row/col sont dans les limites (sinon exception)
        return self.__grid[row][col]  # Renvoie l'objet cellule

    def set_cell_alive(self, row: int, col: int, alive: bool) -> None:  # modifie l'état d'une cellule vivante ou morte
        self.__check_bounds(row, col)  # Vérifie que la cellule existe dans la grille
        self.__grid[row][col].set_alive(alive)  # Change état via méthode de la cellule

    def snapshot_alive(self) -> list[list[bool]]:  #crée une image de la grille sous forme de bool
        """Retourne une image booléenne pour la View (sans exposer les objets)."""
        return [[cell.alive for cell in row] for row in self.__grid]  # Convertit objets -> bool






    def __check_bounds(self, row: int, col: int) -> None:  # vérifie si une position est valide (dans la grille)
        if not self.is_ready():  # Si la grille n'a pas été créée (rows=0 ou cols=0 ou grid vide)
            raise RuntimeError("Grille non créée. Utilise create_grid(rows, cols) d'abord.")  # on doit d'abord appeler create_grid
        if not (0 <= row < self.__rows and 0 <= col < self.__cols):  # Vérifie que row et col sont dans les bornes [0..rows-1] et [0..cols-1]
            raise IndexError(
                f"Cell hors limites: row={row}, col={col}")  #si on demande une cellule en dehors de la grille






if __name__ == "__main__":
    # mini test unitaire nominal (style demandé au cours)
    m = LiveModel()
    m.create_grid(5, 10) # Crée une grille 5 lignes x 10 colonnes
    assert m.rows == 5 and m.cols == 10  # Vérifie que les getters rows/cols donnent les bonnes dimensions
    m.set_cell_alive(0, 0, True)
    assert m.get_cell(0, 0).alive is True
    print("livemodel.py OK")
