# -*- coding: utf-8 -*-
"""Retire 4 propriétés (Surprise, Maintient sans jet, Portée doublée, Volée),
nettoie le barème +20 (dont les orphelins Polyvalente/Mur de piques/Tir de suppression/
Multi-cibles, absents du glossaire) et rééquilibre les 5 armes concernées.
Chaque arme reste à 100. Usage : python scripts/patch_batch3_removals.py"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
P = Path("docs/content/regles/combat/armes.md")
text = P.read_text(encoding="utf-8")


def rep(old, new):
    global text
    assert old in text, "NON TROUVÉ : " + old[:80]
    text = text.replace(old, new, 1)


# --- Entrées de glossaire retirées ---
for name in ["Surprise", "Maintient sans jet", "Portée doublée", "Volée"]:
    pat = r"#### " + re.escape(name) + r" \(\+20\)\n.*?\n\n"
    assert re.search(pat, text, re.S), "glossaire non trouvé : " + name
    text = re.sub(pat, "", text, count=1, flags=re.S)

# --- Barème +20 reconstruit pour coller au glossaire ---
rep("| +20 | Finesse · Polyvalente · Allonge ×2 · Désarmement · Saisie à distance · Mains libres · Surprise · Maintient sans jet · Volée · Réduit au silence · Mur de piques · Tir de suppression · Portée doublée · Multi-cibles · Incendiaire · Persistant |",
    "| +20 | Finesse · Allonge ×2 · Désarmement · Saisie à distance · Mains libres · Réduit au silence · Incendiaire · Persistant |")

# --- Rééquilibrage des 5 armes ---
rep("| Arme enchevêtrante | ✦✧✧ | Jet 10/20 m | 1 main | 10 |  | CON | ☆☆☆☆☆ | Entrave, Maintient sans jet |",
    "| Arme enchevêtrante | ✦✧✧ | Jet 10/20 m | 1 main | 30 |  | CON | ☆☆☆☆☆ | Entrave |")
rep("| Javelot | ✦✧✧ | Jet 20/40 m · mêlée | 1 main | 40 | ×1 FOR | PER | ☆☆☆☆☆ | Portée doublée via propulseur (atlatl), Fragile |",
    "| Javelot | ✦✧✧ | Jet 40/80 m · mêlée | 1 main | 60 | ×1 FOR | PER | ☆☆☆☆☆ | Fragile |")
rep("| Projectile léger de jet | ✦✧✧ | Jet 10/20 m | 1 main | 70 | ×1 FOR | PER | ★★☆☆☆ | Volée (2 par attaque), Légère |",
    "| Projectile léger de jet | ✦✧✧ | Jet 10/20 m | 1 main | 70 | ×1 FOR | PER | ★★☆☆☆ | Finesse, Légère |")
rep("| Arbalète à répétition | ✧✧✧ | Tir 20/70 m | 2 mains | 70 |  | PER | ★☆☆☆☆ | Tir rapide, Volée (2 carreaux), Munitions (10 carreaux) |",
    "| Arbalète à répétition | ✧✧✧ | Tir 20/70 m | 2 mains | 90 |  | PER | ★☆☆☆☆ | Tir rapide, Munitions (10 carreaux) |")
rep("| Fusil à canon double | ✧✧✧ | Tir 10/30 m | 2 mains | 145 |  | PER | ★★☆☆☆ | Zone à bout portant, Volée (deux canons à la fois), Recul, Encombrante, Munitions (2 cartouches) |",
    "| Fusil à canon double | ✧✧✧ | Tir 10/30 m | 2 mains | 165 |  | PER | ★★☆☆☆ | Zone à bout portant, Recul, Encombrante, Munitions (2 cartouches) |")

P.write_text(text, encoding="utf-8")
print("OK - 4 propriétés retirées, barème +20 nettoyé, 5 armes rééquilibrées")
