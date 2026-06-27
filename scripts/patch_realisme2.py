# -*- coding: utf-8 -*-
"""Corrige les 3 incohérences résiduelles trouvées par la contre-vérification :
- Arbalète légère / Arbalète à répétition : 1 main -> 2 mains (−10), compensé +10 dégâts.
- Garrot : AM 1 -> 3 (+20), compensé en retirant « Réduit au silence » (redondant avec Étranglement,
  qui empêche déjà de parler/crier). Chaque arme reste à 100.
Usage : python scripts/patch_realisme2.py"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
P = Path("docs/content/livre/armes.md")


def am_sym(n):
    return "✦" * n + "✧" * (3 - n)


FIX = {
    "Arbalète légère": {"mains": "2 mains", "deg": "140"},
    "Arbalète à répétition": {"mains": "2 mains", "deg": "90"},
    "Garrot": {"am": 3, "drop": ["Réduit au silence"]},
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
            if "deg" in f:
                deg = f["deg"]
            if "am" in f:
                am = am_sym(f["am"])
            if "drop" in f:
                props = drop_props(props, f["drop"])
            n += 1
        out.append("| " + " | ".join([nom, am, por, mains, deg, mod, il, props]) + " |")
        continue
    out.append(l)

P.write_text("\n".join(out) + "\n", encoding="utf-8")
print("OK -", n, "armes corrigées")
