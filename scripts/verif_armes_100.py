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
    "Recharge Rapide": 10, "Retour": 10, "Dégainage instantané": 10, "Poussée": 10,
    "Dissimulable": 10, "Saisie": 10, "Parade": 10, "Finesse": 10, "Précise": 10,
    "Jumelable": 10, "Désarmement": 10,
    # +20
    "Mains libres": 20, "Renversement": 20, "Assommement": 20, "Indésarmable": 20, "Nuage persistant": 20,
    # +30
    "Immobilisation à distance": 30,
    # +40
    "Décharge incapacitante": 40,
    # +50
    "Aveuglement de zone": 50,
}
# Propriétés à coût tiéré, parsées depuis la parenthèse (rayon / longueur, angle pour le cône)
ZONE_TIERS = {3: 20, 5: 30, 10: 40, 20: 50}
CONE_TIERS = {5: 20, 10: 30, 15: 40, 20: 50}   # cône : table de LONGUEUR
CONE_ANGLE = {45: 0, 90: 10}                    # cône : table d'ANGLE (s'ajoute à la longueur)
# Inefficace de près : zone morte, deux barèmes. Mêlée = crans d'allonge (×N → −N×10). Distance = % de la portée max (20/40/60/80/100 → −10/−20/−30/−40/−50).
CONSTRAINT = {
    # −10
    "Lourde": 10, "Rechargement lent": 10, "Bruyante": 10,
    # −20
    "Très lourde": 20, "Surchauffe": 20, "Sensible à l'humidité": 20,
    # −30
    "Extrêmement lourde": 30, "Arme lente": 30,
    # −40
    "Usage unique": 40,
}
# Munitions : coût selon le nombre de TIRS avant recharge (capacité ÷ conso par attaque).
# Plus de tirs = plus pratique = coûte des points ; le mono-coup ne coûte rien.
MUN_COST = {1: 0, 2: 10, 4: 20, 6: 30, 10: 40, 15: 50}


def mun_pts(tirs):
    return MUN_COST.get(tirs, 0)


def zone_pts(r):
    return ZONE_TIERS.get(r, 0)


def portee_pts(cell):
    total = 0
    parts = [x for x in re.split(r"\s*·\s*|<br>", cell) if norm(x)]   # portées séparées par « · » ou <br>
    for part in parts:
        p = norm(part).lower()
        if "cône" in p:   # le cône est une portée : longueur (table) + angle (table)
            nums = re.findall(r"\d+", p)
            ln = int(nums[0]) if nums else 0
            ang = int(nums[1]) if len(nums) > 1 else 45
            total += CONE_TIERS.get(ln, 0) + (CONE_ANGLE[90] if ang >= 90 else CONE_ANGLE[45])
        elif "contact (posée)" in p:
            total += 0
        elif p.startswith("mêlée") or p.startswith("contact"):
            total += 0   # la mêlée (contact) est gratuite
        elif p.startswith("allonge"):   # allonge = mêlée étendue (portée mêlée)
            total += {2: 20, 3: 30, 4: 40, 5: 50}.get(int(re.findall(r"\d+", p)[0]), 0)
        elif p.startswith("jet"):
            lng = int(re.findall(r"\d+", p)[-1])   # coût selon la portée max (longue), valeurs réelles : 5 crans +10→+50
            total += 10 if lng <= 15 else 20 if lng <= 30 else 30 if lng <= 50 else 40 if lng <= 80 else 50
        elif p.startswith("tir"):
            lng = int(re.findall(r"\d+", p)[-1])   # coût selon la portée max (longue), valeurs réelles : 5 crans +10→+50
            total += 10 if lng <= 50 else 20 if lng <= 150 else 30 if lng <= 300 else 40 if lng <= 800 else 50
    total += max(0, len(parts) - 1) * 10   # nombre de portées : 1 → 0, 2 → +10, 3 → +20
    return total


def portee_hors_plafond(cell):
    # Plafonds fermes : lancer 120 m max, tir 2500 m max. Aucune portée illimitée.
    for part in re.split(r"\s*·\s*|<br>", cell):
        p = norm(part).lower()
        nums = re.findall(r"\d+", p)
        if not nums:
            continue
        lng = int(nums[-1])
        if p.startswith("jet") and lng > 120:
            return f"lancer {lng} m > 120"
        if p.startswith("tir") and lng > 2500:
            return f"tir {lng} m > 2500"
    return None


def split_props(s):
    return [norm(p) for p in re.split(r",(?![^(]*\))", s) if norm(p)]


def base(tok):
    return norm(re.sub(r"\s*\([^)]*\)", "", tok))


lines = Path("docs/content/regles/combat/armes.md").read_text(encoding="utf-8").splitlines()
bad, unknown, hors_portee, auto_sans_reservoir, tir_sans_mun, am_illeg = [], {}, [], [], [], []
n = 0
for l in lines:
    if not (l.startswith("|") and l.rstrip().endswith("|")):
        continue
    cells = [c.strip() for c in l.split("|")[1:-1]]
    if len(cells) != 11 or not re.fullmatch(r"[✦✧]{3}", cells[1]):
        continue                       # garde uniquement les lignes d'arme (AM en symboles)
    if cells[0] in ("Main", "Pied", "Tête", "Coude", "Genou"):
        continue                       # armes naturelles du corps : seules exemptées du système
    n += 1
    nom, am, por, mun, mains, deg, mod, typ, il, prix, props = cells   # Prix (colonne cosmetique) ignore dans le total
    deg_v = int(re.match(r"\s*(\d+)", deg).group(1))
    illeg = il.count("★") * 20
    ampts = am.count("✦") * 10
    if am.count("✦") + il.count("★") > 5:   # plafond croisé : AM élevée ⇄ illégalité élevée s'excluent
        am_illeg.append((nom, f"{am.count('✦')}✦ + {il.count('★')}★ = {am.count('✦') + il.count('★')}"))
    por_v = portee_pts(por)
    hp = portee_hors_plafond(por)
    if hp:
        hors_portee.append((nom, hp))
    mm = re.search(r"×(\d)", mod)       # cellule vide = aucun modificateur
    pm = re.search(r"\+(\d+)", mod)     # propulsion mécanique : dégâts fixes de l'arme
    if mm:
        mult_pts = int(mm.group(1)) * 10        # force du porteur : +10 par niveau ×N
    elif pm:
        mult_pts = int(pm.group(1)) // 2        # propulsion : coût = dégâts/2 (efficace, exclusif du ×N FOR)
    else:
        mult_pts = 0
    mains_pts = {"Polyvalente": -10, "2 mains": -20, "1 main": 0}.get(mains, 0)   # rebate : plus l'arme exige de mains, plus elle rembourse
    if typ in ("", "—"):
        type_pts = 0                   # 0 dégât -> pas de type (cellule vide)
    else:
        tt = [x.strip() for x in typ.split("/")]
        type_pts = min(50, 10 * (len(tt) - 1)) + 20 * sum(x in {"FEU", "FRO", "ÉLE", "DÉC"} for x in tt)   # nombre de types plafonné à 6 (+50)
    plus = minus = 0
    has_rafale = False
    has_cone = "cône" in norm(por).lower()
    if ("tir" in norm(por).lower() or has_cone) and not mun.strip():
        tir_sans_mun.append(nom)   # règle : arme de tir ou de cône -> munitions obligatoires (colonne dédiée)
    detail = [f"dég {deg_v}", f"AM +{ampts}", f"portée +{por_v}", f"type +{type_pts}", f"mod +{mult_pts}", f"mains {mains_pts:+d}"]
    if mun.strip():                                     # munitions : colonne dédiée (après Portée)
        tirs = int(re.search(r"(\d+)", mun).group(1))   # nombre de tirs avant recharge
        mp = mun_pts(tirs)
        plus += mp
        if "munitions par tir" in mun.lower():
            has_rafale = True
        detail.append(f"Munitions({mun}) +{mp}")
    if props.strip() != "Aucune":
        for tok in split_props(props):
            b = base(tok)
            if b == "Zone":
                m = re.search(r"(\d+)\s*m", tok)
                zp = zone_pts(int(m.group(1)) if m else 0)
                plus += zp
                detail.append(f"Zone +{zp}")
            elif b == "Inefficace de près":
                ma = re.search(r"[Aa]llonge\D*(\d)", tok)   # mêlée : zone morte en crans d'allonge (×1→−10 … ×5→−50)
                mp = re.search(r"(\d+)\s*%", tok)           # distance : zone morte en % de la portée max (20→−10 … 100→−50)
                ip = int(ma.group(1)) * 10 if ma else (int(mp.group(1)) // 2 if mp else 0)
                minus += ip
                detail.append(f"Inefficace de près −{ip}")
            elif b == "Perce-armure":
                ign = int(re.search(r"\((\d+)", tok).group(1))   # part de réduction ignorée
                pp = ign // 2                                    # ignore 20/40/60/80/100 -> +10/20/30/40/50
                plus += pp
                detail.append(f"Perce-armure({ign}) +{pp}")
            elif b in ("Éraflure", "Aggravation"):
                pct = int(re.search(r"\((\d+)", tok).group(1))   # palier : le coût vaut le bonus en %
                plus += pct
                detail.append(f"{b}({pct}%) +{pct}")
            elif b == "Déchirante":
                m = re.search(r"(\d+)", tok)         # saignement en PV ; base −5 si non précisé
                saign = int(m.group(1)) if m else 5
                dp = min(50, saign * 2)              # −5→+10 … −25→+50
                plus += dp
                detail.append(f"Déchirante(−{saign}) +{dp}")
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
    if has_rafale and not has_cone:
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
    print("\nportées HORS plafond (lancer 120 m / tir 2500 m max) :")
    for nom, hp in hors_portee:
        print(f"  ✗ {nom} : {hp}")
if auto_sans_reservoir:
    print("\ntir en rafale sans cône (une rafale arrose un cône) :")
    for nom in auto_sans_reservoir:
        print(f"  ✗ {nom}")
if tir_sans_mun:
    print("\narmes de tir/cône SANS munitions (obligatoire) :")
    for nom in tir_sans_mun:
        print(f"  ✗ {nom}")
if am_illeg:
    print("\nAM + illégalité > 5 (arme trop martiale ET trop illégale) :")
    for nom, d in am_illeg:
        print(f"  ✗ {nom} : {d}")
if not bad and not unknown and not hors_portee and not auto_sans_reservoir and not tir_sans_mun and not am_illeg:
    print("✓ TOUTES les armes valent exactement 100 points.")
