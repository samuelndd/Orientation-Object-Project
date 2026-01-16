# liveview.py  # gère GUI Tkinter dans le MVC

from __future__ import annotations  # Permet d'utiliser des annotations de type avant que les classes soient définies
from tkinter import Tk, Frame, Label, Entry, Button, Canvas  # Widgets Tkinter utilisés pour créer l'interface
from livecanvas import LiveCanvas  # Importe l'objet itérable + iterator (design pattern Iterator)


class LiveView:
    """
     La View s'occupe uniquement de l'affichage et des interactions utilisateur
    Elle dessine une grille PIXEL (x,y) dérivée du modèle.  # Elle convertit row/col -> x/y pour le Canvas
    """

    # On a rien a declarer ici parce que aucun attribut de classe nécessaire ici

    def __init__(self, controller) -> None:  # reçoit un contrôleur
        self.__controller = controller  #la View ne connaît que le Controller (MVC)
        self.__cell_size = 12  #taille d'une cellule en pixels
        self.__rect_by_cell: dict[tuple[int, int], int] = {}  # (row,col) -> id rectangle du Canvas

        self.__window = Tk()  # fenêtre principale Tkinter
        self.__window.title("Q54 - Game of Life")  # Titre affiché en haut de la fenêtre

        # Top bar: création de grille ---  # Zone du haut : champs rows/cols + bouton
        top = Frame(self.__window)  # conteneur de widgets
        top.pack(side="top", fill="x", padx=8, pady=8)  # Place le frame en haut avec marges

        Label(top, text="Rows:").pack(side="left")  # Texte Rows pour indiquer l'entrée des lignes
        self.__rows_entry = Entry(top, width=6)  # Champ texte (privé) pour entrer le nombre de lignes
        self.__rows_entry.insert(0, "40")  # Valeur par défaut : 40
        self.__rows_entry.pack(side="left", padx=(4, 12))  # Place le champ avec une marge

        Label(top, text="Cols:").pack(side="left")  # Texte Cols pour indiquer l'entrée des colonnes
        self.__cols_entry = Entry(top, width=6)  # Champ texte privé pour entrer le nombre de colonnes
        self.__cols_entry.insert(0, "40")  # Valeur par défaut : 40
        self.__cols_entry.pack(side="left", padx=(4, 12))  # Place le champ avec une marge

        self.__create_btn = Button(top, text="Create grid", command=self.__on_create_grid)  # Bouton création grille
        self.__create_btn.pack(side="left", padx=(0, 12))  # Place le bouton avec marge

        self.__status_label = Label(top, text="Création de grille.")  # Label (privé) pour afficher des messages
        self.__status_label.pack(side="left")  # Place le label d'état

        # --- Canvas ---  # Zone de dessin
        self.__canvas = Canvas(self.__window, width=600, height=600, bg="white")  # Canvas (privé) pour dessiner la grille
        self.__canvas.pack(side="top", padx=8, pady=8)  # Place le canvas avec marges

        # Click gauche / droit (comme le procédural)  # Events souris
        self.__canvas.bind("<Button-1>", self.__on_left_click)  # Clic gauche = rendre une cellule vivante
        self.__canvas.bind("<Button-3>", self.__on_right_click)  # Clic droit = rendre une cellule morte

    def __str__(self) -> str:  # utile pour debug si on imprime la View
        return "LiveView(Tkinter GUI)"  # Description simple






    @property
    def cell_size(self) -> int:  # Getter : fournit la taille d'une cellule pour le Controller
        return self.__cell_size






    def set_status(self, text: str) -> None:
        self.__status_label.config(text=text)  # Met à jour le texte du label

    def render_grid(self, alive_matrix: list[list[bool]]) -> None:  #dessiner la grille
         # On efface puis on redessine tout
        self.__canvas.delete("all")  # Efface tous les éléments du canvas
        self.__rect_by_cell.clear()  # Réinitialise le dictionnaire de rectangles

        rows = len(alive_matrix)  # Nombre de lignes dans la matrice bool
        cols = len(alive_matrix[0]) if rows > 0 else 0  # Nombre de colonnes (0 si la matrice vide)

        width = cols * self.__cell_size  # Largeur du canvas en pixels selon la grille
        height = rows * self.__cell_size  # Hauteur du canvas en pixels selon la grille
        self.__canvas.config(width=width, height=height)  # Adapte la taille du canvas

        # lignes grille  # Dessine les lignes pour voir le damier
        for c in range(cols + 1):  # Lignes verticales (cols+1 pour inclure bord droit)
            x = c * self.__cell_size  # Coordonnée x de la ligne verticale
            self.__canvas.create_line(x, 0, x, height)  # Trace la ligne verticale
        for r in range(rows + 1):  # Lignes horizontales (rows+1 pour inclure bord bas)
            y = r * self.__cell_size  # Coordonnée y de la ligne horizontale
            self.__canvas.create_line(0, y, width, y)  # Trace la ligne horizontale

        live_canvas = LiveCanvas(alive_matrix)  # Crée un objet itérable qui encapsule la matrice bool
        for row, col, alive in live_canvas:  # Itération via __iter__() + __next__() (design pattern Iterator)
            if alive:  # On dessine uniquement les cellules vivantes (comme avant)
                 self.__draw_cell(row, col, True)  # Dessine en noir


    def mainloop(self) -> None:  #démarre Tkinter (boucle d'événements)
        self.__window.mainloop()  # Lance l'application graphique






    def __draw_cell(self, row: int, col: int, alive: bool) -> None:  # Dessine une cellule (privé)
        x1 = col * self.__cell_size  # Coordonnée x du coin gauche
        y1 = row * self.__cell_size  # Coordonnée y du coin haut
        x2 = x1 + self.__cell_size  # Coordonnée x du coin droit
        y2 = y1 + self.__cell_size  # Coordonnée y du coin bas
        fill = "black" if alive else "white"  # Couleur selon vivant/mort (ici on utilise surtout vivant)

        rect_id = self.__canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="")  # Dessine rectangle
        self.__rect_by_cell[(row, col)] = rect_id  # Stocke l'id du rectangle (utile plus tard si optimisation)

    # Events GUI  # Callbacks privés déclenchés par les actions utilisateur

    def __on_create_grid(self) -> None:  # clic sur "Create grid"
        self.__controller.gui_create_grid(self.__rows_entry.get(), self.__cols_entry.get())  # Passe rows/cols au Controller

    def __on_left_click(self, event) -> None:  # clic gauche sur le canvas
        self.__controller.gui_canvas_click(event.x, event.y, alive=True)  # Informe le Controller : cellule vivante

    def __on_right_click(self, event) -> None:  #clic droit sur le canvas
        self.__controller.gui_canvas_click(event.x, event.y, alive=False)  # Informe le Controller : cellule morte
