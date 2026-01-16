# livecontroller.py  # fait le lien entre View (IHM) et Model (données/logique)

from __future__ import annotations  # Permet les annotations de type en avance

from livemodel import LiveModel  # Importe le Model (grille logique + cellules)
from liveview import LiveView  # Importe la View (Tkinter + canvas)


class LiveController:
    """
    - reçoit les événements de la View (boutons, clics)  # La View ne parle qu'au Controller
    - demande au Model de modifier les données  # Le Model ne dépend de personne
    - demande à la View de redessiner  # La View affiche le résultat
    """

    # Aucun attribut de classe nécessaire ici  # Donc rien à déclarer

    def __init__(self) -> None:
        self.__model: LiveModel = LiveModel()  # instance du Model (grille logique)
        self.__view: LiveView = LiveView(self)  #  instance de la View
        self.__view.set_status("Entrez rows/cols puis cliquez 'Create grid'.")
        self.__view.mainloop()  # Lance la boucle Tkinter (programme événementiel)

    def __str__(self) -> str:
        return "LiveController(MVC orchestrator)"






    def gui_create_grid(self, rows_text: str, cols_text: str) -> None:  # Appelée quand on clique sur "Create grid"
        """
        1) Valide les entrées (rows/cols)  # Le Controller vérifie les données de l'utilisateur
        2) Demande au Model de créer la grille  # Model = logique
        3) Demande à la View d'afficher la grille  # View = affichage
        """
        try:  # pour gérer les erreurs de conversion proprement
            rows = int(rows_text)  # Convertit le texte "rows" en entier
            cols = int(cols_text)  # Convertit le texte "cols" en entier
        except ValueError:  # Si l'utilisateur n'a pas tapé un nombre
            self.__view.set_status("Erreur: rows/cols doivent être des entiers.")
            return

        try:  # pour gérer les ValueError du Model (rows/cols <= 0)
            self.__model.create_grid(rows, cols)  # Crée la grille logique (row/col standards) dans le Model
        except ValueError as e:  # Si rows/cols invalides (<= 0)
            self.__view.set_status(f"Erreur: {e}")
            return

        alive_matrix = self.__model.snapshot_alive()  # Demande au Model une matrice bool (True/False) pour la View
        self.__view.render_grid(alive_matrix)  # Demande à la View de dessiner la grille (damier + cellules vivantes)
        self.__view.set_status(f"Grille créée: {rows} x {cols}. Clic gauche=vivant, clic droit=mort.")

    def gui_canvas_click(self, x: int, y: int, alive: bool) -> None:
        """
        Reçoit un clic pixel (x,y) de la View  # View travaille en pixels
        Convertit en indices logiques (row,col)  # Model travaille en indices standards
        Met à jour le Model, puis redessine la View  # Synchronisation MVC
        """
        if not self.__model.is_ready():  # Si l'utilisateur clique avant d'avoir créé une grille
            self.__view.set_status("Crée d'abord une grille (bouton 'Create grid').")
            return

        cell_size = self.__view.cell_size  # Récupère la taille d'une cellule en pixels (via property, pas d'accès direct)
        if cell_size <= 0:  # cell_size doit être > 0
            self.__view.set_status("Erreur interne: cell_size invalide.")
            return

        col = x // cell_size  # Convertit la coordonnée x (pixel) en colonne (index)
        row = y // cell_size  # Convertit la coordonnée y (pixel) en ligne (index)

        try:  # car set_cell_alive peut lever IndexError si on clique hors canvas
            self.__model.set_cell_alive(row, col, alive)  # Met à jour la cellule logique (row,col) dans le Model
        except IndexError:
            self.__view.set_status("Clic hors de la grille.")
            return
        except RuntimeError as e:  # Si grille pas prête (sécurité)
            self.__view.set_status(str(e))  # Affiche l'erreur du Model
            return

        alive_matrix = self.__model.snapshot_alive()  # Récupère la nouvelle matrice bool après modification
        self.__view.render_grid(alive_matrix)  # Redessine la grille (simple pour l'étape 1)






if __name__ == "__main__":  # Permet de lancer ce fichier directement pour tester le Controller
    LiveController()  # Crée l'application (instancie Model + View et démarre mainloop)
