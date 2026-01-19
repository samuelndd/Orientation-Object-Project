"""
liveview.py

View Tkinter :
- affiche la grille
- envoie les événements au controller
- ne contient PAS la logique du jeu (MVC)

Consigne 4 :
- Iterator appliqué à LiveCanvas : __iter__() pour parcourir toutes les cellules affichables.
"""

from __future__ import annotations

from tkinter import Tk, Canvas, Frame, Button, Label, Entry, LEFT, RIGHT, TOP, BOTH, X
from typing import Iterator, Optional


class LiveCanvas:
    """
    Canvas graphique :
    - affichage
    - clics -> controller
    - Iterator (consigne 4)
    """

    def __init__(self, parent: Frame, controller, cell_px: int, width_px: int, height_px: int):
        self.__controller = controller
        self.__cell_px = cell_px
        self.__width_px = width_px
        self.__height_px = height_px

        self.__canvas = Canvas(parent, width=width_px, height=height_px, bg="white")
        self.__canvas.pack(side=TOP, padx=5, pady=5)

        self.__canvas.bind("<Button-1>", self.__on_left_click)
        self.__canvas.bind("<Button-3>", self.__on_right_click)

    # Iterator (consigne 4)
    def __iter__(self) -> Iterator[tuple[int, int]]:
        cols = self.__width_px // self.__cell_px
        rows = self.__height_px // self.__cell_px
        for r in range(rows):
            for c in range(cols):
                yield r, c

    def __on_left_click(self, event) -> None:
        row, col = self.xy_to_rc(event.x, event.y)
        self.__controller.gui_toggle_cell(row, col)

    def __on_right_click(self, event) -> None:
        row, col = self.xy_to_rc(event.x, event.y)
        self.__controller.gui_set_dead(row, col)

    def xy_to_rc(self, x: int, y: int) -> tuple[int, int]:
        col = x // self.__cell_px
        row = y // self.__cell_px
        return row, col

    def clear(self) -> None:
        self.__canvas.delete("all")

    def draw_grid(self, rows: int, cols: int) -> None:
        w = cols * self.__cell_px
        h = rows * self.__cell_px

        for cx in range(0, w + 1, self.__cell_px):
            self.__canvas.create_line(cx, 0, cx, h, width=1, fill="black")
        for cy in range(0, h + 1, self.__cell_px):
            self.__canvas.create_line(0, cy, w, cy, width=1, fill="black")

    def draw_cell(self, row: int, col: int, alive: bool) -> None:
        x1 = col * self.__cell_px
        y1 = row * self.__cell_px
        x2 = x1 + self.__cell_px
        y2 = y1 + self.__cell_px
        color = "black" if alive else "white"
        self.__canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def render(self, rows: int, cols: int, alive_cells: list[tuple[int, int]]) -> None:
        self.clear()
        self.draw_grid(rows, cols)
        for r, c in alive_cells:
            self.draw_cell(r, c, True)


class LiveCommandBar:
    """
    Barre de commandes (boutons + entrées)
    """

    def __init__(self, parent: Frame, controller):
        self.__controller = controller

        self.__frame = Frame(parent, pady=5)
        self.__frame.pack(side=TOP, padx=5, pady=5, fill=X)

        Button(self.__frame, text="Go!", command=controller.gui_go).pack(side=LEFT, padx=3)
        Button(self.__frame, text="Stop", command=controller.gui_stop).pack(side=LEFT, padx=3)
        Button(self.__frame, text="Step", command=controller.gui_step).pack(side=LEFT, padx=3)
        Button(self.__frame, text="Clear", command=controller.gui_clear).pack(side=LEFT, padx=3)

        # Consigne 5 : Aléa
        Button(self.__frame, text="Aléa", command=controller.gui_random).pack(side=LEFT, padx=3)

        # Initiative : Canon (si controller a gui_canon)
        if hasattr(controller, "gui_canon"):
            Button(self.__frame, text="Canon", command=controller.gui_canon).pack(side=LEFT, padx=3)

        # Consigne 3 : resize
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
    Fenêtre Tkinter :
    - contient cmd bar + canvas + info bar
    """

    def __init__(self, controller, cell_px: int, rows: int, cols: int):
        self.__window = Tk()
        self.__window.title("Game of Life (Q54)")
        self.__window.resizable(False, False)

        self.__main_frame = Frame(self.__window)
        self.__main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.__cmd = LiveCommandBar(self.__window, controller)

        width_px = cols * cell_px
        height_px = rows * cell_px
        self.__canvas = LiveCanvas(self.__window, controller, cell_px, width_px, height_px)

        # info bar
        self.__generation_label: Optional[Label] = None
        self.__alive_label: Optional[Label] = None
        self.__create_info_bar(self.__main_frame)

    def __create_info_bar(self, parent: Frame) -> None:
        info_frame = Frame(parent, pady=8)
        info_frame.pack(fill=X, pady=(5, 0))

        self.__generation_label = Label(info_frame, text="Génération: 0")
        self.__generation_label.pack(side=LEFT, padx=20)

        self.__alive_label = Label(info_frame, text="Cellules vivantes: 0")
        self.__alive_label.pack(side=LEFT, padx=20)

        instructions = Label(info_frame, text="Clic gauche: toggle • Clic droit: tuer")
        instructions.pack(side=RIGHT, padx=20)

    def render(self, rows: int, cols: int, alive_cells: list[tuple[int, int]], generation: int = 0, alive_count: int = 0) -> None:
        """
        API MVC :
        Controller -> View : affiche ce qu'on lui donne.
        """
        self.__canvas.render(rows, cols, alive_cells)

        # update info bar
        if self.__generation_label is not None:
            self.__generation_label.config(text=f"Génération: {generation}")
        if self.__alive_label is not None:
            self.__alive_label.config(text=f"Cellules vivantes: {alive_count}")

        self.__window.update()

    def after(self, delay_ms: int, callback) -> None:
        self.__window.after(delay_ms, callback)

    def mainloop(self) -> None:
        self.__window.mainloop()
