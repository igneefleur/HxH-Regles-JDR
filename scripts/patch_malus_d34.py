# -*- coding: utf-8 -*-
"""Comble les creux de malus d'action aux degrés 3-4 (mêmes que le degré 5) : la partie devenait
« hors d'usage »/perdue et le malus chiffré tombait à 0. On ajoute un malus d'action global
(= pic de la zone, levé par le traitement) pour une montée monotone D1->D5 sans creux.
N'ajoute que des malus, n'en baisse aucun.
Usage : python scripts/patch_malus_d34.py"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
P = Path("scripts/blessures_audit.json")
ds = json.loads(P.read_text(encoding="utf-8"))

ANCRE = "Au début de son prochain tour, le blessé doit réussir"

# (zone, degré) -> (malus global Y, traitement réécrit avec « lève le malus de −Y »)
FIX = {
    ("Cœur", 4): (50, "Le médecin pratique une opération cardiaque pour refermer la perforation du ventricule. Retire le saignement, lève le malus de −50 et retire l'état Inconscient."),
    ("Aine", 4): (45, "Le médecin répare l'artère fémorale et suture le nerf crural par microchirurgie. Retire le saignement, lève le malus de −45, retire l'état Inconscient, retire l'état À terre, retire l'état Paralysie partielle et rend l'usage de la jambe."),
    ("Pied", 4): (45, "Le médecin reconstruit le tarse et suture les nerfs et les vaisseaux. Rend l'usage du pied, lève le malus de −45, retire l'état Paralysie partielle, retire l'état À terre et retire l'état Inconscient."),
    ("Genou", 4): (40, "Le médecin reconstruit l'articulation broyée et répare le nerf sectionné, puis mène une rééducation. Rend l'usage de la jambe, lève le malus de −40, retire l'état Paralysie partielle, retire l'état À terre et retire l'état Inconscient."),
    ("Main", 3): (40, "Le médecin redresse les fractures et reconstruit les articulations broyées, suivi d'une consolidation osseuse. Retire le saignement, lève le malus de −40 et rend l'usage de la main."),
    ("Main", 4): (40, "Le médecin pare les chairs broyées et referme la main mutilée, suivi d'une convalescence. Retire le saignement, lève le malus de −40 et retire l'état Inconscient. La perte des doigts reste définitive."),
    ("Poignet", 3): (30, "Le médecin suture les vaisseaux et répare les nerfs sectionnés, puis une convalescence suit. Retire le saignement, lève le malus de −30 et retire l'état Paralysie partielle."),
    ("Poignet", 4): (30, "Le médecin reconstruit l'articulation et greffe les nerfs arrachés, puis une rééducation suit. Retire le saignement, lève le malus de −30, retire l'état Paralysie totale, retire l'état Inconscient et rend l'usage de la main."),
    ("Épaule", 3): (40, "Le médecin fixe les os fracturés et suture les tendons arrachés, puis impose une convalescence prolongée. Retire le saignement, lève le malus de −40, retire l'état Étourdi et rend l'usage du membre."),
    ("Épaule", 4): (40, "Le médecin suture les nerfs et les vaisseaux sectionnés, puis impose une longue convalescence. Retire le saignement, lève le malus de −40 et retire l'état Inconscient, mais l'état Paralysie totale et le malus permanent de −2 à la Force, à l'Agilité et à la Dextérité restent définitifs."),
    ("Abdomen", 3): (20, "Le médecin referme les couches de la paroi abdominale tranchée et remet les entrailles en place. Retire le saignement, lève le malus de −20 et retire l'état Étourdi."),
    ("Abdomen", 4): (20, "Le médecin suture les organes perforés, recoud les intestins déchirés et reconstitue la paroi du ventre, puis le blessé observe une très longue convalescence. Retire le saignement, lève le malus de −20, retire l'état Immobilisé et retire l'état Inconscient."),
    ("Bras", 3): (20, "Le médecin réduit et fixe l'humérus, puis laisse le membre consolider. Retire le saignement, lève le malus de −20, retire l'état Étourdi et rend l'usage du bras."),
    ("Bras", 4): (20, "Le médecin reconstruit l'os et les chairs du bras au fil d'une convalescence. Retire le saignement, lève le malus de −20, retire l'état Paralysie partielle, retire l'état Inconscient et rend l'usage du bras."),
    ("Cuisse", 3): (20, "Le médecin réduit la fracture et fixe le fémur, puis une immobilisation laisse l'os se ressouder. Retire le saignement, lève le malus de −20, retire l'état À terre et rend l'usage de la jambe."),
    ("Cuisse", 4): (20, "Le médecin suture l'artère fémorale et consolide le fémur ouvert, puis une convalescence accompagne la guérison. Retire le saignement, lève le malus de −20, retire l'état Inconscient, retire l'état À terre et rend l'usage du membre."),
}

n = 0
for (zone, degre), (y, tr) in FIX.items():
    e = next(x for x in ds[zone] if x["degre"] == degre)
    clause = f"Il subit en outre −{y} à toute action."
    if ANCRE in e["effet"]:
        e["effet"] = e["effet"].replace(ANCRE, f"{clause} {ANCRE}")
    else:
        e["effet"] = e["effet"].rstrip() + " " + clause
    e["traitement"]["description"] = tr
    n += 1

P.write_text(json.dumps(ds, ensure_ascii=False, indent=1), encoding="utf-8")
print("OK -", n, "entrées D3-D4 dotées d'un malus d'action global")
