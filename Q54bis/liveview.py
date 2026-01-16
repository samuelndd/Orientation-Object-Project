"""
liveview.py
"""

from __future__ import annotations

from tkinter import Tk, Canvas, Frame, Button, Label, Entry, LEFT, RIGHT, TOP


class LiveCanvas:
    """
    LiveCanvas = composant graphique "Canvas".
    - Dessine la grille en pixels
    - Envoie les clics au controller
    """

    def __init__(self, parent: Frame, controller, cell_px: int, width_px: int, height_px: int):
        self._controller = controller
        self._cell_px = cell_px

        self._canvas = Canvas(parent, width=width_px, height=height_px, bg="white")
        self._canvas.pack(side=TOP, padx=5, pady=5)

        # Events -> controller
        self._canvas.bind("<Button-1>", self._on_left_click)   # click gauche
        self._canvas.bind("<Button-3>", self._on_right_click)  # click droit

    def _on_left_click(self, event) -> None:
        row, col = self.xy_to_rc(event.x, event.y)
        self._controller.gui_toggle_cell(row, col)

    def _on_right_click(self, event) -> None:
        row, col = self.xy_to_rc(event.x, event.y)
        self._controller.gui_set_dead(row, col)

    def xy_to_rc(self, x: int, y: int) -> tuple[int, int]:
        """
        Conversion pixels -> logique.
        Exemple : cell_px=10
        - pixel 0..9 => col=0
        - pixel 10..19 => col=1
        """
        col = x // self._cell_px
        row = y // self._cell_px
        return row, col

    def clear(self) -> None:
        """Efface le canvas."""
        self._canvas.delete("all")

    def draw_grid(self, rows: int, cols: int) -> None:
        """
        Dessine le quadrillage (comme procedural).
        """
        w = cols * self._cell_px
        h = rows * self._cell_px

        # lignes verticales
        for cx in range(0, w + 1, self._cell_px):
            self._canvas.create_line(cx, 0, cx, h, width=1, fill="black")

        # lignes horizontales
        for cy in range(0, h + 1, self._cell_px):
            self._canvas.create_line(0, cy, w, cy, width=1, fill="black")

    def draw_cell(self, row: int, col: int, alive: bool) -> None:
        """
        Dessine une cellule (rectangle).
        """
        x1 = col * self._cell_px
        y1 = row * self._cell_px
        x2 = x1 + self._cell_px
        y2 = y1 + self._cell_px

        color = "black" if alive else "white"

        # outline="" pour éviter bordure noire sur chaque cellule
        self._canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def render(self, rows: int, cols: int, alive_cells: list[tuple[int, int]]) -> None:
        """
        Rend l'état du modèle :
        - On redessine tout (simple et fiable au début)
        - Optimisation possible plus tard (refactor)
        """
        self.clear()
        self.draw_grid(rows, cols)
        for r, c in alive_cells:
            self.draw_cell(r, c, True)


class LiveCommandBar:
    """
    Barre de commandes : boutons + champs.
    """

    def __init__(self, parent: Frame, controller):
        self._frame = Frame(parent)
        self._frame.pack(side=TOP, padx=5, pady=5)

        # Boutons => controller
        Button(self._frame, text="Go!", command=controller.gui_go).pack(side=LEFT, padx=3)
        Button(self._frame, text="Stop", command=controller.gui_stop).pack(side=LEFT, padx=3)
        Button(self._frame, text="Step", command=controller.gui_step).pack(side=LEFT, padx=3)
        Button(self._frame, text="Clear", command=controller.gui_clear).pack(side=LEFT, padx=3)

        # Taille de grille (consigne 3)
        Label(self._frame, text="Rows,Cols :").pack(side=RIGHT)
        self._size_entry = Entry(self._frame, width=10)
        self._size_entry.insert(0, "40,40")
        self._size_entry.bind("<Return>", lambda _e: controller.gui_resize(self._size_entry.get()))
        self._size_entry.pack(side=RIGHT, padx=3)

        # Vitesse
        Label(self._frame, text="Speed(ms) :").pack(side=RIGHT)
        self._speed_entry = Entry(self._frame, width=8)
        self._speed_entry.insert(0, "80")
        self._speed_entry.bind("<Return>", lambda _e: controller.gui_change_speed(self._speed_entry.get()))
        self._speed_entry.pack(side=RIGHT, padx=3)


class LiveView:
    """
    ORAL
    Fenêtre principale : contient les widgets.
    """

    def __init__(self, controller, cell_px: int, rows: int, cols: int):
        self._window = Tk()
        self._window.title("Game of Life (Q54)")

        self._cmd = LiveCommandBar(self._window, controller)

        width_px = cols * cell_px
        height_px = rows * cell_px
        self._canvas = LiveCanvas(self._window, controller, cell_px, width_px, height_px)

    def render(self, rows: int, cols: int, alive_cells: list[tuple[int, int]]) -> None:
        self._canvas.render(rows, cols, alive_cells)

    def after(self, delay_ms: int, callback) -> None:
        """Expose Tk.after au controller."""
        self._window.after(delay_ms, callback)

    def mainloop(self) -> None:
        self._window.mainloop()
