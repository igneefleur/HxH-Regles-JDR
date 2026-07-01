# -*- coding: utf-8 -*-
"""Page Critique et Blessures : gravité -> degré -> localisation (proba exacte) -> blessure.
Le contenu des blessures (nom, effet, premiers secours, traitement) est lu depuis le dataset
audité scripts/blessures_audit.json. Saignements en multiples de 5 ; jets formatés ; le
traitement peut combiner chirurgie et repos (mode "chirurgie_repos").
Usage : python scripts/build_critique.py"""
import html
import json
import re
from pathlib import Path

DEST = Path("docs/content/regles/combat/critique-blessures.md")
AUDIT = json.loads(Path("scripts/blessures_audit.json").read_text(encoding="utf-8"))
for _z in AUDIT:
    AUDIT[_z].sort(key=lambda x: x["degre"])

ORDER = ["Cou", "Tête", "Coude", "Cœur", "Aine", "Pied", "Main", "Genou", "Abdomen",
         "Bras", "Cuisse", "Mollet", "Torse", "Œil", "Poignet", "Épaule"]
MALUS = {"Cou": 80, "Tête": 60, "Coude": 60, "Cœur": 60, "Aine": 60, "Pied": 50, "Main": 40,
         "Genou": 40, "Abdomen": 20, "Bras": 20, "Cuisse": 20, "Mollet": 10, "Torse": 10,
         "Œil": 100, "Poignet": 40, "Épaule": 30}
TITRES = {"Cou": "Blessure au Cou", "Tête": "Blessure à la Tête", "Coude": "Blessure au Coude",
          "Cœur": "Blessure au Cœur", "Aine": "Blessure à l'Aine", "Pied": "Blessure au Pied",
          "Main": "Blessure à la Main", "Genou": "Blessure au Genou", "Abdomen": "Blessure à l'Abdomen",
          "Bras": "Blessure au Bras", "Cuisse": "Blessure à la Cuisse", "Mollet": "Blessure au Mollet",
          "Torse": "Blessure au Torse", "Œil": "Blessure à l'Œil", "Poignet": "Blessure au Poignet",
          "Épaule": "Blessure à l'Épaule"}

# --- Localisation : poids = 110 - malus ; proba = poids / somme ; plages d100 (plus fort reste, somme = 100) ---
weights = {p: 110 - MALUS[p] for p in ORDER}
W = sum(weights.values())
exact = {p: weights[p] * 100 / W for p in ORDER}
widths = {p: int(exact[p]) for p in ORDER}
need = 100 - sum(widths.values())
for p in sorted(ORDER, key=lambda p: (-(exact[p] - int(exact[p])), ORDER.index(p)))[:need]:
    widths[p] += 1
assert sum(widths.values()) == 100
loc_order = sorted(ORDER, key=lambda p: (-widths[p], ORDER.index(p)))
ranges, cum = {}, 0
for p in loc_order:
    ranges[p] = (cum + 1, cum + widths[p])
    cum += widths[p]

def esc(s):
    return html.escape((s or "").strip(), quote=False)

def phrase(s):
    s = (s or "").strip()
    if s and s[-1] not in ".!?":
        s += "."
    return s

def round5(m):
    n = int(m.group(1))
    r = round(n / 5) * 5
    if n > 0:
        r = max(5, r)
    return f"{r} PV"

def normalize_effet(s):
    s = phrase(s)
    s = re.sub(r"(\d+) PV", round5, s)                       # « X PV » -> multiple de 5
    s = re.sub(r"([Ss]aignement)\s+(\d+)\b(?!\s*PV)",        # « Saignement N » sans unité
               lambda m: f"{m.group(1)} {max(5, round(int(m.group(2)) / 5) * 5)} PV par tour", s)
    s = re.sub(r"\s*(?:Aucun|Pas de|Sans) saignement\.?", "", s, flags=re.I)  # négations parasites
    s = re.sub(r"\b[Mm]alus(?:\s+de)?\s+(?=[−-])", "", s)    # « Malus de −X » -> « −X »
    s = re.sub(r"\bÉtat ", "", s)                            # « État Mutisme » -> « Mutisme »
    s = re.sub(r"\bHors d'usage\b", "hors d'usage", s)       # pas un état défini : minuscule
    s = re.sub(r"premiers soins", "premiers secours", s)
    s = re.sub(r"premier soin\b", "premier secours", s)
    s = s.replace("PV/tour", "PV par tour")                  # notation uniforme du saignement
    s = s.replace("Au tour suivant", "Au début de son prochain tour")   # timing clair (filet de sécurité)
    s = re.sub(r" +([.,])", r"\1", s)                        # pas d'espace avant . ou , (français)
    s = re.sub(r" {2,}", " ", s).strip()
    return phrase(s)

def loc_table():
    rows = []
    for p in loc_order:
        a, b = ranges[p]
        plage = str(a) if a == b else f"{a} à {b}"
        rows.append(f"<tr><td>{plage}</td><td>{p}</td></tr>")
    return ("<table>\n<thead><tr><th>1d100</th><th>Zone</th></tr></thead>\n"
            "<tbody>\n" + "\n".join(rows) + "\n</tbody>\n</table>")

def jours_txt(j):
    j = int(j)
    return f"{j} {'jour' if j <= 1 else 'jours'}"

def soin(label, roll, desc=None, aucun=False):
    if aucun:
        return (f'<div class="wf-soin"><span class="wf-lbl">{label}</span>'
                '<span class="wf-roll wf-aucun">aucun</span></div>')
    return (f'<div class="wf-soin"><span class="wf-lbl">{label}</span>'
            f'<span class="wf-roll">{roll}</span>'
            f'<span class="wf-desc">{esc(desc)}</span></div>')

def secours_block(ps):
    if not ps.get("possible"):
        return soin("Secours", None, aucun=True)
    return soin("Secours", f'Médecine (Premiers secours) Difficulté {esc(ps["difficulte"])}', ps["description"])

def traitement_block(tr):
    mode = tr.get("mode")
    if mode == "aucun":
        return soin("Traitement", None, aucun=True)
    if mode == "repos":
        roll = f'Repos : {jours_txt(tr["jours"])}'
    elif mode == "chirurgie":
        roll = f'Médecine (Chirurgie) Difficulté {esc(tr["difficulte"])}'
    else:  # chirurgie_repos
        roll = f'Médecine (Chirurgie) Difficulté {esc(tr["difficulte"])}, puis Repos : {jours_txt(tr["jours"])}'
    return soin("Traitement", roll, tr["description"])

def fiche(zone, i):
    l = AUDIT[zone][i]
    bl = (l["nom"] or "").split(":")[0].strip().rstrip(".")
    ef = normalize_effet(l["effet"])
    jauge = "▰" * (i + 1) + "▱" * (4 - i)
    return (
        f'<article class="wfiche" data-deg="{i+1}">'
        f'<header class="wf-head">'
        f'<span class="wf-sceau" aria-label="Degré {i+1} sur 5">{i+1}</span>'
        f'<p class="wf-nom">{esc(bl)}</p>'
        f'<span class="wf-jauge" aria-hidden="true">{jauge}</span>'
        f'</header>'
        f'<p class="wf-effet">{esc(ef)}</p>'
        f'<div class="wf-soins">'
        f'{secours_block(l["premiersSecours"])}'
        f'{traitement_block(l["traitement"])}'
        f'</div>'
        f'</article>')

def zone_section(zone):
    fiches = "".join(fiche(zone, i) for i in range(len(AUDIT[zone])))
    return (f'<section class="wzone"><h4 class="wzone-titre">{TITRES[zone]}</h4>'
            f'<div class="wgrid">{fiches}</div></section>')

HEAD = """# Critique et Blessures

<div class="cols" markdown>

Un coup porté avec une réussite exceptionnelle peut ouvrir une blessure grave, une plaie durable qui handicape le blessé bien au-delà des dégâts. On la résout pas à pas : on calcule sa gravité, on en déduit le degré de blessure, on localise la plaie, puis on lit la blessure correspondante.

### Le coup critique

Une attaque inflige un critique lorsqu'elle atteint 200 % de son degré de touche. Le coup ne se contente alors pas de blesser : il peut laisser une blessure grave, déterminée par les étapes ci-dessous.

### Gravité

<p class="formula">Gravité = dégâts subis (en % des PV max, plafonné à 100) + modificateur de critique + 1d100</p>

Les PV maximaux valant 100, des dégâts en points se lisent directement en pourcentage. La gravité se place sur l'échelle de difficulté, de 120 à 400 : en deçà de 120, le coup reste une attaque ordinaire, sans séquelle ; à partir de 120, il inflige une blessure grave, d'autant plus sévère que la gravité est haute.

### Degré de blessure

La gravité se convertit en degré de blessure, de 1 (le plus léger) à 5 (le pire).

<div class="keep" markdown>

<table>
<thead><tr><th>Gravité</th><th>Degré</th></tr></thead>
<tbody>
<tr><td>120 à 179</td><td>1</td></tr>
<tr><td>180 à 239</td><td>2</td></tr>
<tr><td>240 à 319</td><td>3</td></tr>
<tr><td>320 à 399</td><td>4</td></tr>
<tr><td>400 et plus</td><td>5</td></tr>
</tbody>
</table>

</div>

### Localisation

Si l'attaque visait déjà une zone précise (manœuvre Viser), la blessure la frappe et l'on passe directement à sa table. Sinon, on lance 1d100 sur la table ci-dessous : la probabilité d'une zone décroît avec son malus de visée, si bien que les endroits difficiles à atteindre sont les plus rares au hasard.

<div class="keep" markdown>

__LOC__

</div>

### Saignement

Une plaie ouverte continue de saigner tant qu'elle n'est pas refermée. « Saignement de −X PV » signifie que le blessé perd X PV à la fin de chacun de ses tours, jusqu'à ce qu'un soin l'arrête. Plusieurs saignements se cumulent.

### Soigner une blessure

Chaque blessure se soigne en deux temps, indiqués sous son degré. Les premiers secours sont un geste d'urgence, un test de Médecine qui stoppe l'hémorragie et stabilise le blessé. Le traitement est la vraie réparation : un test de Médecine (Chirurgie), du repos, ou les deux quand il faut opérer puis laisser convalescer. Il lève les malus et restaure la zone, hormis les pertes définitives. Chaque degré détaille son effet, ses premiers secours et son traitement.

---

### Blessures

Une fois le degré et la zone connus, on lit la blessure dans l'entrée de la zone touchée, à la ligne du degré.

"""

wounds = '<div class="wounds">\n' + "\n".join(zone_section(z) for z in ORDER) + '\n</div>'
page = HEAD.replace("__LOC__", loc_table()) + wounds + "\n\n</div>\n"
DEST.write_text(page, encoding="utf-8")
print("OK -", len(ORDER), "zones ecrites")
