"""
livecontroller.py

Controller MVC :
- reçoit les events de la View
- modifie le Model
- demande à la View d'afficher

Fusion :
- ta base MVC
- + Strategy (Empty/Random/Canon)
- + Counter (Observer)
"""

from __future__ import annotations

from livemodel import LiveModel, RandomStrategy, CanonStrategy, EmptyStrategy
from liveview import LiveView
from livecounter import LiveCounter


class LiveController:
    @classmethod
    def default_controller(cls) -> "LiveController":
        return cls(rows=40, cols=40, cell_px=10)

    def __init__(self, rows: int = 40, cols: int = 40, cell_px: int = 10):
        # Model
        self.__model = LiveModel(rows, cols, cell_px=cell_px)

        # Counter (Observer)
        self.__counter = LiveCounter()
        self.__model.set_counter(self.__counter)

        # Strategies
        self.__strategy_empty = EmptyStrategy()
        self.__strategy_random = RandomStrategy(percentage=25)
        self.__strategy_canon = CanonStrategy()

        # Config départ : vide
        self.__model.set_strategy(self.__strategy_empty)
        self.__model.apply_strategy()

        # View
        self.__view = LiveView(self, cell_px=cell_px, rows=rows, cols=cols)

        # Premier affichage
        self.gui_render()

        # Lancement GUI
        self.__view.mainloop()

    # ------------------------------------
    # Helper : liste vivantes
    # ------------------------------------
    def __alive_cells(self) -> list[tuple[int, int]]:
        out: list[tuple[int, int]] = []
        for r, c, cell in self.__model.grid:
            if cell.alive:
                out.append((r, c))
        return out

    # ------------------------------------
    # Rendu
    # ------------------------------------
    def gui_render(self) -> None:
        # console (consigne 6 alternative)
        print(
            f"[GEN={self.__model.generation}] "
            f"alive={self.__model.alive_count()} "
            f"running={self.__model.running} "
            f"counter_alive={self.__counter.alive_count}"
        )

        # GUI
        self.__view.render(
            rows=self.__model.grid.rows,
            cols=self.__model.grid.cols,
            alive_cells=self.__alive_cells(),
            generation=self.__model.generation,
            alive_count=self.__counter.alive_count,
        )

    # ------------------------------------
    # boucle after
    # ------------------------------------
    def __tick(self) -> None:
        if not self.__model.running:
            return

        self.__model.step()
        self.gui_render()
        self.__view.after(self.__model.speed_ms, self.__tick)

    # ------------------------------------
    # handlers GUI
    # ------------------------------------
    def gui_go(self) -> None:
        self.__model.start()
        self.__tick()

    def gui_stop(self) -> None:
        self.__model.stop()

    def gui_step(self) -> None:
        self.__model.stop()
        self.__model.step()
        self.gui_render()

    def gui_clear(self) -> None:
        self.__model.stop()
        self.__model.set_strategy(self.__strategy_empty)
        self.__model.apply_strategy()
        self.gui_render()

    def gui_random(self) -> None:
        self.__model.stop()
        self.__model.set_strategy(self.__strategy_random)
        self.__model.apply_strategy()
        self.gui_render()

    def gui_canon(self) -> None:
        self.__model.stop()
        self.__model.set_strategy(self.__strategy_canon)
        self.__model.apply_strategy()
        self.gui_render()

    def gui_change_speed(self, txt: str) -> None:
        self.__model.speed_ms = int(txt)

    def gui_resize(self, txt: str) -> None:
        self.__model.stop()

        parts = [p.strip() for p in txt.split(",")]
        rows = int(parts[0])
        cols = int(parts[1])

        # recrée le modèle
        self.__model = LiveModel(rows, cols, cell_px=self.__model.cell_px)
        self.__model.set_counter(self.__counter)

        # config vide
        self.__model.set_strategy(self.__strategy_empty)
        self.__model.apply_strategy()

        self.gui_render()

    def gui_toggle_cell(self, row: int, col: int) -> None:
        if 0 <= row < self.__model.grid.rows and 0 <= col < self.__model.grid.cols:
            self.__model.toggle_cell(row, col)
            self.gui_render()

    def gui_set_dead(self, row: int, col: int) -> None:
        if 0 <= row < self.__model.grid.rows and 0 <= col < self.__model.grid.cols:
            self.__model.grid.set_alive(row, col, False)
            self.gui_render()
