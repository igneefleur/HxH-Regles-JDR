# -*- coding: utf-8 -*-
"""Vérifie que chaque arme du tableau vaut exactement 100 points selon le barème
du document : Dégâts + Portée(s) + Propriétés + AM − Contraintes − Illégalité = 100.
Signale toute arme ≠ 100 et toute propriété non reconnue.
Usage : python scripts/verif_armes_100.py"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")


def norm(s):
    return s.replace("’", "'").strip()


BONUS = {
    # +10
    "Légère": 10, "Indésarmable": 10, "Retour": 10, "Dégainage instantané": 10,
    "Contourne un abri": 10, "Assommement": 10, "Poussée": 10, "Ralentissement": 10,
    "Fauchage": 10, "Éraflure": 10, "Aggravation": 10, "Dissimulable": 10, "Harcèlement": 10,
    # +20
    "Saisie": 10,
    "Finesse": 20, "Désarmement": 20, "Mains libres": 20,
    "Incendiaire": 20, "Persistant": 20, "Renversement": 20,
    "Allonge ×2": 20,
    # +30
    "Perce-armure": 30, "Tir en rafale": 30, "Allonge ×3": 30,
    # +40
    "Zone": 40, "Tir soutenu": 40, "Zone à bout portant": 40, "Perce-blindage": 40, "Allonge ×4": 40,
    # +50
    "Choc": 50, "Étourdissement": 50, "Immobilisation à distance": 50, "Étranglement": 50,
}
CONSTRAINT = {
    # −10
    "À deux mains": 10, "Lourde": 10, "Rechargement lent": 10, "Rechargement très lent": 10,
    "Lente à armer": 10, "Délai": 10, "Mise en place": 10, "Maintenance requise": 10,
    "Danger de proximité": 10, "Risque de raté": 10, "Manipulation dangereuse": 10, "Dégainage lent": 10,
    # −20
    "Encombrante": 20, "Bruyante": 20, "Recul": 20, "Inutilisable sous la pluie": 20,
    "Inutilisable au contact": 20, "Inefficace à courte/longue portée": 20,
    "Inefficace à courte portée": 20, "Inefficace au-delà de courte portée": 20,
    "Inefficace en espace confiné": 20, "Préparation": 20, "Souffle arrière": 20, "Fragile": 20,
    "Détection possible": 20, "Esquive ½": 20, "Réservoir explosif": 20, "Cadence lente": 20,
    "Enrayage possible": 20, "Sensible à l'humidité": 20, "Voyante": 20, "Compétence requise": 20,
    "Imprécise en mouvement": 20, "Surchauffe": 20,
    # −30
    "Très bruyante": 30, "Recul sévère": 30, "Immobile en tir": 30, "Préparation longue": 30,
    "Posée": 30, "Encombrement extrême": 30,
    # −40
    "Affût requis": 40, "Usage unique": 40, "Conditionnel": 40,
}
MUN = [(1, 1, 40), (2, 2, 35), (3, 4, 30), (5, 6, 25), (7, 10, 20),
       (11, 15, 15), (16, 20, 10), (21, 30, 5), (31, 100, 0)]


def mun_pts(n):
    for lo, hi, p in MUN:
        if lo <= n <= hi:
            return p
    return 0


def portee_pts(cell):
    total = 0
    for part in cell.split(" · "):
        p = norm(part).lower()
        if "cône" in p or "contact (posée)" in p:
            total += 0
        elif p.startswith("mêlée") or p.startswith("contact"):
            total += 10
        elif p.startswith("jet"):
            lng = int(re.findall(r"\d+", p)[-1])
            total += 10 if lng <= 20 else 20
        elif p.startswith("tir"):
            lng = int(re.findall(r"\d+", p)[-1])
            total += 20 if lng <= 40 else 30 if lng <= 90 else 40 if lng <= 180 else 50
    return total


def split_props(s):
    return [norm(p) for p in re.split(r",(?![^(]*\))", s) if norm(p)]


def base(tok):
    return norm(re.sub(r"\s*\([^)]*\)", "", tok))


lines = Path("docs/content/livre/armes.md").read_text(encoding="utf-8").splitlines()
bad, unknown = [], {}
n = 0
for l in lines:
    if not (l.startswith("|") and l.rstrip().endswith("|")):
        continue
    cells = [c.strip() for c in l.split("|")[1:-1]]
    if len(cells) != 9 or not re.fullmatch(r"[✦✧]{3}", cells[1]):
        continue                       # garde uniquement les lignes d'arme (AM en symboles)
    if cells[0] in ("Mains nues", "Pieds", "Tête"):
        continue                       # armes naturelles du corps : hors système de points
    n += 1
    nom, am, por, mains, deg, mod, typ, il, props = cells
    deg_v = int(re.match(r"\s*(\d+)", deg).group(1))
    illeg = il.count("★") * 20
    ampts = am.count("✦") * 10
    por_v = portee_pts(por)
    mm = re.search(r"×(\d)", mod)       # cellule vide = ×0
    mult_pts = (int(mm.group(1)) if mm else 0) * 20
    mains_pts = {"Polyvalente": 20, "2 mains": -10, "1 main": 0}.get(mains, 0)
    if typ in ("", "—"):
        type_pts = 0                   # 0 dégât -> pas de type (cellule vide)
    else:
        tt = [x.strip() for x in typ.split("/")]
        type_pts = 10 * (len(tt) - 1) + 20 * sum(x in {"FEU", "FRO", "ÉLE", "DÉC"} for x in tt)
    plus = minus = 0
    detail = [f"dég {deg_v}", f"AM +{ampts}", f"portée +{por_v}", f"type +{type_pts}", f"mod +{mult_pts}", f"mains {mains_pts:+d}"]
    if props.strip() != "Aucune":
        for tok in split_props(props):
            b = base(tok)
            if b.startswith("Munitions"):
                num = int(re.search(r"\((\d+)", tok).group(1))
                mp = mun_pts(num)
                minus += mp
                detail.append(f"{b} −{mp}")
            elif b in BONUS:
                plus += BONUS[b]
                detail.append(f"{b} +{BONUS[b]}")
            elif b in CONSTRAINT:
                minus += CONSTRAINT[b]
                detail.append(f"{b} −{CONSTRAINT[b]}")
            else:
                unknown.setdefault(b, []).append(nom)
                detail.append(f"{b} ??")
    total = deg_v + por_v + ampts + type_pts + mult_pts + mains_pts + plus - minus - illeg
    detail.append(f"illég −{illeg}")
    if total != 100:
        bad.append((nom, total, " | ".join(detail)))

print(f"armes vérifiées : {n}")
print(f"armes ≠ 100 : {len(bad)}")
for nom, t, d in bad:
    print(f"  ✗ {nom} = {t}\n      {d}")
if unknown:
    print("\npropriétés NON reconnues (hors barème) :")
    for k, v in unknown.items():
        print(f"  « {k} » → {', '.join(v)}")
if not bad and not unknown:
    print("✓ TOUTES les armes valent exactement 100 points.")
