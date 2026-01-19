class LiveCounter:
    """
    Compteur de cellules vivantes
    Implémente le pattern Observer : observe les cellules
    """

    def __init__(self):
        self._alive_count = 0

    @property
    def alive_count(self):
        """Retourne le nombre de cellules vivantes"""
        return self._alive_count

    def update(self, cell):
        """
        Methode appelée quand une cellule change d'état
        (interface du pattern Observer)
        Note : Dans cette implémentation, on préfère recompter
        toutes les cellules plutôt que de tracker chaque changement
        individuellement pour éviter les incohérences
        """

    def count_all(self, model):
        """
        Compte toutes les cellules vivantes dans le modèle
        Méthode principale utilisée pour mettre à jour le compteur
        """
        count = 0
        for cell in model.get_all_cells():
            if cell.is_alive():
                count += 1
        self._alive_count = count

    def reset(self):
        """Remet le compteur à zéro"""
        self._alive_count = 0

    def __str__(self):
        return f"LiveCounter: {self._alive_count} cellules vivantes"