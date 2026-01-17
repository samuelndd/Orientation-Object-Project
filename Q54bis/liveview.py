"""
liveview.py

- Interface Tkinter (Canvas + boutons + champs)

BUT MVC :
- La View ne calcule pas la logique du jeu
- Elle affiche uniquement ce que le Controller lui donne
- Elle envoie les événements au Controller (clics, boutons, entrées)
"""

from __future__ import annotations

from tkinter import Tk, Canvas, Frame, Button, Label, Entry, LEFT, RIGHT, TOP
from typing import Iterator


class LiveCanvas:
    """
    LiveCanvas = composant graphique "Canvas".
    - Dessine la grille en pixels
    - Envoie les clics au controller

    CONSIGNE 4 :
    - Implémenter l’itération de sortie (affichage de la matrice)
      avec un design pattern Iterator appliqué à l’objet nécessaire (ex: LiveCanvas).
    """

    def __init__(self, parent: Frame, controller, cell_px: int, width_px: int, height_px: int):
        self.__controller = controller
        self.__cell_px = cell_px

        self.__canvas = Canvas(parent, width=width_px, height=height_px, bg="white")
        self.__canvas.pack(side=TOP, padx=5, pady=5)

        # Events -> controller
        self.__canvas.bind("<Button-1>", self.__on_left_click)   # click gauche
        self.__canvas.bind("<Button-3>", self.__on_right_click)  # click droit

    # ==========================
    # Iterator (CONSigne 4)
    # ==========================
    def __iter__(self) -> Iterator[tuple[int, int]]:
        """
        Iterator appliqué à LiveCanvas.

        BUT :
        - permettre d’itérer facilement sur toutes les cellules visibles
        - utile pour l’affichage (ex: redessiner, debug, futur refactor)

        Remarque :
        - Ici on itère sur les cellules "pixelisées" (row/col)
        - La View ne connaît PAS l’état vivant/mort (ça vient du Controller)
        """
        width_px = int(self.__canvas["width"])
        height_px = int(self.__canvas["height"])

        cols = width_px // self.__cell_px
        rows = height_px // self.__cell_px

        for r in range(rows):
            for c in range(cols):
                yield r, c

    # ==========================
    # Events souris -> controller
    # ==========================
    def __on_left_click(self, event) -> None:
        row, col = self.xy_to_rc(event.x, event.y)
        self.__controller.gui_toggle_cell(row, col)

    def __on_right_click(self, event) -> None:
        row, col = self.xy_to_rc(event.x, event.y)
        self.__controller.gui_set_dead(row, col)

    def xy_to_rc(self, x: int, y: int) -> tuple[int, int]:
        """
        Conversion pixels -> logique.
        Exemple : cell_px=10
        - pixel 0..9 => col=0
        - pixel 10..19 => col=1
        """
        col = x // self.__cell_px
        row = y // self.__cell_px
        return row, col

    # ==========================
    # Affichage Canvas
    # ==========================
    def clear(self) -> None:
        """Efface le canvas."""
        self.__canvas.delete("all")

    def draw_grid(self, rows: int, cols: int) -> None:
        """
        Dessine le quadrillage (comme procedural).
        """
        w = cols * self.__cell_px
        h = rows * self.__cell_px

        # lignes verticales
        for cx in range(0, w + 1, self.__cell_px):
            self.__canvas.create_line(cx, 0, cx, h, width=1, fill="black")

        # lignes horizontales
        for cy in range(0, h + 1, self.__cell_px):
            self.__canvas.create_line(0, cy, w, cy, width=1, fill="black")

    def draw_cell(self, row: int, col: int, alive: bool) -> None:
        """
        Dessine une cellule (rectangle).
        """
        x1 = col * self.__cell_px
        y1 = row * self.__cell_px
        x2 = x1 + self.__cell_px
        y2 = y1 + self.__cell_px

        color = "black" if alive else "white"

        # outline="" pour éviter bordure noire sur chaque cellule
        self.__canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def render(self, rows: int, cols: int, alive_cells: list[tuple[int, int]]) -> None:
        """
        Rend l'état du modèle :
        - On redessine tout (simple et fiable au début)
        - Optimisation possible plus tard (refactor)

        CONSIGNE 4 (Iterator) :
        - Ici, l’iterator LiveCanvas pourrait servir à redessiner cellule par cellule.
        - Pour l’instant, on garde la méthode simple (effacer/redessiner),
          mais l’iterator est bien implanté sur LiveCanvas.
        """
        self.clear()
        self.draw_grid(rows, cols)

        # Dessine uniquement les vivantes (venant du Controller -> Model)
        for r, c in alive_cells:
            self.draw_cell(r, c, True)


class LiveCommandBar:
    """
    Barre de commandes : boutons + champs.
    """

    def __init__(self, parent: Frame, controller):
        self.__frame = Frame(parent)
        self.__frame.pack(side=TOP, padx=5, pady=5)

        # Boutons => controller
        Button(self.__frame, text="Go!", command=controller.gui_go).pack(side=LEFT, padx=3)
        Button(self.__frame, text="Stop", command=controller.gui_stop).pack(side=LEFT, padx=3)
        Button(self.__frame, text="Step", command=controller.gui_step).pack(side=LEFT, padx=3)
        Button(self.__frame, text="Clear", command=controller.gui_clear).pack(side=LEFT, padx=3)

        # CONSIGNE 5 : bouton "Aléa"
        Button(self.__frame, text="Aléa", command=controller.gui_random).pack(side=LEFT, padx=3)

        # Taille de grille (consigne 3)
        Label(self.__frame, text="Rows,Cols :").pack(side=RIGHT)
        self.__size_entry = Entry(self.__frame, width=10)
        self.__size_entry.insert(0, "40,40")
        self.__size_entry.bind("<Return>", lambda _e: controller.gui_resize(self.__size_entry.get()))
        self.__size_entry.pack(side=RIGHT, padx=3)

        # Vitesse
        Label(self.__frame, text="Speed(ms) :").pack(side=RIGHT)
        self.__speed_entry = Entry(self.__frame, width=8)
        self.__speed_entry.insert(0, "80")
        self.__speed_entry.bind("<Return>", lambda _e: controller.gui_change_speed(self.__speed_entry.get()))
        self.__speed_entry.pack(side=RIGHT, padx=3)


class LiveView:
    """
    ORAL
    Fenêtre principale : contient les widgets.
    """

    def __init__(self, controller, cell_px: int, rows: int, cols: int):
        self.__window = Tk()
        self.__window.title("Game of Life (Q54)")

        # Commandes (boutons + entries)
        self.__cmd = LiveCommandBar(self.__window, controller)

        # Canvas (grille)
        width_px = cols * cell_px
        height_px = rows * cell_px
        self.__canvas = LiveCanvas(self.__window, controller, cell_px, width_px, height_px)

    def render(self, rows: int, cols: int, alive_cells: list[tuple[int, int]]) -> None:
        self.__canvas.render(rows, cols, alive_cells)

    def after(self, delay_ms: int, callback) -> None:
        """Expose Tk.after au controller."""
        self.__window.after(delay_ms, callback)

    def mainloop(self) -> None:
        self.__window.mainloop()
