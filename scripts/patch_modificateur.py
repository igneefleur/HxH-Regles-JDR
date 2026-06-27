# -*- coding: utf-8 -*-
"""Ajoute la colonne « Mod. dégâts » (multiplicateur du modificateur de FOR/DEX, ×0 à ×3)
à droite de Dégâts, et rééquilibre : le multiplicateur coûte 20 points par niveau, compensés
en baissant les dégâts de base de 20×N (sans toucher illégalité, AM ni multiplicateur).
Armes Finesse → DEX, sinon FOR ; armes à gâchette/mécaniques/utilitaires → ×0.
Usage : python scripts/patch_modificateur.py"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
COST = 20

# (multiplicateur, stat) par arme. stat = FOR / DEX ; None pour ×0.
MULT = {
    "Dague": (1, "FOR"), "Katar": (1, "FOR"), "Épée courte": (1, "FOR"), "Épée longue": (2, "FOR"),
    "Épée à deux mains": (3, "FOR"), "Sabre": (1, "FOR"), "Rapière": (1, "FOR"), "Falchion": (2, "FOR"),
    "Macuahuitl": (3, "FOR"),
    "Hache à une main": (2, "FOR"), "Hache à deux mains": (3, "FOR"), "Gourdin / matraque": (1, "FOR"),
    "Masse d'armes": (2, "FOR"), "Marteau de guerre": (2, "FOR"), "Masse lourde": (3, "FOR"),
    "Fléau d'armes": (3, "FOR"), "Arme articulée (nunchaku)": (1, "FOR"), "Chaîne lestée": (1, "FOR"),
    "Kusarigama": (1, "FOR"), "Fouet": (1, "FOR"),
    "Lance": (2, "FOR"), "Pique": (2, "FOR"), "Hallebarde": (2, "FOR"), "Glaive d'hast": (2, "FOR"),
    "Trident / fourche": (2, "FOR"), "Arme de capture": (0, None), "Bâton": (1, "FOR"),
    "Javelot": (1, "FOR"), "Projectile léger de jet": (1, "FOR"), "Hache de jet": (1, "FOR"),
    "Boomerang": (1, "FOR"), "Arme enchevêtrante": (0, None),
    "Fronde": (1, "FOR"), "Sarbacane": (0, None), "Arc court": (1, "FOR"), "Arc long": (1, "FOR"),
    "Arc composite": (1, "FOR"), "Arc à poulies": (1, "FOR"), "Arbalète de poing": (0, None),
    "Arbalète légère": (0, None), "Arbalète lourde": (0, None), "Arbalète à répétition": (0, None),
    "Pistolet à poudre noire": (0, None), "Mousquet": (0, None), "Tromblon": (0, None),
    "Pistolet semi-auto": (0, None), "Revolver": (0, None), "Derringer": (0, None),
    "Derringer 4 canons": (0, None), "Pistolet-mitrailleur": (0, None), "Fusil d'assaut": (0, None),
    "Fusil de combat": (0, None), "Fusil de précision": (0, None), "Fusil anti-matériel": (0, None),
    "Fusil à pompe": (0, None), "Fusil à canon double": (0, None), "Carabine civile": (0, None),
    "Mitrailleuse légère": (0, None),
    "Grenade à main": (0, None), "Lance-grenades": (0, None), "Lance-roquettes": (0, None),
    "Charge explosive": (0, None), "Lance-flammes": (0, None),
    "Arme à impulsion électrique": (0, None), "Lanceur à létalité réduite": (0, None),
    "Agent chimique": (0, None),
    "Arme de poing renforcée": (1, "FOR"), "Griffes": (1, "FOR"), "Faucille de combat": (1, "FOR"),
    "Sai / Jutte": (1, "FOR"), "Éventail de fer": (1, "FOR"), "Crochets chinois": (1, "FOR"),
    "Bouclier offensif": (1, "FOR"), "Garrot": (1, "FOR"),
}

HEAD_OLD = "| Arme | AM | Portée | Dégâts | Illégalité | Propriétés |"
HEAD_NEW = "| Arme | AM | Portée | Dégâts | Mod. dégâts | Illégalité | Propriétés |"
SEP_OLD = "|---|---|---|---|---|---|"
SEP_NEW = "|---|---|---|---|---|---|---|"
ROW = re.compile(r"^\| ([^|]+?) \| ([✦✧]{3}) \| ([^|]+?) \| ([^|]+?) \| ([★☆]{5}) \| ([^|]+?) \|$")


def reduce_deg(deg, drop):
    m = re.match(r"^(\d+)(?:\s*\((\d+)\))?$", deg.strip())
    one = int(m.group(1))
    new_one = one - drop
    if m.group(2):
        diff = int(m.group(2)) - one
        return f"{new_one} ({new_one + diff})"
    return str(new_one)


P = Path("docs/content/livre/armes.md")
text = P.read_text(encoding="utf-8")
if "Mod. dégâts" in text:
    raise SystemExit("Déjà appliqué (colonne Mod. dégâts présente) : ne pas relancer, "
                     "cela re-baisserait les dégâts. Utiliser patch_modcell.py pour l'affichage.")
out, n = [], 0
for l in text.splitlines():
    if l.strip() == HEAD_OLD:
        out.append(HEAD_NEW)
        continue
    if l.strip() == SEP_OLD:
        out.append(SEP_NEW)
        continue
    m = ROW.match(l)
    if m:
        nom, am, por, deg, il, props = [g.strip() for g in m.groups()]
        if nom not in MULT:
            raise SystemExit(f"Arme non couverte : {nom}")
        mult, stat = MULT[nom]
        new_deg = reduce_deg(deg, COST * mult)
        modcell = f"×{mult} {stat}" if mult else ""
        out.append(f"| {nom} | {am} | {por} | {new_deg} | {modcell} | {il} | {props} |")
        n += 1
        continue
    out.append(l)

P.write_text("\n".join(out) + "\n", encoding="utf-8")
print("OK -", n, "armes : colonne Mod. dégâts ajoutée et dégâts rééquilibrés")
