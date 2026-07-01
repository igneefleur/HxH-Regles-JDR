# -*- coding: utf-8 -*-
"""Page Armes : la compatibilité arts martiaux (AM, 0 à 3) s'affiche en symboles
✦ (plein) / ✧ (vide), comme l'illégalité en étoiles. Colonne des tableaux, table
de référence AM, puces de prose et ligne d'intro.
Usage : python scripts/patch_am_symboles.py"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
P = Path("docs/content/regles/combat/armes.md")
text = P.read_text(encoding="utf-8")


def am(n):
    return "✦" * n + "✧" * (3 - n)


# 1. Colonne AM des tableaux d'armes (3e cellule, après l'illégalité en étoiles).
text = re.sub(r"(?m)^(\| [^|]+ \| [★☆]{5} \| )([0-3])( \|)",
              lambda m: m.group(1) + am(int(m.group(2))) + m.group(3), text)

# 2. Table de référence AM : 1re colonne 0-3 -> symboles, en-tête « Note » -> « AM ».
text = re.sub(r"(?m)^\| ([0-3]) \| ",
              lambda m: "| " + am(int(m.group(1))) + " | ", text)
text = text.replace("| Note | Signification | Points |", "| AM | Signification | Points |")

# 3. Puces de prose « **AM N** ».
for n in range(4):
    text = text.replace(f"**AM {n}**", f"**{am(n)}**")

# 4. Ligne d'intro.
text = text.replace(
    "**AM** = compatibilité arts martiaux (0 à 3) ·",
    "**AM** = compatibilité arts martiaux (0 à 3), en symboles (✦ plein, ✧ vide) ·",
)

P.write_text(text, encoding="utf-8")
print("OK - AM en symboles ✦/✧")
