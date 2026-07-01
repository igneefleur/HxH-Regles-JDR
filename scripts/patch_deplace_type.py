# -*- coding: utf-8 -*-
"""Déplace la colonne « Type » à droite de « Mod. dégâts » :
ancien  : Arme | AM | Portée | Mains | Dégâts | Type | Mod. dégâts | Illégalité | Propriétés
nouveau : Arme | AM | Portée | Mains | Dégâts | Mod. dégâts | Type | Illégalité | Propriétés
Permutation des cellules 5 et 6 (en-tête, séparateur et lignes). Aucun point ne change.
Usage : python scripts/patch_deplace_type.py"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
P = Path("docs/content/regles/combat/armes.md")
ORDER = [0, 1, 2, 3, 4, 6, 5, 7, 8]

out, n = [], 0
for l in P.read_text(encoding="utf-8").splitlines():
    s = l.rstrip()
    if s.startswith("|") and s.endswith("|"):
        cells = s.split("|")[1:-1]
        if len(cells) == 9:
            cells = [cells[i] for i in ORDER]
            l = "|" + "|".join(cells) + "|"
            n += 1
    out.append(l)

P.write_text("\n".join(out) + "\n", encoding="utf-8")
print("OK -", n, "lignes réordonnées (Type déplacé après Mod. dégâts)")
