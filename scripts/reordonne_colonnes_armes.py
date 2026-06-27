# -*- coding: utf-8 -*-
"""Réordonne les colonnes des tableaux d'armes (les seuls à 6 colonnes) :
ancien  : Arme | Illégalité | AM | Dégâts | Portée | Propriétés
nouveau : Arme | AM | Portée | Dégâts | Illégalité | Propriétés
Mapping des indices : 0, 2, 4, 3, 1, 5. En-tête, séparateur et lignes inclus.
Usage : python scripts/reordonne_colonnes_armes.py"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
P = Path("docs/content/livre/armes.md")
lines = P.read_text(encoding="utf-8").splitlines()

ORDER = [0, 2, 4, 3, 1, 5]
n = 0
out = []
for l in lines:
    s = l.rstrip()
    if s.startswith("|") and s.endswith("|"):
        cells = s.split("|")[1:-1]          # cellules internes (espaces compris)
        if len(cells) == 6:
            cells = [cells[i] for i in ORDER]
            l = "|" + "|".join(cells) + "|"
            n += 1
    out.append(l)

P.write_text("\n".join(out) + "\n", encoding="utf-8")
print("OK -", n, "lignes de tableau réordonnées")
