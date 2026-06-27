# -*- coding: utf-8 -*-
"""Correction orthographique (accents, signe −, espaces français) des 7 entrées
produites en ASCII par certains agents. Contenu et règles préservés ; seules les
chaînes nom/effet/descriptions sont corrigées. Idempotent.
Usage : python scripts/patch_orthographe.py"""
import json
from pathlib import Path

P = Path("scripts/blessures_audit.json")
ds = json.loads(P.read_text(encoding="utf-8"))

# (zone, degré) -> {champ corrigé}. On ne touche pas mode/difficulte/jours/possible.
PATCH = {
    ("Coude", 1): {
        "effet": "La main subit −20 ; toute action de force du bras subit −10.",
        "ps": "Ni saignement ni Inconscience : aucun geste d'urgence ne s'impose.",
        "tr": "Repos et immobilisation : lève les malus de −20 et −10.",
    },
    ("Pied", 2): {
        "nom": "Entorse grave de la cheville, ligaments déchirés",
        "effet": "À terre. −30 aux déplacements, vitesse réduite de moitié.",
        "ps": "Ni saignement ni Inconscience : relève du traitement.",
        "tr": "Repos : lève le malus de −30 et met fin à l'état À terre.",
    },
    ("Pied", 3): {
        "nom": "Fracture ouverte des métatarses, os saillant",
        "effet": "Saignement 5 PV par tour. Étourdi 1 tour. −60 aux déplacements.",
        "ps": "Comprime la plaie : retire le saignement.",
        "tr": "Réduit les fractures : retire le saignement, met fin à l'Étourdi et lève le malus de −60.",
    },
    ("Main", 4): {
        "nom": "Main broyée, plusieurs doigts sectionnés",
        "effet": "Saignement 10 PV par tour. Perte définitive des doigts. Main restante hors d'usage de façon permanente.",
        "ps": "Garrot au poignet : retire le saignement.",
        "tr": "Chirurgie : retire le saignement, mais la perte des doigts reste définitive.",
    },
    ("Main", 5): {
        "nom": "Main arrachée ou tranchée au poignet",
        "effet": "Saignement 15 PV par tour. Perte définitive de la main. À terre et Inconscience.",
        "ps": "Garrot : retire le saignement et met fin à l'Inconscience.",
        "tr": "Parage du moignon : retire le saignement et met fin à l'état À terre, mais la perte reste définitive.",
    },
    ("Poignet", 5): {
        "nom": "Poignet tranché, main séparée du bras",
        "effet": "La main est sectionnée et perdue définitivement. Saignement 15 PV par tour.",
        "ps": "Garrot à l'avant-bras : retire le saignement.",
        "tr": "Régularise le moignon : retire le saignement, mais la perte de la main reste définitive.",
    },
    ("Bras", 5): {
        "effet": "Perte définitive du membre. Saignement 20 PV par tour. À terre et Étourdi un tour.",
        "ps": "Garrot à la racine du bras : retire le saignement.",
        "tr": "Régularise le moignon : retire le saignement, met fin à l'état À terre et à l'Étourdi, mais la perte reste définitive.",
    },
    ("Mollet", 2): {
        "nom": "Lacération profonde du mollet entaillant le faisceau musculaire",
        "effet": "Paralysie partielle : vitesse réduite de moitié, −40 aux actions d'appui. Saignement 5 PV par tour.",
        "ps": "Comprime la plaie : retire le saignement.",
        "tr": "Suture le muscle : met fin à la Paralysie partielle et lève les malus.",
    },
    ("Mollet", 3): {
        "effet": "Paralysie partielle, course et saut impossibles, −60 aux actions d'appui. À terre. Saignement 5 PV par tour.",
        "ps": "Attelle et comprime la plaie : retire le saignement.",
        "tr": "Suture le tendon : met fin à la Paralysie partielle et à l'état À terre, et lève les malus.",
    },
}

n = 0
for (zone, degre), fix in PATCH.items():
    e = next(x for x in ds[zone] if x["degre"] == degre)
    if "nom" in fix:
        e["nom"] = fix["nom"]
    e["effet"] = fix["effet"]
    e["premiersSecours"]["description"] = fix["ps"]
    e["traitement"]["description"] = fix["tr"]
    n += 1

P.write_text(json.dumps(ds, ensure_ascii=False, indent=1), encoding="utf-8")
print("OK -", n, "entrées corrigées")
