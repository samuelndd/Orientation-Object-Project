import unittest
from livemodel import LiveModel, LiveCell, RandomStrategy, CanonStrategy, EmptyStrategy
from livecounter import LiveCounter


class TestSingleton(unittest.TestCase):
    """Test du Pattern Singleton"""

    def test_singleton_same_instance(self):
        """Vérifie qu'on a toujours la même instance"""
        model1 = LiveModel.get_instance()
        model2 = LiveModel.get_instance()
        self.assertIs(model1, model2, "Les deux instances doivent être identiques")

    def test_singleton_name_id(self):
        """Vérifie que les IDs mémoire sont identiques"""
        model1 = LiveModel.get_instance()
        model2 = LiveModel.get_instance()
        self.assertEqual(id(model1), id(model2), "Les IDs mémoire doivent être identiques")


class TestLiveCell(unittest.TestCase):
    """Test de la classe LiveCell"""
    def test_cell_creation(self):
        """Test création cellule"""
        cell = LiveCell(5, 10)
        self.assertEqual(cell.x, 5, "Coordonnée x incorrecte")
        self.assertEqual(cell.y, 10, "Coordonnée y incorrecte")
        self.assertFalse(cell.is_alive(), "Une nouvelle cellule doit être morte")

    def test_cell_initial_state(self):
        """Test état initial d'une cellule"""
        cell = LiveCell(0, 0)
        self.assertFalse(cell.is_alive(), "Etat initial doit être mort")
        self.assertEqual(cell.nb_neighbours, 0, "Nombre initial de voisins doit être 0")

    def test_cell_set_alive(self):
        """Test activation cellule"""
        cell = LiveCell(0, 0)
        cell.set_alive(True)
        self.assertTrue(cell.is_alive(), "La cellule devrait être vivante")

    def test_cell_set_dead(self):
        """Test désactivation cellule"""
        cell = LiveCell(0, 0)
        cell.set_alive(True)
        cell.set_alive(False)
        self.assertFalse(cell.is_alive(), "La cellule devrait être morte")

    def test_cell_toggle(self):
        """Test basculement état cellule"""
        cell = LiveCell(0, 0)
        initial_state = cell.is_alive()
        cell.toggle()
        self.assertNotEqual(cell.is_alive(), initial_state, "L'état devrait avoir basculé")

    def test_cell_neighbours(self):
        """Test comptage Voisins"""
        cell = LiveCell(0, 0)
        cell.set_nb_neighbours(3)
        self.assertEqual(cell.nb_neighbours, 3, "Nombre de voisins incorrect")

    def test_cell_neighbours_range(self):
        """Test valeurs limites voisins (0-8)"""
        cell = LiveCell(0, 0)
        for nb in range(9):  # 0 à 8 voisins possibles
            cell.set_nb_neighbours(nb)
            self.assertEqual(cell.nb_neighbours, nb, f"Devrait avoir {nb} voisins")


class TestObserver(unittest.TestCase):
    """Test du pattern Observer"""

    def test_attach_observer(self):
        """Test attachement d'un observateur"""
        cell = LiveCell(0, 0)
        counter = LiveCounter()

        # Test que l'attachement fonctionne sans erreur
        try:
            cell.attach_observer(counter)
            self.assertTrue(True, "L'attachement de l'observer a réussi")
        except Exception as e:
            self.fail(f"L'attachement de l'observer a échoué: {e}")

    def test_observer_notification_on_change(self):
        """Test que l'observer est notifié lors d'un changement"""
        model = LiveModel.get_instance()
        model.reset_all_cells()

        # Utiliser le compteur du modèle
        initial_count = model.count_alive_cells()

        # Activer une cellule
        cell = model.get_cell(25, 25)
        cell.set_alive(True)

        # Vérifier que le compteur a été mis à jour
        new_count = model.count_alive_cells()
        self.assertEqual(new_count, initial_count + 1,
                         "Le compteur devrait augmenter quand une cellule naît")

    def test_observer_multiple_changes(self):
        """Test observer avec plusieurs changements"""
        model = LiveModel.get_instance()
        model.reset_all_cells()

        # Activer plusieurs cellules
        model.get_cell(10, 10).set_alive(True)
        model.get_cell(10, 11).set_alive(True)
        model.get_cell(10, 12).set_alive(True)

        # Vérifier le comptage
        self.assertEqual(model.count_alive_cells(), 3,
                         "Le compteur devrait compter 3 cellules vivantes")

        # Désactiver une cellule
        model.get_cell(10, 11).set_alive(False)

        # Vérifier le nouveau comptage
        self.assertEqual(model.count_alive_cells(), 2,
                         "Le compteur devrait compter 2 cellules vivantes après désactivation")


class TestConwayRules(unittest.TestCase):
    """Test des règles de Conway"""

    def setUp(self):
        """Initialise un modèle pour chaque test"""
        self.model = LiveModel.get_instance()
        self.model.reset_all_cells()

    def test_birth_rule(self):
        """Une cellule morte avec 3 voisins naît"""
        model = LiveModel.get_instance()
        # config : cellule morte avec 3 voisins
        # verifier qu'elle devient vivante
        # Vider la grille
        self.model.reset_all_cells()

        # Créer une configuration où la cellule centrale (25,25) a exactement 3 voisins
        self.model.get_cell(24, 25).set_alive(True)  # Haut
        self.model.get_cell(25, 24).set_alive(True)  # Gauche
        self.model.get_cell(25, 26).set_alive(True)  # Droite

        # La cellule centrale doit être morte
        center_cell = self.model.get_cell(25, 25)
        self.assertFalse(center_cell.is_alive(), "La cellule centrale doit être morte au départ")

        # Exécuter une génération
        self.model.next_generation()

        # La cellule centrale devrait maintenant être vivante
        self.assertTrue(center_cell.is_alive(),
                        "Une cellule morte avec 3 voisins devrait naître")

    def test_survival_rule_2_neighbours(self):

        self.model.reset_all_cells()

        # Creer une cellule vivante avec 2 voisins
        self.model.get_cell(25, 25).set_alive(True)  # Cellule testée
        self.model.get_cell(25, 26).set_alive(True)  # Voisin 1
        self.model.get_cell(26, 25).set_alive(True)  # Voisin 2

        cell = self.model.get_cell(25, 25)
        self.assertTrue(cell.is_alive(), "La cellule doit être vivante au départ")

        # Exécuter une génération
        self.model.next_generation()

        # La cellule devrait rester vivante
        self.assertTrue(cell.is_alive(),
                        "Une cellule vivante avec 2 voisins devrait survivre")

    def test_survival_rule_3_neighbours(self):
        """
        Règle de survie : Une cellule vivante avec 3 voisins reste vivante
        """
        self.model.reset_all_cells()

        # Créer une cellule vivante avec 3 voisins
        self.model.get_cell(25, 25).set_alive(True)  # Cellule testée
        self.model.get_cell(24, 25).set_alive(True)  # Voisin 1
        self.model.get_cell(25, 24).set_alive(True)  # Voisin 2
        self.model.get_cell(25, 26).set_alive(True)  # Voisin 3

        cell = self.model.get_cell(25, 25)

        # Exécuter une génération
        self.model.next_generation()

        # La cellule devrait rester vivante
        self.assertTrue(cell.is_alive(),
                        "Une cellule vivante avec 3 voisins devrait survivre")

    def test_death_by_underpopulation(self):
        """
        Règle de mort par solitude : Une cellule vivante avec 0-1 voisin meurt
        """
        self.model.reset_all_cells()

        # Cellule isolée (0 voisins)
        self.model.get_cell(25, 25).set_alive(True)
        cell = self.model.get_cell(25, 25)

        self.assertTrue(cell.is_alive(), "La cellule doit être vivante au départ")

        # Exécuter une génération
        self.model.next_generation()

        # La cellule devrait mourir
        self.assertFalse(cell.is_alive(),
                         "Une cellule isolée (0 voisin) devrait mourir")

    def test_death_by_underpopulation_1_neighbour(self):
        """
        Règle de mort par solitude : Une cellule vivante avec 1 voisin meurt
        """
        self.model.reset_all_cells()

        # Cellule avec 1 voisin
        self.model.get_cell(25, 25).set_alive(True)
        self.model.get_cell(25, 26).set_alive(True)  # 1 voisin
        cell = self.model.get_cell(25, 25)

        # Exécuter une génération
        self.model.next_generation()

        # La cellule devrait mourir
        self.assertFalse(cell.is_alive(),
                         "Une cellule avec 1 voisin devrait mourir")

    def test_death_by_overpopulation(self):
        """
        Règle de mort par surpopulation : Une cellule vivante avec 4+ voisins meurt
        Configuration :
          ■ ■ ■
          ■ ■ □  (cellule centrale avec 4 voisins)
          □ □ □
        """
        self.model.reset_all_cells()

        # Créer une cellule avec 4 voisins
        self.model.get_cell(25, 25).set_alive(True)  # Cellule testée
        self.model.get_cell(24, 24).set_alive(True)  # Voisin 1
        self.model.get_cell(24, 25).set_alive(True)  # Voisin 2
        self.model.get_cell(24, 26).set_alive(True)  # Voisin 3
        self.model.get_cell(25, 24).set_alive(True)  # Voisin 4

        cell = self.model.get_cell(25, 25)

        # Exécuter une génération
        self.model.next_generation()

        # La cellule devrait mourir
        self.assertFalse(cell.is_alive(),
                         "Une cellule avec 4+ voisins devrait mourir")

    def test_stable_block_pattern(self):
        """
        Test pattern stable : Bloc 2x2
        ■ ■
        ■ ■
        Ce pattern ne doit pas changer
        """
        self.model.reset_all_cells()

        # Créer un bloc 2x2
        cells = [
            self.model.get_cell(25, 25),
            self.model.get_cell(25, 26),
            self.model.get_cell(26, 25),
            self.model.get_cell(26, 26)
        ]

        for cell in cells:
            cell.set_alive(True)

        # Mémoriser l'état initial
        initial_states = [cell.is_alive() for cell in cells]

        # Exécuter une génération
        self.model.next_generation()

        # Vérifier que toutes les cellules sont toujours vivantes
        final_states = [cell.is_alive() for cell in cells]
        self.assertEqual(initial_states, final_states,
                         "Le bloc 2x2 devrait rester stable")

    def test_blinker_oscillation(self):

        self.model.reset_all_cells()
        # Créer un blinker vertical
        self.model.get_cell(24, 25).set_alive(True)
        self.model.get_cell(25, 25).set_alive(True)
        self.model.get_cell(26, 25).set_alive(True)

        # Après 1 génération, devrait être horizontal
        self.model.next_generation()

        self.assertTrue(self.model.get_cell(25, 24).is_alive(), "Devrait être horizontal")
        self.assertTrue(self.model.get_cell(25, 25).is_alive(), "Centre reste vivant")
        self.assertTrue(self.model.get_cell(25, 26).is_alive(), "Devrait être horizontal")

        # Après 2 générations, devrait redevenir vertical
        self.model.next_generation()

        self.assertTrue(self.model.get_cell(24, 25).is_alive(), "Retour vertical")
        self.assertTrue(self.model.get_cell(25, 25).is_alive(), "Centre reste vivant")
        self.assertTrue(self.model.get_cell(26, 25).is_alive(), "Retour vertical")


class TestStrategy(unittest.TestCase):
    """Test du pattern Strategy"""

    def setUp(self):
        """Initialise un modèle pour chaque test"""
        self.model = LiveModel.get_instance()

    def test_random_strategy_percentage(self):
        """Test configuration aléatoire"""
        strategy = RandomStrategy(25)
        strategy.apply(self.model)

        # compter cellules vivantes
        alive = self.model.count_alive_cells()
        total = self.model.matrix_width * self.model.matrix_height
        expected = int(total * 0.25)

        # verifier que c'est dans l'intervalle acceptable
        min_expected = int(expected * 0.95)
        max_expected = int(expected * 1.05)

        self.assertGreaterEqual(alive, min_expected,
                                f"Trop peu de cellules vivantes: {alive} < {min_expected}")
        self.assertLessEqual(alive, max_expected,
                             f"Trop de cellules vivantes: {alive} > {max_expected}")

    def test_random_strategy_different_percentage(self):
        """Test configuration aléatoire avec différents pourcentages"""
        for percentage in [10, 25, 50]:
            strategy = RandomStrategy(percentage)
            strategy.apply(self.model)

            alive = self.model.count_alive_cells()
            total = self.model.matrix_width * self.model.matrix_height
            expected = int(total * percentage / 100)

            # Tolérance ±10% pour les petits échantillons
            tolerance = max(int(expected * 0.1), 50)

            self.assertAlmostEqual(alive, expected, delta=tolerance,
                                   msg=f"Pourcentage {percentage}% incorrect")

    def test_canon_strategy(self):
        """Test configuration canon à planeurs"""
        strategy = CanonStrategy()
        strategy.apply(self.model)

        # Le canon devrait avoir environ 36 cellules
        alive = self.model.count_alive_cells()
        self.assertGreater(alive, 0, "Le canon devrait avoir des cellules vivantes")
        self.assertLess(alive, 100, "Le canon ne devrait pas avoir trop de cellules")

    def test_empty_strategy(self):
        """Test configuration vide"""
        # D'abord, remplir avec des cellules
        random_strategy = RandomStrategy(50)
        random_strategy.apply(self.model)
        self.assertGreater(self.model.count_alive_cells(), 0,
                           "Devrait avoir des cellules vivantes")

        # Puis vider
        empty_strategy = EmptyStrategy()
        empty_strategy.apply(self.model)

        self.assertEqual(self.model.count_alive_cells(), 0,
                         "La grille devrait être vide")

    def test_strategy_interchangeable(self):
        """Test que les stratégies sont interchangeables"""
        strategies = [
            RandomStrategy(25),
            CanonStrategy(),
            EmptyStrategy()
        ]

        # Toutes les stratégies devraient fonctionner sans erreur
        for strategy in strategies:
            try:
                self.model.set_strategy(strategy)
                self.model.apply_strategy()
            except Exception as e:
                self.fail(f"La stratégie {strategy.__class__.__name__} a échoué: {e}")

    class TestModel(unittest.TestCase):
        """Test du modèle général"""

        def setUp(self):
            """Initialise un modèle pour chaque test"""
            self.model = LiveModel.get_instance()

        def test_model_dimensions(self):
            """Test des dimensions du modèle"""
            self.assertEqual(self.model.matrix_width, 50, "Largeur devrait être 50")
            self.assertEqual(self.model.matrix_height, 50, "Hauteur devrait être 50")

        def test_model_initial_generation(self):
            """Test génération initiale"""
            self.model.reset_all_cells()
            self.assertEqual(self.model.generation, 0, "Génération initiale devrait être 0")

        def test_model_generation_increment(self):
            """Test incrémentation de la génération"""
            self.model.reset_all_cells()
            initial_gen = self.model.generation

            self.model.next_generation()

            self.assertEqual(self.model.generation, initial_gen + 1,
                             "La génération devrait s'incrémenter")

        def test_model_count_alive_cells(self):
            """Test comptage des cellules vivantes"""
            self.model.reset_all_cells()
            self.assertEqual(self.model.count_alive_cells(), 0,
                             "Grille vide devrait avoir 0 cellules vivantes")

            # Ajouter quelques cellules
            self.model.get_cell(0, 0).set_alive(True)
            self.model.get_cell(1, 1).set_alive(True)
            self.model.get_cell(2, 2).set_alive(True)

            self.assertEqual(self.model.count_alive_cells(), 3,
                             "Devrait compter 3 cellules vivantes")

        def test_model_reset(self):
            """Test remise à zéro"""
            # Remplir avec des cellules
            RandomStrategy(50).apply(self.model)
            self.assertGreater(self.model.count_alive_cells(), 0)

            # Reset
            self.model.reset_all_cells()

            self.assertEqual(self.model.count_alive_cells(), 0,
                             "Toutes les cellules devraient être mortes après reset")

        def test_model_get_cell(self):
            """Test récupération d'une cellule"""
            cell = self.model.get_cell(10, 20)
            self.assertIsNotNone(cell, "La cellule ne devrait pas être None")
            self.assertEqual(cell.x, 10, "Coordonnée x incorrecte")
            self.assertEqual(cell.y, 20, "Coordonnée y incorrecte")

        def test_model_wrap_around(self):
            """Test que la grille s'enroule (tore)"""
            # Les bords devraient se connecter
            # Test à implémenter selon l'implémentation exacte du modèle
            cell_top = self.model.get_cell(0, 25)
            cell_bottom = self.model.get_cell(49, 25)

            # Ces cellules devraient être voisines (tore)
            self.assertIsNotNone(cell_top)
            self.assertIsNotNone(cell_bottom)

    # Point d'entrée pour exécuter les tests
if __name__ == '__main__':
    # Configuration du runner de tests
    unittest.main()