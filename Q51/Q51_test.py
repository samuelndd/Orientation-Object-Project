from Q51_calc_313 import Calculator
# from Q51_calc_312 import Calculator
# pytest est un framework de test en Python,
# - pytest cherche automatiquement les fichiers et fonctions de test
#   en fonction de certaines conventions
# - utilisation de assert
import pytest



@pytest.fixture
def calc():
    """
    Les fixtures permettent de factoriser du code
    (ici: initialisation de l'objet calc ) et
    de le réutiliser entre les tests.
    """
    return Calculator("POOC")  # Instanciation de l'objet



def test_somme(calc):
    """
    Convention simple mais stricte :
    - Les fonctions de test doivent commencer par test_ (en minuscules).
    - Le nom doit décrire ce qui est testé et le comportement attendu.
    """
    assert calc.plus(3, 4) == 7     # Réussi car 3 + 4 == 7
    assert calc.plus(2, 1) == 3     # Réussi car 2 + 1 == 3
    assert calc.plus(30, 40) == 70  # Echoue à cause d'un bug
    assert calc.plus(-5, 8) == 3  # négatif + positif
    assert calc.plus(11, -2) == 9  # >10 + négatif



def test_produit(calc):
    assert calc.fois(2, 5) == 10    # Réussi car 2 * 5 == 10
    assert calc.fois(10, 5) == 50   # Echoue a cause d'un bug
    assert calc.fois(12, 11) == 132  # >10 * >10
    assert calc.fois(-4, 6) == -24  # négatif * positif
    assert calc.fois(-7, -3) == 21


    
def test_difference(calc):
    assert calc.moins(6, 3) == 3
    assert calc.moins(10, 5) == 5
    assert calc.moins(15, 20) == -5        # résultat négatif
    assert calc.moins(-4, 6) == -10        # négatif - positif
    assert calc.moins(100, 11) == 89       # >10 - >10