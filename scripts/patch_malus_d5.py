# -*- coding: utf-8 -*-
"""Le degré 5 (le pire) n'avait aucun malus d'action chiffré (la zone était « perdue »/« hors
d'usage » sans pénalité globale). On ajoute à chaque degré 5 un malus d'action global = le PIC
d'action de la zone (douleur de choc qui handicape tout) : temporaire, levé par le traitement,
en plus de la perte permanente. Le malus culmine ainsi au degré 5.
Usage : python scripts/patch_malus_d5.py"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
P = Path("scripts/blessures_audit.json")
ds = json.loads(P.read_text(encoding="utf-8"))

PEAK = {"Œil": 50, "Cou": 40, "Tête": 50, "Coude": 50, "Cœur": 50, "Aine": 45, "Pied": 45,
        "Main": 40, "Genou": 40, "Poignet": 30, "Épaule": 40, "Abdomen": 20, "Bras": 20,
        "Cuisse": 20, "Mollet": 35, "Torse": 40}

# Traitements réécrits : ajout de « lève le malus de −Y » (le malus d'action est temporaire).
TR = {
    "Œil": "Le médecin retire la pointe et rétablit la circulation cérébrale, puis le blessé observe une très longue convalescence. Retire le saignement, lève le malus de −50 et retire l'état Inconscient, mais la perte de l'œil et le malus de −2 à l'Érudition, à la Logique et à l'Imagination restent définitifs.",
    "Cou": "Le médecin suture les vaisseaux et reconstruit le cou. Retire le saignement, lève le malus de −40 et retire l'état Inconscient, mais le Mutisme reste permanent.",
    "Tête": "Le médecin relève la boîte crânienne enfoncée et draine l'hématome, puis une très longue convalescence suit l'opération. Retire le saignement, lève le malus de −50 et retire l'état Inconscient, mais le malus permanent de −2 à l'Érudition, à la Logique et à l'Imagination reste définitif.",
    "Coude": "Le médecin ampute le membre, ligature les vaisseaux et referme le moignon, puis vient une longue convalescence. Retire le saignement, lève le malus de −50 et retire l'état Inconscient. La perte du bras reste définitive.",
    "Cœur": "Le médecin pratique une opération extrême, suivie d'une convalescence. Le traitement ne peut être réalisé sans un cœur de remplacement viable à transplanter. Retire le saignement, lève le malus de −50 et retire l'état Inconscient.",
    "Aine": "Le médecin procède à la désarticulation de la hanche, assure l'hémostase de la fémorale et referme le moignon. Retire le saignement, lève le malus de −45, retire l'état À terre et retire l'état Inconscient. La perte de la jambe reste définitive.",
    "Pied": "Le médecin régularise le moignon, ferme les vaisseaux et appareille le pied. Retire le saignement, lève le malus de −45, retire l'état Immobilisé, retire l'état À terre et retire l'état Inconscient. La perte du pied reste définitive.",
    "Main": "Le médecin pare et referme le moignon du poignet, suivi d'une convalescence. Retire le saignement, lève le malus de −40 et retire l'état Inconscient. La perte de la main reste définitive.",
    "Genou": "Le médecin régularise le moignon et ferme les vaisseaux, puis mène une convalescence. Retire le saignement, lève le malus de −40, retire l'état Immobilisé, retire l'état À terre et retire l'état Inconscient. La perte de la jambe reste définitive.",
    "Poignet": "Le médecin régularise et referme le moignon, puis une convalescence suit. Retire le saignement, lève le malus de −30 et retire l'état Inconscient. La perte de la main reste définitive.",
    "Épaule": "Le médecin procède à la désarticulation et à la fermeture chirurgicale du moignon à l'épaule, puis impose une longue convalescence. Retire le saignement, lève le malus de −40 et retire l'état Inconscient, mais la perte du bras reste définitive.",
    "Abdomen": "Le médecin réalise l'hémostase de l'aorte, retire les organes détruits et reconstruit la paroi, puis le blessé observe une très longue convalescence. Le rétablissement des organes vitaux arrachés est impossible sans organes de remplacement viables. Retire le saignement, lève le malus de −20 et retire l'état Inconscient, mais la perte des organes arrachés reste définitive.",
    "Bras": "Le médecin régularise et referme le moignon, puis laisse le bras cicatriser. Retire le saignement, lève le malus de −20 et retire l'état Inconscient, mais la perte du bras reste définitive.",
    "Cuisse": "Le médecin régularise le moignon et referme l'artère fémorale, puis une convalescence s'installe. Retire le saignement, lève le malus de −20 et retire l'état Inconscient. La perte de la jambe reste définitive.",
    "Mollet": "Le médecin régularise le moignon et assure l'hémostase des vaisseaux ouverts, puis une convalescence referme la plaie. Retire le saignement, lève le malus de −35, retire l'état À terre et retire l'état Inconscient. La perte de la jambe reste définitive.",
    "Torse": "Le médecin reconstruit la cage thoracique et referme la lésion, puis impose une convalescence. Le poumon détruit ne peut être restauré sans un poumon de remplacement viable. Retire le saignement, lève le malus de −40 et retire l'état Inconscient, mais la perte du poumon reste définitive.",
}

ANCRE = "Au début de son prochain tour, le blessé doit réussir"
n = 0
for zone, y in PEAK.items():
    e = next(x for x in ds[zone] if x["degre"] == 5)
    assert ANCRE in e["effet"], zone
    e["effet"] = e["effet"].replace(ANCRE, f"Il subit en outre −{y} à toute action. {ANCRE}")
    e["traitement"]["description"] = TR[zone]
    n += 1

P.write_text(json.dumps(ds, ensure_ascii=False, indent=1), encoding="utf-8")
print("OK -", n, "degrés 5 dotés d'un malus d'action global (pic de zone)")
