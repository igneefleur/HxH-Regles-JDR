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
    "Retour": 10, "Dégainage instantané": 10, "Poussée": 10, "Éraflure": 10,
    "Aggravation": 10, "Dissimulable": 10, "Saisie": 10, "Parade": 10, "Finesse": 10, "Précise": 10, "Déchirante": 10,
    "Jumelable": 10, "Désarmement": 10,
    # +20
    "Vitesse du son": 20, "Mains libres": 20, "Renversement": 20, "Allonge ×2": 20, "Assommement": 20, "Indésarmable": 20, "Nuage persistant": 20,
    # +30
    "Allonge ×3": 30, "Immobilisation à distance": 30, "Aveuglement de zone": 50,
    # +40
    "Allonge ×4": 40, "Décharge incapacitante": 40,
}
# Propriétés à coût tiéré, parsées depuis la parenthèse (rayon / longueur, angle pour le cône)
ZONE_TIERS = {3: 20, 5: 30, 10: 40, 20: 50}
CONE_TIERS = {5: 20, 10: 30, 15: 40, 20: 50}
INEFF_TIERS = {"contact": 10, "courte": 20, "moyenne": 30, "longue": 40}
CONSTRAINT = {
    # −10
    "À deux mains": 10, "Lourde": 10, "Rechargement lent": 10, "Bruyante": 10,
    # −20
    "Très lourde": 20, "Surchauffe": 20, "Sensible à l'humidité": 20,
    # −30
    "Extrêmement lourde": 30, "Arme lente": 30,
    # −40
    "Usage unique": 40,
}
# Munitions : coût selon le nombre de TIRS avant recharge (capacité ÷ conso par attaque).
# Plus de tirs = plus pratique = coûte des points ; le mono-coup ne coûte rien.
MUN_COST = {1: 0, 2: 0, 4: 10, 6: 20, 10: 30, 15: 40, 20: 50}


def mun_pts(tirs):
    return MUN_COST.get(tirs, 0)


def zone_pts(r):
    return ZONE_TIERS.get(r, 0)


def cone_pts(length, angle=45):
    return min(50, CONE_TIERS.get(length, 0) + (10 if angle >= 90 else 0))


def portee_pts(cell):
    total = 0
    for part in re.split(r"\s*·\s*|<br>", cell):   # deux portées séparées par « · » ou un saut de ligne <br>
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


def portee_hors_plafond(cell):
    # Plafonds fermes : lancer 80 m max, tir 360 m max. Aucune portée illimitée.
    for part in re.split(r"\s*·\s*|<br>", cell):
        p = norm(part).lower()
        nums = re.findall(r"\d+", p)
        if not nums:
            continue
        lng = int(nums[-1])
        if p.startswith("jet") and lng > 80:
            return f"lancer {lng} m > 80"
        if p.startswith("tir") and lng > 360:
            return f"tir {lng} m > 360"
    return None


def split_props(s):
    return [norm(p) for p in re.split(r",(?![^(]*\))", s) if norm(p)]


def base(tok):
    return norm(re.sub(r"\s*\([^)]*\)", "", tok))


lines = Path("docs/content/regles/combat/armes.md").read_text(encoding="utf-8").splitlines()
bad, unknown, hors_portee, auto_sans_reservoir = [], {}, [], []
n = 0
for l in lines:
    if not (l.startswith("|") and l.rstrip().endswith("|")):
        continue
    cells = [c.strip() for c in l.split("|")[1:-1]]
    if len(cells) != 9 or not re.fullmatch(r"[✦✧]{3}", cells[1]):
        continue                       # garde uniquement les lignes d'arme (AM en symboles)
    if cells[0] in ("Mains nues", "Pieds", "Tête"):
        continue                       # armes naturelles du corps : seules exemptées du système
    n += 1
    nom, am, por, mains, deg, mod, typ, il, props = cells
    deg_v = int(re.match(r"\s*(\d+)", deg).group(1))
    illeg = il.count("★") * 20
    ampts = am.count("✦") * 10
    por_v = portee_pts(por)
    hp = portee_hors_plafond(por)
    if hp:
        hors_portee.append((nom, hp))
    mm = re.search(r"×(\d)", mod)       # cellule vide = ×0
    mult_pts = (int(mm.group(1)) if mm else 0) * 10   # modificateur : +10 par niveau
    mains_pts = {"Polyvalente": -10, "2 mains": -20, "1 main": 0}.get(mains, 0)   # rebate : plus l'arme exige de mains, plus elle rembourse
    if typ in ("", "—"):
        type_pts = 0                   # 0 dégât -> pas de type (cellule vide)
    else:
        tt = [x.strip() for x in typ.split("/")]
        type_pts = 10 * (len(tt) - 1) + 20 * sum(x in {"FEU", "FRO", "ÉLE", "DÉC"} for x in tt)
    plus = minus = 0
    has_auto = False
    has_rafale = False
    detail = [f"dég {deg_v}", f"AM +{ampts}", f"portée +{por_v}", f"type +{type_pts}", f"mod +{mult_pts}", f"mains {mains_pts:+d}"]
    if props.strip() != "Aucune":
        for tok in split_props(props):
            b = base(tok)
            if b.startswith("Munitions"):
                tirs = int(re.search(r"\((\d+)", tok).group(1))   # nombre de tirs avant recharge
                mp = mun_pts(tirs)
                plus += mp
                if "rafale" in tok.lower():
                    has_rafale = True
                detail.append(f"Munitions({tirs} tirs) +{mp}")
            elif b == "Zone":
                m = re.search(r"(\d+)\s*m", tok)
                zp = zone_pts(int(m.group(1)) if m else 0)
                plus += zp
                detail.append(f"Zone +{zp}")
            elif b in ("Cône", "Cone"):
                m = re.search(r"(\d+)\s*m", tok)
                ln = int(m.group(1)) if m else 0
                cp = cone_pts(ln, 90 if "90" in tok else 45)
                plus += cp
                detail.append(f"Cône +{cp}")
            elif b == "Tir soutenu":
                m = re.search(r"(\d+)\s*m", tok)
                cp = cone_pts(int(m.group(1)) if m else 0, 45)
                plus += cp
                has_auto = True
                detail.append(f"Tir soutenu +{cp}")
            elif b == "Inefficace de près":
                mb = re.search(r"\((\w+)", tok)
                ip = INEFF_TIERS.get(mb.group(1) if mb else "", 0)
                minus += ip
                detail.append(f"Inefficace de près −{ip}")
            elif b == "Perce-armure":
                ign = int(re.search(r"\((\d+)", tok).group(1))   # part de réduction ignorée
                pp = ign // 2                                    # ignore 20/40/60/80/100 -> +10/20/30/40/50
                plus += pp
                detail.append(f"Perce-armure({ign}) +{pp}")
            elif b in BONUS:
                plus += BONUS[b]
                detail.append(f"{b} +{BONUS[b]}")
            elif b in CONSTRAINT:
                minus += CONSTRAINT[b]
                detail.append(f"{b} −{CONSTRAINT[b]}")
            else:
                unknown.setdefault(b, []).append(nom)
                detail.append(f"{b} ??")
    total = (deg_v - 20) + por_v + ampts + type_pts + mult_pts + mains_pts + plus - minus - illeg  # 20 de dégâts de base gratuits
    detail.append(f"illég −{illeg}")
    if total != 100:
        bad.append((nom, total, " | ".join(detail)))
    if has_auto and not has_rafale:
        auto_sans_reservoir.append(nom)

print(f"armes vérifiées : {n}")
print(f"armes ≠ 100 : {len(bad)}")
for nom, t, d in bad:
    print(f"  ✗ {nom} = {t}\n      {d}")
if unknown:
    print("\npropriétés NON reconnues (hors barème) :")
    for k, v in unknown.items():
        print(f"  « {k} » → {', '.join(v)}")
if hors_portee:
    print("\nportées HORS plafond (lancer 80 m / tir 360 m max) :")
    for nom, hp in hors_portee:
        print(f"  ✗ {nom} : {hp}")
if auto_sans_reservoir:
    print("\ntir automatique sans rafale (Tir soutenu exige une arme à rafale) :")
    for nom in auto_sans_reservoir:
        print(f"  ✗ {nom}")
if not bad and not unknown and not hors_portee and not auto_sans_reservoir:
    print("✓ TOUTES les armes valent exactement 100 points.")
