# -*- coding: utf-8 -*-
"""Page Armes : illégalité affichée en 5 étoiles (pleines/vides) au lieu de « N★ »,
et en-tête de colonne « Illégalité » au lieu du symbole.
Usage : python scripts/patch_armes_etoiles.py"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
P = Path("docs/content/livre/armes.md")
text = P.read_text(encoding="utf-8")


def stars(n):
    return "★" * n + "☆" * (5 - n)


# 1. « N★ » -> 5 étoiles (cellules de tableau ET prose ; l'en-tête « ★ » seul n'a pas de chiffre).
text = re.sub(r"([0-5])★", lambda m: stars(int(m.group(1))), text)

# 2. En-tête des tableaux d'armes : « ★ » -> « Illégalité ».
text = text.replace("| Arme | ★ | AM | Dégâts | Portée | Propriétés |",
                    "| Arme | Illégalité | AM | Dégâts | Portée | Propriétés |")

# 3. En-tête de la table d'illégalité : « Note » -> « Illégalité ».
text = text.replace("| Note | Statut | Points |", "| Illégalité | Statut | Points |")

# 4. Ligne d'intro décrivant les colonnes.
text = re.sub(
    r"Colonnes des tableaux : \*\*★\*\* = illégalité \(0 à 5\)[^\n]*",
    "Colonnes des tableaux : **Illégalité** = note de 0 à 5 affichée en étoiles "
    "(★ pleine, ☆ vide) · **AM** = compatibilité arts martiaux (0 à 3) · "
    "**Portée** = distance(s) d'engagement.",
    text,
)

P.write_text(text, encoding="utf-8")
print("OK - étoiles + en-têtes appliqués")
