# -*- coding: utf-8 -*-
"""L'escalade a fait dériver la zone Bras vers le coude (doublon de la zone Coude).
On réécrit le Bras comme une plaie du bras/de l'avant-bras qui s'aggrave (muscle ->
muscle+tendon -> fracture de l'humérus -> broyé -> sectionné), distincte du coude.
Usage : python scripts/patch_bras.py"""
import json
from pathlib import Path

P = Path("scripts/blessures_audit.json")
ds = json.loads(P.read_text(encoding="utf-8"))

ds["Bras"] = [
    {
        "degre": 1,
        "nom": "Entaille musculaire du bras",
        "effet": "Saignement 5 PV par tour. −10 à toute action de ce bras.",
        "premiersSecours": {"possible": True, "difficulte": "Moyenne",
            "description": "Comprime et bande la plaie du bras : retire le saignement."},
        "traitement": {"mode": "repos", "difficulte": "", "jours": 10,
            "description": "Repos et soins de la plaie : le muscle cicatrise, retire le saignement et lève le malus de −10."},
    },
    {
        "degre": 2,
        "nom": "Lacération profonde du bras, muscle et tendon tranchés",
        "effet": "Saignement 10 PV par tour. −20 à toute action de ce bras ; la cible lâche ce qu'elle tient de cette main.",
        "premiersSecours": {"possible": True, "difficulte": "Difficile",
            "description": "Comprime fermement et bande le bras : retire le saignement."},
        "traitement": {"mode": "chirurgie_repos", "difficulte": "Difficile", "jours": 21,
            "description": "Suture le muscle et le tendon, puis cicatrisation : retire le saignement et lève le malus de −20."},
    },
    {
        "degre": 3,
        "nom": "Fracture ouverte de l'humérus",
        "effet": "Saignement 10 PV par tour. Bras hors d'usage. Étourdi 1 tour sous le choc.",
        "premiersSecours": {"possible": True, "difficulte": "Difficile",
            "description": "Pose un garrot et attelle le membre fracturé : retire le saignement."},
        "traitement": {"mode": "chirurgie_repos", "difficulte": "Très difficile", "jours": 45,
            "description": "Réduit et fixe l'humérus, puis consolidation : retire le saignement, met fin à l'Étourdi et rend l'usage du bras."},
    },
    {
        "degre": 4,
        "nom": "Bras broyé, os et chairs écrasés",
        "effet": "Saignement 15 PV par tour. Bras hors d'usage. Paralysie partielle du membre. À terre.",
        "premiersSecours": {"possible": True, "difficulte": "Très difficile",
            "description": "Pose un garrot et comprime les chairs broyées : retire le saignement."},
        "traitement": {"mode": "chirurgie_repos", "difficulte": "Absurde", "jours": 90,
            "description": "Reconstruit l'os et les chairs du bras, puis longue convalescence : retire le saignement, met fin à la Paralysie partielle et à l'état À terre et rend l'usage du bras."},
    },
    {
        "degre": 5,
        "nom": "Bras sectionné ou arraché",
        "effet": "Saignement 20 PV par tour. Perte définitive du bras. À terre et Étourdi un tour.",
        "premiersSecours": {"possible": True, "difficulte": "Absurde",
            "description": "Pose un garrot d'urgence à la racine du bras : retire le saignement et écarte la mort imminente."},
        "traitement": {"mode": "chirurgie_repos", "difficulte": "Absurde", "jours": 90,
            "description": "Régularise et referme le moignon, puis cicatrisation : retire le saignement et met fin à l'état À terre, mais la perte du bras reste définitive."},
    },
]

P.write_text(json.dumps(ds, ensure_ascii=False, indent=1), encoding="utf-8")
print("OK - Bras reecrit (zone bras distincte du coude)")
