# -*- coding: utf-8 -*-
"""Retraits nets du paquet final :
- « +1 attaque par action » supprimée (on ne garde que Légère) -> nunchaku +30 dégâts.
- « Entrave » supprimée (= Immobilisation à distance) -> le filet bascule dessus.
Chaque arme reste à 100. Usage : python scripts/patch_final_clean.py"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
P = Path("docs/content/livre/armes.md")
text = P.read_text(encoding="utf-8")


def rep(old, new):
    global text
    assert old in text, "NON TROUVÉ : " + old[:80]
    text = text.replace(old, new, 1)


# Glossaire
for name in ["+1 attaque par action", "Entrave"]:
    pat = r"#### " + re.escape(name) + r" \(\+\d+\)\n.*?\n\n"
    assert re.search(pat, text, re.S), "glossaire non trouvé : " + name
    text = re.sub(pat, "", text, count=1, flags=re.S)

# Barème
rep("· Tir rapide · +1 attaque/action · Allonge ×3", "· Tir rapide · Allonge ×3")
rep("· Renverse · Entrave · Immobilisation ·", "· Renverse · Immobilisation ·")

# Nunchaku : perd +1 attaque par action, garde Légère, +30 dégâts
rep("| Arme articulée (nunchaku) | ✦✦✦ | Mêlée | 1 main | 30 | ×1 FOR | CON | ★★☆☆☆ | +1 attaque par action, Dissimulable, Légère |",
    "| Arme articulée (nunchaku) | ✦✦✦ | Mêlée | 1 main | 60 | ×1 FOR | CON | ★★☆☆☆ | Dissimulable, Légère |")

# Filet : Entrave -> Immobilisation à distance (même +50)
rep("| Arme enchevêtrante | ✦✧✧ | Jet 10/20 m | 1 main | 30 |  | CON | ☆☆☆☆☆ | Entrave |",
    "| Arme enchevêtrante | ✦✧✧ | Jet 10/20 m | 1 main | 30 |  | CON | ☆☆☆☆☆ | Immobilisation à distance |")

P.write_text(text, encoding="utf-8")
print("OK - +1 attaque par action & Entrave retirées ; nunchaku 60 ; filet -> Immobilisation à distance")
