# -*- coding: utf-8 -*-
"""Dissimulable +20 -> +10 et Harcèlement +20 -> +10. Les armes concernées gagnent
+10 dégâts pour rester à 100. Met à jour glossaire, barème et exemple Dague.
Usage : python scripts/patch_dissim_harcel.py"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
P = Path("docs/content/regles/combat/armes.md")
text = P.read_text(encoding="utf-8")


def rep(old, new):
    global text
    assert old in text, "NON TROUVÉ : " + old[:70]
    text = text.replace(old, new, 1)


# Glossaire
rep("#### Dissimulable (+20)", "#### Dissimulable (+10)")
rep("#### Harcèlement (+20)", "#### Harcèlement (+10)")

# Barème : retirer du +20, ajouter au +10
rep("· Dissimulable · Polyvalente", "· Polyvalente")
rep("· Incendiaire · Persistant · Harcèlement |", "· Incendiaire · Persistant |")
rep("| +10 | Légère ·", "| +10 | Légère · Dissimulable · Harcèlement ·")

# Exemple Dague (dégâts 20 -> 30, Dissimulable 20 -> 10)
rep("**Exemple, Dague (★☆☆☆☆, AM ✦✦✧)** : 20 (dégâts)",
    "**Exemple, Dague (★☆☆☆☆, AM ✦✦✧)** : 30 (dégâts)")
rep("+ 20 (Dissimulable) +", "+ 10 (Dissimulable) +")

# Lignes d'armes : +10 dégâts
DEG = {"Dague", "Arme articulée (nunchaku)", "Sarbacane", "Arbalète de poing",
       "Pistolet à poudre noire", "Pistolet semi-auto", "Derringer", "Derringer 4 canons",
       "Arme de poing renforcée", "Éventail de fer", "Hache de jet"}
out, n = [], 0
for l in text.splitlines():
    cells = l.split("|")[1:-1]
    if len(cells) == 9 and re.fullmatch(r"\s*[✦✧]{3}\s*", cells[1]):
        c = [x.strip() for x in cells]
        if c[0] in DEG:
            m = re.match(r"(\d+)(.*)", c[4])
            c[4] = str(int(m.group(1)) + 10) + m.group(2)
            l = "| " + " | ".join(c) + " |"
            n += 1
    out.append(l)
text = "\n".join(out) + "\n"

P.write_text(text, encoding="utf-8")
print(f"OK - Dissimulable/Harcèlement -> +10 ; {n} armes compensées (+10 dégâts)")
