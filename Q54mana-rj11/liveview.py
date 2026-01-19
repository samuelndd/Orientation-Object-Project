from tkinter import *


# ============================================================================
# PATTERN ITERATOR : Pour parcourir les cellules
# ============================================================================

class CellIterator:
    """Itérateur pour parcourir toutes les cellules de la grille
    Pattern Iterator explicite
    """

    def __init__(self, model):
        self._model = model
        self._cells = list(model.get_all_cells())   # on récupère toutes les cellules
        self._index = 0

    def __iter__(self):
        """Retourne l'itérateur lui-meme"""
        return self

    def __next__(self):
        """Retourne la prochaine cellule"""
        if self._index >= len(self._cells):
            raise StopIteration

        call = self._cells[self._index]
        self._index += 1
        return call

# ============================================================================
# CANVAS - Affichage de la grille
# ============================================================================

class LiveCanvas:
    """
    il gère l'affichage de l grille et des cellules
    Implémente le pattern Iterator pour parcourir les cellules
    """

    def __init__(self, parent, width: int, height: int, cell_size: int, controller):
        self._width = width
        self._height = height
        self._cell_size = cell_size
        self._controller = controller

        # créer le canvas tkinter
        self._canvas = Canvas(parent, width=width, height=height, bg="white")
        self._canvas.pack(side=TOP, padx=5, pady=5)

        self._bind_clicks()
        self.draw_grid()

    def _bind_clicks(self):
        """ lie les clics souris au controller"""
        self._canvas.bind("<Button-1>", self._on_left_click)
        self._canvas.bind("<Button-3>", self._on_right_click)

    def _on_left_click(self, event):
        """Clic gauche : active/desactive une cellule"""
        self._controller.gui_cell_click(event.x, event.y, 1)

    def _on_right_click(self, event):
        """Clic droit : tue une cellule"""
        self._controller.gui_cell_click(event.x, event.y, 3)

    def draw_grid(self):
        """Dessine les lignes de la grille"""
        # ligne verticales
        for x in range(0, self._width + 1, self._cell_size):
            self._canvas.create_line(x, 0, x, self._height, width=1, fill="black")

        for y in range(0, self._height + 1, self._cell_size):
            self._canvas.create_line(0, y, self._width, y, width=1, fill="black")

    def draw_cell(self, x: int, y: int, alive: bool):
        """
        Dessine la cellule.
        :param x: Position X (indice de la grille)
        :param y: Position Y (indice de la grille)
        :param alive: True=noire, False=blanche
        """
        pixel_x = x * self._cell_size
        pixel_y = y * self._cell_size

        color = 'black' if alive else 'white'
        self._canvas.create_rectangle(
            pixel_x, pixel_y,
            pixel_x + self._cell_size, pixel_y + self._cell_size,
            fill=color, outline="black"
        )

    def clear(self):
        """Efface tout les canvas"""
        self._canvas.delete(ALL)

    def redraw(self, model):
        """
        Redessine toutes les cellules,
        Utilise le pattern Iterator via model.get_all_cells()
        :param model:
        :return:
        """
        self.clear()
        self.draw_grid()

        # Tiliser l'itérateur explicite (pattern Iterator)
        for cell in CellIterator(model):
            self.draw_cell(cell.x, cell.y, cell.is_alive())

# ============================================================================
# BARRE DE COMMANDES
# ============================================================================

class LiveCommandBar:
    """
    Barre de commandes avec les boutons et le champ de vitesse
    :return:
    """
    def __init__(self, parent, controller):
        self._controller = controller
        self._parent = parent

        # frame pour les boutons
        self._frame = Frame(parent, bg='lightblue', pady=5)
        self._frame.pack(fill=X, padx=5, pady=5)

        self._create_buttons()
        self._create_speed_entry()

    def _create_buttons(self):
        """ je crée les boutons de controle. Go, Stop, Canon, Aléa"""
        # bouton Go (démarrer)
        btn_go = Button(self._frame, text='Go!', command=self._controller.gui_go, width=10)
        btn_go.pack(side=LEFT, padx=3, pady=3)

        # bouton Stop (pause)
        btn_stop = Button(self._frame, text='Stop', command=self._controller.gui_stop, width=10)
        btn_stop.pack(side=LEFT, padx=3, pady=3)

        # Bouton Reset
        btn_reset = Button(self._frame, text='Reset', command=self._controller.gui_reset, width=10)
        btn_reset.pack(side=LEFT, padx=3, pady=3)

        # Bouton Step (une génération)
        btn_step = Button(self._frame, text='Step', command=self._controller.gui_step, width=10)
        btn_step.pack(side=LEFT, padx=3, pady=3)

        # Bouton Canon à planeurs
        btn_canon = Button(self._frame, text='Canon planeur', command=self._controller.gui_canon, width=10)
        btn_canon.pack(side=LEFT, padx=3, pady=3)

        # Bouton aléatoire
        btn_random = Button(self._frame, text='Aléa', command=self._controller.gui_random, width=10)
        btn_random.pack(side=LEFT, padx=3, pady=3)

        # Bouton Vider (Empty)
        btn_empty = Button(self._frame, text='Vider', command=self._controller.gui_empty, width=10)
        btn_empty.pack(side=LEFT, padx=3, pady=3)

    def _create_speed_entry(self):
        """Cree le champ de vitesse"""
        label = Label(self._frame, text="Attente entre chaque étape (ms) :")
        label.pack(side=RIGHT, padx=5)

        entry = Entry(self._frame, width=10)
        entry.insert(0, "100")  # Valeur par défaut
        entry.bind("<Return>", lambda event: self._controller.gui_change_speed(entry.get()))
        entry.pack(side=RIGHT)

# ============================================================================
# VUE PRINCIPALE
# ============================================================================

class LiveView:
    """
    Vue principale du jeu de la vie
    gère la fenetre, le canvas et la barre de commandes
    """

    def __init__(self, controller):
        self._controller = controller

        # Creer la fenêtre principale
        self._window = Tk()
        self._window.title("Jeu de la vie - Conway's Game of life")
        self._window.resizable(False, False)

        # Récupérer les dimensions depuis le modèle
        model = controller.model
        canvas_width = model.canvas_width
        canvas_height = model.canvas_height
        cell_size = model.cell_size

        # Frame principal
        main_frame = Frame(self._window, bg='lightblue')
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Titre
        self._create_title(main_frame)

        # Canvas (grille)
        self._canvas = LiveCanvas(
            self._window,
            canvas_width,
            canvas_height,
            cell_size,
            controller
        )

        # Barre de commande
        self._command_bar = LiveCommandBar(self._window, controller)

        # Barre d'informations (génération + compteur)
        self._create_info_bar(main_frame)

        # Lier la vue au controleur
        controller.set_view(self)

    def _create_title(self, parent):
        """Creer le titre de l'application"""
        title_frame = Frame(parent, bg='darkblue', pady=10)
        title_frame.pack(fill=X, pady=(0, 10))

        title_label = Label(title_frame, text="JEU DE LA VIE - CONWAY'S GAME OF LIFE :", font=('Arial', 14, 'bold'), bg='darkblue', fg='white')
        title_label.pack()

    def _create_info_bar(self, parent):
        """Crée la barre d'informations (génération + compteur)"""
        info_frame = Frame(parent, bg='lightblue', pady=8)
        info_frame.pack(fill=X, pady=(5, 0))

        # Label génération
        self._generation_label = Label(info_frame, text='Génération: 0', font=('Arial', 11, 'bold'), bg='lightblue')
        self._generation_label.pack(side=LEFT, padx=20)

        # Label compteur de cellules vivantes
        self._counter_label = Label(info_frame, text="Cellules vivante: 0", font=('Arial', 11, 'bold'), bg='lightblue')
        self._counter_label.pack(side=LEFT, padx=20)

        # Instructions
        instructions = Label(info_frame, text='Clic gauche: activer • Clic droit: tuer', font=('Arial', 10, 'italic'), bg='lightblue', fg='darkblue')
        instructions.pack(side=RIGHT, padx=20)

    def mainloop(self):
        """Lance la boucle principale Tkinter"""
        self._window.mainloop()

    # Ajout méthode
    def get_window(self):
        """Retourne la fenêtre tkinter"""
        return self._window

    def update_display(self):
        """Met à jour l'affichage
        Redessine toutes les cellules"""
        # Redessiner le canvas
        self._canvas.redraw(self._controller.model)

        # Mettre a jour les infos
        generation = self._controller.model.generation
        alive_count = self._controller.model.count_alive_cells()

        self._generation_label.config(text=f"Génération: {generation}")
        self._counter_label.config(text=f"Cellules vivantes: {alive_count}")

        # force le rafraichissement de la fenêtre
        self._window.update()

    def schedule_next_iteration(self, delay: int, callback):
        """
        Programme la prochaine itération
        :param delay: délai en millisecondes
        :param callback: fonction à appeler (généralement controller.play)
        """
        self._window.after(delay, callback)

    def close(self):
        """Ferme la fenêtre"""
        self._window.destroy()