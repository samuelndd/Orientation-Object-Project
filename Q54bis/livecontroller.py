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

    MVC :
    View -> Controller -> Model
    puis Controller -> View (render)
    """

    # ORAL : exemple de méthode de classe
    @classmethod
    def default_controller(cls) -> "LiveController":
        """
        Méthode de classe :
        - Elle reçoit 'cls' (la classe), pas 'self' (une instance).
        - Sert à créer un controller avec des valeurs par défaut.
        """
        return cls(rows=40, cols=40, cell_px=10)

    def __init__(self, rows: int = 40, cols: int = 40, cell_px: int = 10):
        # Le model est créé ici : indices logiques 0..n-1 (consigne 2)
        self.__model = LiveModel(rows, cols)

        # La view est créée ici : gère pixels + events Tkinter (consigne 2)
        self.__view = LiveView(self, cell_px=cell_px, rows=rows, cols=cols)

        # Premier affichage
        self.gui_render()

        # OPTIONNEL (si tu veux comme procedural : démarrer direct)
        # self.gui_go()

        # Lancement boucle Tkinter (bloquant)
        self.__view.mainloop()

    # Helpers internes (méthodes privées/protégées : ici privées)
    def __alive_cells(self) -> list[tuple[int, int]]:
        """
        Transforme le modèle en "liste de cellules vivantes".
        C'est ce qu'on envoie à la View pour dessiner.
        """
        out: list[tuple[int, int]] = []
        for r, c, cell in self.__model.grid:
            if cell.alive:
                out.append((r, c))
        return out

    def gui_render(self) -> None:
        """
        ORAL
        Controller -> View : on envoie les données utiles à afficher.

        CONSIGNE 6 :
        - afficher nombre de cellules vivantes (ici en console)
        """
        print(
            f"[GEN={self.__model.generation}] "
            f"alive={self.__model.alive_count()} "
            f"running={self.__model.running}"
        )

        self.__view.render(
            rows=self.__model.grid.rows,
            cols=self.__model.grid.cols,
            alive_cells=self.__alive_cells(),
        )

    def __tick(self) -> None:
        """
        Boucle after()
        Équivalent de fen.after(vitesse, play) dans la version procédurale.
        - si running => step + render + reprogrammer
        """
        if not self.__model.running:
            return

        self.__model.step()
        self.gui_render()

        # Reprogrammer __tick dans speed_ms ms
        self.__view.after(self.__model.speed_ms, self.__tick)

    # Handlers GUI (publics) : ce sont les méthodes appelées par Tkinter
    def gui_go(self) -> None:
        """Bouton Go! : start + lancer boucle."""
        self.__model.start()
        self.__tick()

    def gui_stop(self) -> None:
        """Bouton Stop : stop => __tick se stoppe tout seul."""
        self.__model.stop()

    def gui_step(self) -> None:
        """Bouton Step : une génération."""
        self.__model.step()
        self.gui_render()

    def gui_clear(self) -> None:
        """Bouton Clear : vider grille."""
        self.__model.clear()
        self.gui_render()

    def gui_random(self) -> None:
        """CONSIGNE 5 : bouton Aléa (25% vivantes)."""
        self.__model.randomize(0.25)
        self.gui_render()

    def gui_change_speed(self, txt: str) -> None:
        """Entrée speed : setter avec validation."""
        self.__model.speed_ms = int(txt)

    def gui_resize(self, txt: str) -> None:
        """
        Consigne 3 : l'utilisateur peut créer grille dimension donnée.
        Format : "rows,cols"
        """
        parts = [p.strip() for p in txt.split(",")]
        rows = int(parts[0])
        cols = int(parts[1])

        # Recréation du modèle (simple et propre au début)
        self.__model = LiveModel(rows, cols)
        self.gui_render()

    def gui_toggle_cell(self, row: int, col: int) -> None:
        """Click gauche : toggle (vivant/mort)."""
        if 0 <= row < self.__model.grid.rows and 0 <= col < self.__model.grid.cols:
            self.__model.toggle_cell(row, col)
            self.gui_render()

    def gui_set_dead(self, row: int, col: int) -> None:
        """Click droit : forcer mort."""
        if 0 <= row < self.__model.grid.rows and 0 <= col < self.__model.grid.cols:
            self.__model.grid.set_alive(row, col, False)
            self.gui_render()
