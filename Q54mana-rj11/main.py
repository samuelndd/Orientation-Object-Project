"""
Module main.py
Point d'entrée de l'application Jeu de la Vie

Architecture MVC avec Design Patterns:
- Singleton (LiveModel)
- Observer (LiveCounter)
- Strategy (Configurations)
- Iterator (Parcours de grille)
"""

from livecontroller import LiveController
from liveview import LiveView


def main():
    """
    Fonction principale pour lancer le Jeu de la Vie
    """
    print("=" * 60)
    print("🎮 JEU DE LA VIE - CONWAY'S GAME OF LIFE 🎮")
    print("=" * 60)
    print("\nArchitecture : MVC")
    print("Design Patterns : Singleton, Observer, Strategy, Iterator")
    print("=" * 60)
    print("\nDémarrage de l'application...")
    print("\nCommandes :")
    print("  • Go/Stop : Démarrer/Arrêter la simulation")
    print("  • Reset : Réinitialiser la grille")
    print("  • Step : Avancer d'une génération")
    print("  • Canon : Placer un canon à planeurs")
    print("  • Aléa : Configuration aléatoire (25%)")
    print("  • Vider : Effacer toute la grille")
    print("  • Clic gauche : Activer/désactiver une cellule")
    print("  • Clic droit : Tuer une cellule")
    print("=" * 60)
    print()

    # Créer le contrôleur
    controller = LiveController(
        canvas_width=500,   # Largeur en pixels
        canvas_height=500,  # Hauteur en pixels
        cell_size=10        # Taille d'une cellule en pixels
    )

    # Créer la vue
    view = LiveView(controller)

    # Lancer la boucle principale
    view.mainloop()

    print("\n✓ Application fermée. Au revoir !")


if __name__ == "__main__":
    main()