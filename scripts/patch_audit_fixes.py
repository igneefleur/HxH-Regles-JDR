# -*- coding: utf-8 -*-
"""Corrections issues de l'audit (cohérence, équilibrage, glossaire) :
- Suppr. Vecteur de poison (Sarbacane -> Étourdissement) et Double mode (Kusarigama +10 dég).
- Renversement +10 -> +20 (Masse lourde, Hallebarde -10 dég).
- Perce-blindage +30 -> +40 (Masse d'armes -10 dég, Fusil anti-matériel +Maintenance, Lance-roquettes -10 dég).
- Perce-armure -> ignore la moitié de la TA ; Perce-blindage -> ignore toute la TA.
- Immobilisation à distance -> applique l'état Immobilisé (jet opposé chiffré).
- Choc/Étourdissement -> jet opposé d'Endurance contre le total d'attaque.
- Assommement -> 'sonnée' (plus de collision avec l'état Étourdi).
- Étranglement -> renvoie aux états Mutisme/Inconscience.
- Derringers : létalité ramenée sous les pistolets de service.
- Glossaire/barème : Zone à bout portant ajoutée ; variantes Inefficace ajoutées ; barème resynchronisé.
Chaque arme reste à 100. Usage : python scripts/patch_audit_fixes.py"""
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


# ---------- Glossaire : suppressions ----------
for pat in [r"#### Double mode \(\+10\)\n.*?\n\n", r"#### Vecteur de poison \(\+50\)\n.*?\n\n"]:
    assert re.search(pat, text, re.S), "glossaire non trouvé : " + pat
    text = re.sub(pat, "", text, count=1, flags=re.S)

# ---------- Glossaire : reformulations ----------
rep("#### Renversement (+10)", "#### Renversement (+20)")
rep("**Dès que l'attaque touche**, la cible est étourdie et **perd 1 action active** à son prochain tour (minimum 0).",
    "**Dès que l'attaque touche**, la cible est **sonnée** et **perd 1 action active** à son prochain tour (minimum 0). Effet distinct de l'état Étourdi.")
rep("#### Perce-armure (+30)\nL'attaque **ignore la TA des armures souples** (tissu, cuir, kevlar, rembourrage) : contre une cible en armure souple, on calcule les dégâts comme si elle n'en portait pas. Sans effet sur une armure rigide/lourde.",
    "#### Perce-armure (+30)\nL'attaque **ignore la moitié de la TA** de la cible (arrondi à la dizaine inférieure) : conçue pour mordre dans les protections, elle réduit de moitié leur valeur d'armure, quel qu'en soit le type.")
rep("#### Perce-blindage (+30)\nL'attaque **ignore la TA des armures lourdes** (plaque, blindage rigide, véhicules, structures) et, étant la version supérieure, aussi des souples. Défonce ce qui arrête tout le reste.",
    "#### Perce-blindage (+40)\nL'attaque **ignore toute la TA** de la cible : on calcule les dégâts comme si elle ne portait aucune armure. Version supérieure de Perce-armure, elle défonce jusqu'aux blindages, véhicules et structures.")
rep("#### Immobilisation à distance (+50)\nSur une touche, la cible est **clouée sur place** à distance : elle ne peut plus se déplacer tant que la prise tient. Elle se libère en consacrant une action (jet opposé).",
    "#### Immobilisation à distance (+50)\nSur une touche, la cible subit l'état **Immobilisé** (voir États) à distance : elle ne peut plus bouger, subit −20 à l'attaque et à l'esquive, et les attaques contre elle gagnent +20. Elle se libère en consacrant une action (jet opposé de Force ou Agilité contre la Dextérité du porteur).")
rep("Sur une touche, la cible tente un **jet opposé** (sa caractéristique la plus pertinente contre celle de l'attaquant). En cas d'échec, elle est mise **À terre** et **Étourdie** (voir États), incapable d'agir à son prochain tour. Munitions à létalité réduite, tirs de choc.",
    "Sur une touche, la cible oppose son **Endurance** au total d'attaque (jet opposé). En cas d'échec, elle est mise **À terre** et **Étourdie** (voir États), incapable d'agir à son prochain tour. Munitions à létalité réduite, tirs de choc.")
rep("#### Étourdissement (jet opposé) (+50)\nSur une touche, la cible tente un **jet opposé**. En cas d'échec, elle est **Étourdie** (voir États) : elle perd ses actions et ne peut pas réagir pendant un tour. Décharge électrique, gaz incapacitant.",
    "#### Étourdissement (jet opposé) (+50)\nSur une touche, la cible oppose son **Endurance** au total d'attaque (jet opposé). En cas d'échec, elle est **Étourdie** (voir États) : elle perd ses actions et ne peut pas réagir pendant un tour. Décharge électrique, gaz incapacitant.")
rep("#### Étranglement (+50)\nMaintenue en prise, l'arme comprime la gorge : tant que la prise tient, la cible **subit les dégâts à chaque tour**, ne peut plus parler ni crier, et finit par sombrer dans l'inconscience.",
    "#### Étranglement (+50)\nMaintenue en prise, l'arme comprime la gorge : tant que la prise tient, la cible **subit les dégâts à chaque tour**, subit l'état **Mutisme** (voir États), et finit par sombrer dans l'**Inconscience** (voir États).")

# ---------- Glossaire : ajout Zone à bout portant ----------
rep("On vise un point ou une direction, non une cible unique.\n\n#### Tir soutenu (+40)",
    "On vise un point ou une direction, non une cible unique.\n\n#### Zone à bout portant (+40)\nVariante de **Zone** limitée à la **portée courte** de l'arme : le tir s'évase et touche toutes les cibles d'un petit cône à bout portant (fusils à dispersion). Sans effet au-delà de la portée courte.\n\n#### Tir soutenu (+40)")

# ---------- Barème ----------
rep("| +10 | Légère · Dissimulable · Harcèlement · Indésarmable · Retour · Dégainage instantané · Double mode · Contourne un abri · Assommement · Renversement · Poussée · Ralentissement · Fauchage · Éraflure · Aggravation |",
    "| +10 | Légère · Dissimulable · Harcèlement · Indésarmable · Retour · Dégainage instantané · Contourne un abri · Assommement · Poussée · Ralentissement · Fauchage · Éraflure · Aggravation |")
rep("| +20 | Finesse · Allonge ×2 · Désarmement · Saisie à distance · Mains libres · Réduit au silence · Incendiaire · Persistant |",
    "| +20 | Finesse · Renversement · Allonge ×2 · Désarmement · Saisie à distance · Mains libres · Réduit au silence · Incendiaire · Persistant |")
rep("| +30 | Perce-armure · Perce-blindage · Tir en rafale · Allonge ×3 |",
    "| +30 | Perce-armure · Tir en rafale · Allonge ×3 |")
rep("| +40 | Zone · Tir soutenu · Allonge ×4 |",
    "| +40 | Zone · Zone à bout portant · Perce-blindage · Tir soutenu · Allonge ×4 |")
rep("| +50 | Vecteur de poison · Choc · Immobilisation à distance · Étourdissement · Étranglement |",
    "| +50 | Choc · Immobilisation à distance · Étourdissement · Étranglement |")
rep("· Inefficace à courte/longue portée · Inefficace en espace confiné",
    "· Inefficace à courte/longue portée · Inefficace à courte portée · Inefficace au-delà de courte portée · Inefficace en espace confiné")

# ---------- Exemple Fusil anti-matériel (corrige les 2 mains + Perce-blindage +40) ----------
rep("240 + 50 (tir très longue) + 30 (Perce-blindage) + 0 (×0) − 100 (Affût 40, Encombrement extrême 30, Préparation 20, Maintenance 10) − 20 (Munitions, 10 balles) − 100 (★★★★★) = **100**",
    "240 + 50 (tir très longue) − 10 (2 mains) + 40 (Perce-blindage) − 100 (Affût 40, Encombrement extrême 30, Préparation 20, Maintenance 10) − 20 (Munitions, 10 balles) − 100 (★★★★★) = **100**")

# ---------- Armes ----------
rep("| Masse d'armes | ✦✧✧ | Mêlée | 1 main | 30 | ×2 FOR | CON | ★☆☆☆☆ | Perce-blindage (défonce l'armure lourde) |",
    "| Masse d'armes | ✦✧✧ | Mêlée | 1 main | 20 | ×2 FOR | CON | ★☆☆☆☆ | Perce-blindage |")
rep("| Masse lourde | ✦✧✧ | Mêlée | 2 mains | 60 | ×3 FOR | CON | ★☆☆☆☆ | Renversement, Encombrante |",
    "| Masse lourde | ✦✧✧ | Mêlée | 2 mains | 50 | ×3 FOR | CON | ★☆☆☆☆ | Renversement, Encombrante |")
rep("| Kusarigama | ✦✦✦ | Mêlée | 1 main | 30 | ×1 FOR | TRA / CON | ★★☆☆☆ | Allonge ×3, Double mode (faux / chaîne contrôle) |",
    "| Kusarigama | ✦✦✦ | Mêlée | 1 main | 40 | ×1 FOR | TRA / CON | ★★☆☆☆ | Allonge ×3 |")
rep("| Hallebarde | ✦✦✧ | Mêlée | 2 mains | 60 | ×2 FOR | TRA / PER | ★☆☆☆☆ | Renversement, Inutilisable au contact |",
    "| Hallebarde | ✦✦✧ | Mêlée | 2 mains | 50 | ×2 FOR | TRA / PER | ★☆☆☆☆ | Renversement, Inutilisable au contact |")
rep("| Sarbacane | ✦✧✧ | Tir 10/20 m | 1 main | 20 |  | PER | ★☆☆☆☆ | Vecteur de poison, Dissimulable, Légère |",
    "| Sarbacane | ✦✧✧ | Tir 10/20 m | 1 main | 20 |  | PER | ★☆☆☆☆ | Étourdissement (jet opposé), Dissimulable, Légère |")
rep("| Derringer | ✧✧✧ | Tir 10/20 m | 1 main | 165 |  | PER | ★★★☆☆ | Dissimulable, Munitions (2 balles) |",
    "| Derringer | ✧✧✧ | Tir 10/20 m | 1 main | 125 |  | PER | ★☆☆☆☆ | Dissimulable, Munitions (2 balles) |")
rep("| Derringer 4 canons | ✧✧✧ | Tir 10/20 m | 1 main | 160 |  | PER | ★★★☆☆ | Dissimulable, Munitions (4 balles) |",
    "| Derringer 4 canons | ✧✧✧ | Tir 10/20 m | 1 main | 120 |  | PER | ★☆☆☆☆ | Dissimulable, Munitions (4 balles) |")
rep("| Fusil anti-matériel | ✧✧✧ | Tir 90/360 m | 2 mains | 240 |  | PER | ★★★★★ | Perce-blindage, Affût requis (bipied), Encombrement extrême, Préparation, Munitions (10 balles) |",
    "| Fusil anti-matériel | ✧✧✧ | Tir 90/360 m | 2 mains | 240 |  | PER | ★★★★★ | Perce-blindage, Affût requis (bipied), Encombrement extrême, Préparation, Maintenance requise, Munitions (10 balles) |")
rep("| Lance-roquettes | ✧✧✧ | Tir 40 m (direct) | 2 mains | 230 |  | CON / PER | ★★★★★ | Zone (rayon 10 m), Perce-blindage, Souffle arrière, Très bruyante, Encombrement extrême, Munitions (1 roquette) |",
    "| Lance-roquettes | ✧✧✧ | Tir 40 m (direct) | 2 mains | 220 |  | CON / PER | ★★★★★ | Zone (rayon 10 m), Perce-blindage, Souffle arrière, Très bruyante, Encombrement extrême, Munitions (1 roquette) |")

P.write_text(text, encoding="utf-8")
print("OK - corrections d'audit appliquées à armes.md")
