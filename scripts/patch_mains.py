# -*- coding: utf-8 -*-
"""Ajoute la colonne « Mains » (avant Dégâts) : 1 main / Polyvalente / 2 mains.
Déplace les traits de maniement hors de Propriétés :
- propriété « Polyvalente » -> Mains « Polyvalente » (le +20 suit) ;
- propriété « À deux mains » -> Mains « 2 mains » (le −10 suit) ;
- sinon -> « 1 main » (et on retire une notation « (Y) » de dégâts parasite, sans Polyvalente).
Les points changent juste de colonne : chaque arme reste à 100.
Usage : python scripts/patch_mains.py"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
P = Path("docs/content/livre/armes.md")

HEAD_OLD = "| Arme | AM | Portée | Dégâts | Mod. dégâts | Illégalité | Propriétés |"
HEAD_NEW = "| Arme | AM | Portée | Mains | Dégâts | Mod. dégâts | Illégalité | Propriétés |"
SEP_OLD = "|---|---|---|---|---|---|---|"
SEP_NEW = "|---|---|---|---|---|---|---|---|"

out, n = [], 0
for l in P.read_text(encoding="utf-8").splitlines():
    s = l.strip()
    if s == HEAD_OLD:
        out.append(HEAD_NEW); continue
    if s == SEP_OLD:
        out.append(SEP_NEW); continue
    cells = l.split("|")[1:-1]
    if len(cells) == 7 and re.fullmatch(r"\s*[✦✧]{3}\s*", cells[1]):
        nom, am, por, deg, mod, il, props = [c.strip() for c in cells]
        plist = [p.strip() for p in re.split(r",(?![^(]*\))", props) if p.strip()]
        if "Polyvalente" in plist:
            mains = "Polyvalente"; plist.remove("Polyvalente")
        elif "À deux mains" in plist:
            mains = "2 mains"; plist.remove("À deux mains")
        else:
            mains = "1 main"
            deg = re.sub(r"\s*\(\d+\)", "", deg)        # retire un « (Y) » parasite
        new_props = ", ".join(plist) if plist else "Aucune"
        new = [nom, am, por, mains, deg, mod, il, new_props]
        out.append("| " + " | ".join(new) + " |")
        n += 1
        continue
    out.append(l)

P.write_text("\n".join(out) + "\n", encoding="utf-8")
print("OK -", n, "armes : colonne Mains ajoutée, traits de maniement déplacés")
