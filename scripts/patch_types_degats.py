# -*- coding: utf-8 -*-
"""Ajoute la colonne « Type » (à droite de Dégâts) : type(s) de dégâts CON/TRA/PER/FEU/FRO/ÉLE/DÉC.
Coût : +10 par type au-delà du premier, +20 par type élémentaire (FEU/FRO/ÉLE/DÉC).
Compensé en baissant les dégâts du coût (sauf le taser à 10 dégâts : on retire « Dissimulable »).
L'agent chimique (0 dégât) n'a pas de type (« — », gratuit). Chaque arme reste à 100.
Usage : python scripts/patch_types_degats.py"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
P = Path("docs/content/livre/armes.md")
ELEM = {"FEU", "FRO", "ÉLE", "DÉC"}

TYPE = {
    "Dague": ("PER", ""), "Katar": ("PER", ""), "Épée courte": ("TRA", ""), "Épée longue": ("TRA", ""),
    "Épée à deux mains": ("TRA", ""), "Sabre": ("TRA", ""), "Rapière": ("PER", ""), "Falchion": ("TRA", ""),
    "Macuahuitl": ("TRA", "CON"),
    "Hache à une main": ("TRA", ""), "Hache à deux mains": ("TRA", ""), "Gourdin / matraque": ("CON", ""),
    "Masse d'armes": ("CON", ""), "Marteau de guerre": ("CON", "PER"), "Masse lourde": ("CON", ""),
    "Fléau d'armes": ("CON", ""), "Arme articulée (nunchaku)": ("CON", ""), "Chaîne lestée": ("CON", ""),
    "Kusarigama": ("TRA", "CON"), "Fouet": ("CON", ""),
    "Lance": ("PER", ""), "Pique": ("PER", ""), "Hallebarde": ("TRA", "PER"), "Glaive d'hast": ("TRA", ""),
    "Trident / fourche": ("PER", ""), "Arme de capture": ("CON", ""), "Bâton": ("CON", ""),
    "Javelot": ("PER", ""), "Projectile léger de jet": ("PER", ""), "Hache de jet": ("TRA", ""),
    "Boomerang": ("CON", ""), "Arme enchevêtrante": ("CON", ""),
    "Fronde": ("CON", ""), "Sarbacane": ("PER", ""), "Arc court": ("PER", ""), "Arc long": ("PER", ""),
    "Arc composite": ("PER", ""), "Arc à poulies": ("PER", ""), "Arbalète de poing": ("PER", ""),
    "Arbalète légère": ("PER", ""), "Arbalète lourde": ("PER", ""), "Arbalète à répétition": ("PER", ""),
    "Pistolet à poudre noire": ("PER", ""), "Mousquet": ("PER", ""), "Tromblon": ("PER", ""),
    "Pistolet semi-auto": ("PER", ""), "Revolver": ("PER", ""), "Derringer": ("PER", ""),
    "Derringer 4 canons": ("PER", ""), "Pistolet-mitrailleur": ("PER", ""), "Fusil d'assaut": ("PER", ""),
    "Fusil de combat": ("PER", ""), "Fusil de précision": ("PER", ""), "Fusil anti-matériel": ("PER", ""),
    "Fusil à pompe": ("PER", ""), "Fusil à canon double": ("PER", ""), "Carabine civile": ("PER", ""),
    "Mitrailleuse légère": ("PER", ""),
    "Grenade à main": ("CON", "PER"), "Lance-grenades": ("CON", "PER"), "Lance-roquettes": ("CON", "PER"),
    "Charge explosive": ("CON", ""), "Lance-flammes": ("FEU", ""),
    "Arme à impulsion électrique": ("ÉLE", ""), "Lanceur à létalité réduite": ("CON", ""),
    "Agent chimique": ("—", ""),
    "Arme de poing renforcée": ("CON", ""), "Griffes": ("TRA", ""), "Faucille de combat": ("TRA", ""),
    "Sai / Jutte": ("CON", ""), "Éventail de fer": ("CON", ""), "Crochets chinois": ("TRA", ""),
    "Bouclier offensif": ("CON", ""), "Garrot": ("TRA", ""),
}

HEAD_OLD = "| Arme | AM | Portée | Mains | Dégâts | Mod. dégâts | Illégalité | Propriétés |"
HEAD_NEW = "| Arme | AM | Portée | Mains | Dégâts | Type | Mod. dégâts | Illégalité | Propriétés |"
SEP_OLD = "|---|---|---|---|---|---|---|---|"
SEP_NEW = "|---|---|---|---|---|---|---|---|---|"


def drop_prop(props, name):
    toks = [t.strip() for t in re.split(r",(?![^(]*\))", props) if t.strip()]
    toks = [t for t in toks if re.sub(r"\s*\([^)]*\)", "", t).strip() != name]
    return ", ".join(toks) if toks else "Aucune"


out, n = [], 0
for l in P.read_text(encoding="utf-8").splitlines():
    s = l.strip()
    if s == HEAD_OLD:
        out.append(HEAD_NEW); continue
    if s == SEP_OLD:
        out.append(SEP_NEW); continue
    cells = l.split("|")[1:-1]
    if len(cells) == 8 and re.fullmatch(r"\s*[✦✧]{3}\s*", cells[1]):
        nom, am, por, mains, deg, mod, il, props = [c.strip() for c in cells]
        p, sec = TYPE[nom]
        if p == "—":
            type_str, cost = "", 0     # 0 dégât -> pas de type (cellule vide, jamais « — »)
        else:
            types = [p] + ([sec] if sec else [])
            type_str = " / ".join(types)
            cost = 10 * (len(types) - 1) + 20 * sum(t in ELEM for t in types)
        if cost:
            if nom == "Arme à impulsion électrique":   # 10 dégâts : on compense en propriété
                props = drop_prop(props, "Dissimulable")
            else:
                m = re.match(r"^(\d+)(.*)$", deg)
                deg = str(int(m.group(1)) - cost) + m.group(2)
        new = [nom, am, por, mains, deg, type_str, mod, il, props]
        out.append("| " + " | ".join(new) + " |")
        n += 1
        continue
    out.append(l)

P.write_text("\n".join(out) + "\n", encoding="utf-8")
print("OK -", n, "armes : colonne Type ajoutée")
