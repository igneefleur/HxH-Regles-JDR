# -*- coding: utf-8 -*-
"""Normalise la colonne « Mod. dégâts » des tableaux d'armes :
- multiplicateur ×0 -> cellule vide (rien) ;
- toujours en FOR (la propriété Finesse autorise à substituer la DEX au moment de l'attaque,
  mais l'affichage reste ×N FOR).
Idempotent. Usage : python scripts/patch_modcell.py"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
P = Path("docs/content/livre/armes.md")

out, n = [], 0
for l in P.read_text(encoding="utf-8").splitlines():
    if l.startswith("|") and l.rstrip().endswith("|"):
        cells = l.split("|")[1:-1]
        if len(cells) == 7 and re.fullmatch(r"\s*[✦✧]{3}\s*", cells[1]):
            mod = cells[4].strip()
            if mod == "×0":
                cells[4] = "  "
                n += 1
            elif "DEX" in mod:
                cells[4] = cells[4].replace("DEX", "FOR")
                n += 1
            l = "|" + "|".join(cells) + "|"
    out.append(l)

P.write_text("\n".join(out) + "\n", encoding="utf-8")
print("OK -", n, "cellules Mod. normalisées (×0 vidées, DEX -> FOR)")
