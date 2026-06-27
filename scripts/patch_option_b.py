# -*- coding: utf-8 -*-
"""Option (b) du paquet final : reformule les propriétés à « sauvegarde » en
applicateurs d'état via jet opposé, sans rien supprimer d'utile.
- Tir rapide retirée -> Arbalète à répétition renommée « Arbalète à chargeur », +30 dég.
- Renverse -> « Choc (jet opposé) » (À terre + Étourdi). Lanceur inchangé.
- Incapacitation -> « Étourdissement (jet opposé) » (Étourdi). Taser inchangé.
- Aveuglement + Incapacitation -> fusionnée dans « Étourdissement (jet opposé) ».
  Agent chimique : aveuglement géré par les Sens (gaz), inchangé en points.
- Contrainte « Sauvegarde ½ » -> « Esquive ½ » (jet opposé).
Chaque arme reste à 100. Usage : python scripts/patch_option_b.py"""
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


# --- Glossaire : retraits ---
for pat in [r"#### Tir rapide \(\+30\)\n.*?\n\n",
            r"#### Aveuglement \+ Incapacitation \(\+50\)\n.*?\n\n"]:
    assert re.search(pat, text, re.S), "glossaire non trouvé : " + pat
    text = re.sub(pat, "", text, count=1, flags=re.S)

# --- Glossaire : renommages (entrée complète) ---
rep("#### Renverse (+50)\nSur une touche, la cible doit réussir un **jet de sauvegarde** ou être violemment mise **à terre** et sonnée, incapable d'agir à son prochain tour.",
    "#### Choc (jet opposé) (+50)\nSur une touche, la cible tente un **jet opposé** (sa caractéristique la plus pertinente contre celle de l'attaquant). En cas d'échec, elle est mise **À terre** et **Étourdie** (voir États), incapable d'agir à son prochain tour. Munitions à létalité réduite, tirs de choc.")
rep("#### Incapacitation (+50)\nSur une touche, la cible doit réussir un **jet de sauvegarde** ou devenir **incapable d'agir** pendant un tour (décharge, choc).",
    "#### Étourdissement (jet opposé) (+50)\nSur une touche, la cible tente un **jet opposé**. En cas d'échec, elle est **Étourdie** (voir États) : elle perd ses actions et ne peut pas réagir pendant un tour. Décharge électrique, gaz incapacitant.")

# --- Barème ---
rep("· Tir en rafale · Tir rapide · Allonge ×3", "· Tir en rafale · Allonge ×3")
rep("| +50 | Vecteur de poison · Renverse · Immobilisation · Incapacitation · Aveuglement + Incapacitation · Étranglement |",
    "| +50 | Vecteur de poison · Choc · Immobilisation à distance · Étourdissement · Étranglement |")
rep("· Détection possible · Sauvegarde ½ · Réservoir explosif", "· Détection possible · Esquive ½ · Réservoir explosif")

# --- Armes ---
rep("| Arbalète à répétition | ✧✧✧ | Tir 20/70 m | 2 mains | 90 |  | PER | ★☆☆☆☆ | Tir rapide, Munitions (10 carreaux) |",
    "| Arbalète à chargeur | ✧✧✧ | Tir 20/70 m | 2 mains | 120 |  | PER | ★☆☆☆☆ | Munitions (10 carreaux) |")
rep("| Lanceur à létalité réduite | ✧✧✧ | Tir 20/40 m | 1 main | 95 |  | CON | ★★☆☆☆ | Renverse (sauvegarde), Munitions (6 cartouches) |",
    "| Lanceur à létalité réduite | ✧✧✧ | Tir 20/40 m | 1 main | 95 |  | CON | ★★☆☆☆ | Choc (jet opposé), Munitions (6 cartouches) |")
rep("| Arme à impulsion électrique | ✧✧✧ | Tir 10 m | 1 main | 10 |  | ÉLE | ★★☆☆☆ | Incapacitation (1 tour, sauvegarde), Perce-armure, Légère |",
    "| Arme à impulsion électrique | ✧✧✧ | Tir 10 m | 1 main | 10 |  | ÉLE | ★★☆☆☆ | Étourdissement (jet opposé), Perce-armure, Légère |")
rep("| Agent chimique | ✧✧✧ | Cône 10 m | 1 main | 0 |  |  | ★☆☆☆☆ | Aveuglement + Incapacitation (sauvegarde), Zone (cône 10 m), Persistant, Légère |",
    "| Agent chimique | ✧✧✧ | Cône 10 m | 1 main | 0 |  |  | ★☆☆☆☆ | Étourdissement (jet opposé), Zone (cône 10 m), Persistant, Légère |")
rep("Zone (rayon 10 m), Sauvegarde ½, Encombrante", "Zone (rayon 10 m), Esquive ½, Encombrante")

P.write_text(text, encoding="utf-8")
print("OK - option (b) appliquée : Choc / Étourdissement (jet opposé), arbalète renommée, Esquive ½")
