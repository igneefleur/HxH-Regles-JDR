# -*- coding: utf-8 -*-
"""Extrait docs/content/regles/combat/critique-blessures.md vers scripts/blessures.json.

Outil de reprise en main : la page avait divergé de son générateur (23 zones dans la
page, 16 dans l'ancien dataset). On relit donc la page, qui fait foi, pour reconstituer
un dataset complet. À n'utiliser qu'une fois ; ensuite, blessures.json est la source et
build_critique.py écrit la page.

Usage : python scripts/extract_blessures.py
"""
import html
import json
import re
from pathlib import Path

SRC = Path("docs/content/regles/combat/critique-blessures.md")
DEST = Path("scripts/blessures.json")

page = SRC.read_text(encoding="utf-8")


def unesc(s):
    return html.unescape(s).strip()


# --- Table de localisation : plages d100 telles que publiées ---
loc_html = re.search(
    r"<thead><tr><th>1d100</th><th>Zone</th></tr></thead>.*?</table>", page, re.S
).group(0)
loc = []
for plage, zone in re.findall(r"<tr><td>([^<]+)</td><td>([^<]+)</td></tr>", loc_html):
    if " à " in plage:
        a, b = (int(x) for x in plage.split(" à "))
    else:
        a = b = int(plage)
    loc.append({"zone": unesc(zone), "de": a, "a": b})

# --- Sections de blessure ---
DIFFICULTES = "Facile|Moyenne|Difficile|Très difficile|Absurde|Quasi impossible|Impossible"


def parse_soin(bloc):
    """Retrouve la structure d'un soin depuis son rendu HTML."""
    if 'class="wf-roll wf-aucun"' in bloc:
        return {"possible": False}
    roll = unesc(re.search(r'<span class="wf-roll">(.*?)</span>', bloc, re.S).group(1))
    desc_m = re.search(r'<span class="wf-desc">(.*?)</span>', bloc, re.S)
    desc = unesc(desc_m.group(1)) if desc_m else ""
    out = {"possible": True, "description": desc}

    m = re.fullmatch(rf"Médecine \(Premiers secours\) Difficulté ({DIFFICULTES})", roll)
    if m:
        out["difficulte"] = m.group(1)
        return out
    m = re.fullmatch(rf"Médecine \(Chirurgie\) Difficulté ({DIFFICULTES}), puis Repos : (\d+) jours?", roll)
    if m:
        out.update(mode="chirurgie_repos", difficulte=m.group(1), jours=int(m.group(2)))
        return out
    m = re.fullmatch(rf"Médecine \(Chirurgie\) Difficulté ({DIFFICULTES})", roll)
    if m:
        out.update(mode="chirurgie", difficulte=m.group(1))
        return out
    m = re.fullmatch(r"Repos : (\d+) jours?", roll)
    if m:
        out.update(mode="repos", jours=int(m.group(1)))
        return out
    raise SystemExit(f"Soin non reconnu : {roll!r}")


zones = []
for sec in re.findall(r"<section class=\"wzone\">(.*?)</section>", page, re.S):
    titre = unesc(re.search(r'<h4 class="wzone-titre">(.*?)</h4>', sec, re.S).group(1))
    degres = []
    for art in re.findall(r'<article class="wfiche" data-deg="\d+">(.*?)</article>', sec, re.S):
        soins = re.findall(r'<div class="wf-soin">.*?</div>\s*(?=<div class="wf-soin">|$)', art, re.S)
        if len(soins) != 2:
            soins = re.split(r'(?=<div class="wf-soin">)', art.split('<div class="wf-soins">')[1])
            soins = [s for s in soins if 'wf-lbl' in s]
        degres.append({
            "degre": int(re.search(r'aria-label="Degré (\d+) sur 5"', art).group(1)),
            "nom": unesc(re.search(r'<p class="wf-nom">(.*?)</p>', art, re.S).group(1)),
            "effet": unesc(re.search(r'<p class="wf-effet">(.*?)</p>', art, re.S).group(1)),
            "premiersSecours": parse_soin(soins[0]),
            "traitement": parse_soin(soins[1]),
        })
    # Carte de perte : soit une illustration, soit une fiche « Ne pas avoir de X »
    perte_img = re.search(r'<article class="wfiche wperte wperte-img">.*?</article>', sec, re.S)
    if perte_img:
        perte = {"type": "image"}
    else:
        pa = re.search(r'<article class="wfiche wperte">(.*?)</article>', sec, re.S).group(1)
        perte = {
            "type": "fiche",
            "nom": unesc(re.search(r'<p class="wf-nom">(.*?)</p>', pa, re.S).group(1)),
            "effet": unesc(re.search(r'<p class="wf-effet">(.*?)</p>', pa, re.S).group(1)),
        }
    zones.append({"titre": titre, "perte": perte, "degres": degres})

data = {
    "_note": "Source des blessures. Édité à la main ; python scripts/build_critique.py régénère la page.",
    "localisation": loc,
    "zones": zones,
}
DEST.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"OK - {len(zones)} zones, {sum(len(z['degres']) for z in zones)} fiches, "
      f"{len(loc)} lignes de localisation -> {DEST}")
