"""
main.py
Conforme consigne :
- uniquement lancer le Controller
"""

from __future__ import annotations
from livecontroller import LiveController


def main() -> None:
    print("=" * 60)
    print("JEU DE LA VIE - Q54 (MVC + Patterns)")
    print("=" * 60)
    LiveController(rows=40, cols=40, cell_px=10)


if __name__ == "__main__":
    main()
