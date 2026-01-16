"""
livecontroller.py

Rôle :
- Recevoir les événements de la View (boutons, clics, entrée)
- Appeler le Model (modif / calcul)
- Demander à la View de s'afficher (render)
"""

from __future__ import annotations

from livemodel import LiveModel
from liveview import LiveView


class LiveController:
    """
    ORAL
    Le controller possède :
    - un model (données + logique)
    - une view (GUI)
    """

    #ORAL
    # Exemple de utile à l’oral)
    @classmethod
    def default_controller(cls) -> "LiveController":
        """
        Méthode de classe :
        - Elle reçoit 'cls' (la classe), pas 'self' (une instance).
        - Sert à créer un controller avec des valeurs par défaut.
        """
        return cls(rows=40, cols=40, cell_px=10)

    def __init__(self, rows: int = 40, cols: int = 40, cell_px: int = 10):
        # Le model est créé ici : indices logiques 0..n-1
        self._model = LiveModel(rows, cols)

        # La view est créée ici : gère pixels + events Tkinter
        self._view = LiveView(self, cell_px=cell_px, rows=rows, cols=cols)

        # Premier affichage
        self.gui_render()

        # Lancement boucle Tkinter (bloquant)
        self._view.mainloop()

    # Helpers internes
    def _alive_cells(self) -> list[tuple[int, int]]:
        """
        Transforme le modèle en "liste de cellules vivantes".
        """
        out: list[tuple[int, int]] = []
        for r, c, cell in self._model.grid:
            if cell.alive:
                out.append((r, c))
        return out

    def gui_render(self) -> None:
        """
        ORAL
        Controller -> View : on envoie les données utiles à afficher.
        """
        self._view.render(
            rows=self._model.grid.rows,
            cols=self._model.grid.cols,
            alive_cells=self._alive_cells(),
        )

    def _tick(self) -> None:
        """
        Équivalent de fen.after(vitesse, play) dans la version procédurale.
        - si running => step + render + reprogrammer
        """
        if not self._model.running:
            return

        self._model.step()
        self.gui_render()

        # Reprogrammer _tick dans speed_ms ms
        self._view.after(self._model.speed_ms, self._tick)

    # Handlers GUI (publics)
    def gui_go(self) -> None:
        """Bouton Go! : start + lancer boucle."""
        self._model.start()
        self._tick()

    def gui_stop(self) -> None:
        """Bouton Stop : stop => _tick se stoppe tout seul."""
        self._model.stop()

    def gui_step(self) -> None:
        """Bouton Step : une génération."""
        self._model.step()
        self.gui_render()

    def gui_clear(self) -> None:
        """Bouton Clear : vider grille."""
        self._model.clear()
        self.gui_render()

    def gui_change_speed(self, txt: str) -> None:
        """Entrée speed : setter avec validation."""
        self._model.speed_ms = int(txt)

    def gui_resize(self, txt: str) -> None:
        """
        Consigne 3 : l'utilisateur peut créer grille dimension donnée.
        Format : "rows,cols"
        """
        parts = [p.strip() for p in txt.split(",")]
        rows = int(parts[0])
        cols = int(parts[1])

        # Recréation du modèle (simple et propre au début)
        self._model = LiveModel(rows, cols)
        self.gui_render()

    def gui_toggle_cell(self, row: int, col: int) -> None:
        """Click gauche : toggle (vivant/mort)."""
        if 0 <= row < self._model.grid.rows and 0 <= col < self._model.grid.cols:
            self._model.toggle_cell(row, col)
            self.gui_render()

    def gui_set_dead(self, row: int, col: int) -> None:
        """Click droit : forcer mort."""
        if 0 <= row < self._model.grid.rows and 0 <= col < self._model.grid.cols:
            self._model.grid.set_alive(row, col, False)
            self.gui_render()
