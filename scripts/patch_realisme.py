# -*- coding: utf-8 -*-
"""Corrige les 24 incohérences de réalisme repérées par la revue, en rééquilibrant
chaque arme à 100 points (sans toucher aux autres armes).
- Mains : 17 armes longues/d'épaule passent en « 2 mains » (−10), compensé par +10 dégâts
  (ou retrait d'une contrainte mineure pour les armes déjà à 240).
- AM : Gourdin 3→1, Projectile de jet 3→1 (+20 dégâts chacun), Macuahuitl 1→2 (−10 dégâts).
- Illégalité : Carabine 1★→2★, Sarbacane 2★→1★ (drop Surprise pour compenser).
- Portée : Sarbacane 10/30→10/20 (gratuit). - Mod : Fléau ×3→×2 (+20 dégâts).
Usage : python scripts/patch_realisme.py"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
P = Path("docs/content/livre/armes.md")


def am_sym(n):
    return "✦" * n + "✧" * (3 - n)


def il_sym(n):
    return "★" * n + "☆" * (5 - n)


# Changements par arme (valeurs finales). deg = dégâts absolus ; drop = propriétés à retirer.
FIX = {
    # --- Mains : armes d'hast ---
    "Pique": {"mains": "2 mains", "deg": "60", "deg_new": "70"},
    "Hallebarde": {"mains": "2 mains", "deg_new": "70"},
    "Glaive d'hast": {"mains": "2 mains", "deg_new": "70"},
    # --- Mains : armes à feu / lanceurs ---
    "Mousquet": {"mains": "2 mains", "deg_new": "170"},
    "Tromblon": {"mains": "2 mains", "deg_new": "130"},
    "Pistolet-mitrailleur": {"mains": "2 mains", "deg_new": "135"},
    "Fusil d'assaut": {"mains": "2 mains", "deg_new": "175"},
    "Fusil de combat": {"mains": "2 mains", "deg_new": "200"},
    "Fusil de précision": {"mains": "2 mains", "deg_new": "215"},
    "Fusil anti-matériel": {"mains": "2 mains", "drop": ["Maintenance requise"]},
    "Fusil à pompe": {"mains": "2 mains", "deg_new": "175"},
    "Fusil à canon double": {"mains": "2 mains", "deg_new": "145"},
    "Mitrailleuse légère": {"mains": "2 mains", "deg_new": "180"},
    "Lance-grenades": {"mains": "2 mains", "deg_new": "240"},
    "Lance-roquettes": {"mains": "2 mains", "drop": ["Dégainage lent"]},
    "Lance-flammes": {"mains": "2 mains", "deg_new": "175"},
    "Carabine civile": {"mains": "2 mains", "il": 2, "deg_new": "140"},   # + illégalité 2★
    # --- AM ---
    "Gourdin / matraque": {"am": 1, "deg_new": "50"},
    "Projectile léger de jet": {"am": 1, "deg_new": "70"},
    "Macuahuitl": {"am": 2, "deg_new": "40"},
    # --- Illégalité / portée / propriété ---
    "Sarbacane": {"il": 1, "por": "Tir 10/20 m", "drop": ["Surprise"]},
    # --- Mod. dégâts ---
    "Fléau d'armes": {"mod": "×2 FOR", "deg_new": "80"},
}


def drop_props(props, drops):
    toks = [t.strip() for t in re.split(r",(?![^(]*\))", props) if t.strip()]
    toks = [t for t in toks if re.sub(r"\s*\([^)]*\)", "", t).strip() not in drops]
    return ", ".join(toks) if toks else "Aucune"


out, n = [], 0
for l in P.read_text(encoding="utf-8").splitlines():
    cells = l.split("|")[1:-1]
    if len(cells) == 8 and re.fullmatch(r"\s*[✦✧]{3}\s*", cells[1]):
        nom, am, por, mains, deg, mod, il, props = [c.strip() for c in cells]
        f = FIX.get(nom)
        if f:
            if "mains" in f:
                mains = f["mains"]
            if "deg_new" in f:
                deg = f["deg_new"]
            if "am" in f:
                am = am_sym(f["am"])
            if "il" in f:
                il = il_sym(f["il"])
            if "por" in f:
                por = f["por"]
            if "mod" in f:
                mod = f["mod"]
            if "drop" in f:
                props = drop_props(props, f["drop"])
            n += 1
        out.append("| " + " | ".join([nom, am, por, mains, deg, mod, il, props]) + " |")
        continue
    out.append(l)

P.write_text("\n".join(out) + "\n", encoding="utf-8")
print("OK -", n, "armes corrigées")
