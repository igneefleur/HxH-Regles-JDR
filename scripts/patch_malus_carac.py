# -*- coding: utf-8 -*-
"""Corrige les pertes définitives exprimées en malus de caractéristiques :
- échelle des caractéristiques (0-30) -> malus petit (−2), pas −40 ;
- la perte de la voix (Cou D5) redevient un Mutisme permanent (pas un malus de Charisme/Présence) ;
- les organes vitaux (cœur, poumon, viscères) n'imposent aucun malus d'Endurance : la perte est
  déjà portée par la greffe obligatoire au traitement ;
- Abdomen D5 renommé pour éviter la redondance « éventré » (= é-ventre-é).
Usage : python scripts/patch_malus_carac.py"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
P = Path("scripts/blessures_audit.json")
ds = json.loads(P.read_text(encoding="utf-8"))

FIX = {
    ("Cou", 5): {
        "effet": "La gorge s'ouvre en grand et le cou est presque tranché, le sang inondant la poitrine en flots ininterrompus. Le blessé subit un Saignement de −25 PV et subit l'état Mutisme de façon permanente. Au début de son prochain tour, le blessé doit réussir un test d'Impassibilité Difficulté Impossible ou tomber Inconscient.",
        "tr": "Le médecin suture les vaisseaux et reconstruit le cou. Retire le saignement et retire l'état Inconscient, mais le Mutisme reste permanent.",
    },
    ("Tête", 5): {
        "effet": "La boîte crânienne cède et s'enfonce dans un fracas d'os, écrasant le cerveau sous les éclats. Le blessé subit un Saignement de −25 PV et −2 permanent à l'Érudition, à la Logique et à l'Imagination. Au début de son prochain tour, le blessé doit réussir un test d'Impassibilité Difficulté Impossible ou tomber Inconscient.",
        "tr": "Le médecin relève la boîte crânienne enfoncée et draine l'hématome, puis une très longue convalescence suit l'opération. Retire le saignement et retire l'état Inconscient, mais le malus permanent de −2 à l'Érudition, à la Logique et à l'Imagination reste définitif.",
    },
    ("Cœur", 5): {
        "effet": "Le cœur se rompt et se vide d'un seul coup, l'organe déchiré ne pouvant plus assurer sa fonction. Le blessé subit un Saignement de −30 PV et la perte définitive de son cœur. Au début de son prochain tour, le blessé doit réussir un test d'Impassibilité Difficulté Impossible ou tomber Inconscient.",
        "tr": "Le médecin pratique une opération extrême, suivie d'une convalescence. Le traitement ne peut être réalisé sans un cœur de remplacement viable à transplanter. Retire le saignement et retire l'état Inconscient.",
    },
    ("Abdomen", 5): {
        "nom": "Abdomen ouvert, organes vitaux arrachés",
        "effet": "L'abdomen se déchire et les organes vitaux qu'il abrite sont broyés et arrachés de la cavité. Le sang jaillit en flot continu et la conscience vacille. Le blessé subit un Saignement de −30 PV et la perte définitive des organes arrachés. Au début de son prochain tour, le blessé doit réussir un test d'Impassibilité Difficulté Impossible ou tomber Inconscient.",
        "tr": "Le médecin réalise l'hémostase de l'aorte, retire les organes détruits et reconstruit la paroi, puis le blessé observe une très longue convalescence. Le rétablissement des organes vitaux arrachés est impossible sans organes de remplacement viables. Retire le saignement et retire l'état Inconscient, mais la perte des organes arrachés reste définitive.",
    },
    ("Torse", 5): {
        "effet": "La cage thoracique cède sous le coup et un poumon est irrémédiablement broyé ; le souffle se fait rare et chaque râle projette du sang. Le blessé subit un Saignement de −15 PV et la perte définitive d'un poumon. Au début de son prochain tour, le blessé doit réussir un test d'Impassibilité Difficulté Absurde ou tomber Inconscient.",
        "tr": "Le médecin reconstruit la cage thoracique et referme la lésion, puis impose une convalescence. Le poumon détruit ne peut être restauré sans un poumon de remplacement viable. Retire le saignement et retire l'état Inconscient, mais la perte du poumon reste définitive.",
    },
    ("Œil", 5): {
        "effet": "La pointe s'enfonce à travers l'orbite et perce le crâne, fouillant les tissus profonds, et la douleur insoutenable terrasse le blessé. Le blessé subit un Saignement de −20 PV, la perte définitive de l'œil et une lésion cérébrale profonde qui inflige un malus permanent de −2 à l'Érudition, à la Logique et à l'Imagination. Au début de son prochain tour, le blessé doit réussir un test d'Impassibilité Difficulté Impossible ou tomber Inconscient.",
        "tr": "Le médecin retire la pointe et rétablit la circulation cérébrale, puis le blessé observe une très longue convalescence. Retire le saignement et retire l'état Inconscient, mais la perte de l'œil et le malus de −2 à l'Érudition, à la Logique et à l'Imagination restent définitifs.",
    },
    ("Épaule", 4): {
        "effet": "La lame tranche les nerfs du plexus brachial et ouvre les gros vaisseaux de l'aisselle, le sang jaillit et le bras du blessé ne répond plus à aucun ordre. Le blessé subit un Saignement de −15 PV et l'état Paralysie totale du bras, et les nerfs sectionnés lui infligent un malus permanent de −2 à la Force, à l'Agilité et à la Dextérité. Au début de son prochain tour, le blessé doit réussir un test d'Impassibilité Difficulté Très difficile ou tomber Inconscient.",
        "tr": "Le médecin suture les nerfs et les vaisseaux sectionnés, puis impose une longue convalescence. Retire le saignement et retire l'état Inconscient, mais l'état Paralysie totale et le malus permanent de −2 à la Force, à l'Agilité et à la Dextérité restent définitifs.",
    },
}

for (zone, degre), fix in FIX.items():
    e = next(x for x in ds[zone] if x["degre"] == degre)
    if "nom" in fix:
        e["nom"] = fix["nom"]
    e["effet"] = fix["effet"]
    e["traitement"]["description"] = fix["tr"]

P.write_text(json.dumps(ds, ensure_ascii=False, indent=1), encoding="utf-8")
print("OK -", len(FIX), "entrées corrigées (malus de caractéristique ramené à −2 ; Cou D5 -> Mutisme permanent)")
