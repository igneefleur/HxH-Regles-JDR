# -*- coding: utf-8 -*-
"""Unifie la prise sur la propriété « Saisie » (la portée se gère via Allonge) :
- Supprime « Saisie à distance » (glossaire + barème).
- Met à jour l'entrée « Saisie ».
- Ajoute Saisie aux armes souples : Fouet (dég 10->0), Kusarigama (40->30) ;
  Chaîne lestée passe de Saisie à distance à Saisie (dég 10->20).
Chaque arme reste à 100. Usage : python scripts/patch_saisie.py"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
P = Path("docs/content/livre/armes.md")
text = P.read_text(encoding="utf-8")


def rep(old, new):
    global text
    assert old in text, "NON TROUVÉ : " + old[:80]
    text = text.replace(old, new, 1)


# Glossaire : maj Saisie + suppression de Saisie à distance (entrées adjacentes)
rep(
    "#### Saisie (+10)\nL'arme peut **agripper** : elle donne accès, au contact, à la chaîne de manœuvres de prise (**Agripper**, puis **Maîtriser** et **Soumettre** ; voir Manœuvres). Sans *Saisie* ni *Saisie à distance*, une arme ne peut pas employer Agripper.\n\n#### Saisie à distance (+20)\nComme **Saisie**, mais le porteur emploie ces manœuvres de prise (Agripper, Maîtriser, Soumettre) **à la portée de l'arme** (chaîne, fouet lesté…), et non plus seulement au contact.",
    "#### Saisie (+10)\nL'arme peut **agripper** : elle donne accès à la chaîne de manœuvres de prise (**Agripper**, puis **Maîtriser** et **Soumettre** ; voir Manœuvres). La prise s'exerce à la portée habituelle de l'arme : une arme dotée d'**Allonge** agrippe d'autant plus loin. Sans *Saisie*, une arme ne peut pas employer Agripper.",
)

# Barème : retirer Saisie à distance du +20
rep("· Désarmement · Saisie à distance · Mains libres", "· Désarmement · Mains libres")

# Armes
rep("| Chaîne lestée | ✦✦✦ | Mêlée | 1 main | 10 | ×1 FOR | CON | ★★☆☆☆ | Allonge ×3, Désarmement, Saisie à distance |",
    "| Chaîne lestée | ✦✦✦ | Mêlée | 1 main | 20 | ×1 FOR | CON | ★★☆☆☆ | Allonge ×3, Désarmement, Saisie |")
rep("| Fouet | ✦✦✦ | Mêlée | 1 main | 10 | ×1 FOR | CON | ★☆☆☆☆ | Allonge ×3, Désarmement |",
    "| Fouet | ✦✦✦ | Mêlée | 1 main | 0 | ×1 FOR | CON | ★☆☆☆☆ | Allonge ×3, Désarmement, Saisie |")
rep("| Kusarigama | ✦✦✦ | Mêlée | 1 main | 40 | ×1 FOR | TRA / CON | ★★☆☆☆ | Allonge ×3 |",
    "| Kusarigama | ✦✦✦ | Mêlée | 1 main | 30 | ×1 FOR | TRA / CON | ★★☆☆☆ | Allonge ×3, Saisie |")

P.write_text(text, encoding="utf-8")
print("OK - Saisie unifiée ; Fouet/Kusarigama/Chaîne lestée dotées de Saisie")
