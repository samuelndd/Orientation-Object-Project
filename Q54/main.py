# main.py  # Point d'entrée UNIQUE de l'application (critère : main doit uniquement lancer l'application)

from __future__ import annotations  # Permet les annotations de type en avance (bonne pratique, même si pas obligatoire)

from livecontroller import LiveController  # Importe la classe Controller (orchestrateur MVC)


if __name__ == "__main__":  # Vérifie que ce fichier est exécuté directement (et pas importé)
    LiveController()  # Lance l'application : le Controller crée Model + View et démarre la boucle Tkinter
