# -*- coding: utf-8 -*-
"""Réécriture propre des descriptions de soins (Main / Abdomen / Torse) que des agents
avaient noyées dans la phrase de jet. Forme « geste narratif. Règle. », sans jamais citer
le jet (auto-affiché). Les champs structurés (difficulté/mode/jours) sont déjà corrects.
Usage : python scripts/patch_descriptions.py"""
import json
from pathlib import Path

P = Path("scripts/blessures_audit.json")
ds = json.loads(P.read_text(encoding="utf-8"))

# clé "Zone|degré|ps|tr" -> description corrigée
FIX = {
    "Main|1|ps": "Le soignant lave et bande les doigts meurtris. Retire le saignement.",
    "Main|2|ps": "Le soignant comprime la plaie et serre un garrot au poignet. Retire le saignement.",
    "Main|2|tr": "Une opération suture un à un les tendons fléchisseurs tranchés, puis une immobilisation prolongée les laisse se ressouder. Retire le saignement et lève le malus de −40.",
    "Main|3|ps": "Le soignant comprime les plaies et pose une attelle rigide. Retire le saignement.",
    "Main|3|tr": "Une opération redresse les fractures et reconstruit les articulations broyées, suivie d'une longue consolidation osseuse. Retire le saignement et rend l'usage de la main.",
    "Main|4|ps": "Le soignant pose un garrot serré au poignet pour endiguer l'hémorragie. Retire le saignement.",
    "Main|4|tr": "Une opération pare les chairs broyées et referme la main mutilée, suivie d'une longue convalescence. Retire le saignement et retire l'état Inconscient, mais la perte des doigts reste définitive.",
    "Main|5|ps": "Le soignant pose un garrot serré sur le moignon pour stopper le flot de sang. Retire le saignement.",
    "Main|5|tr": "Une opération pare et referme proprement le moignon du poignet, suivie d'une très longue convalescence. Retire le saignement et retire l'état Inconscient, mais la perte de la main reste définitive.",

    "Abdomen|2|ps": "Le secouriste comprime la plaie du flanc et pose un pansement serré pour endiguer l'écoulement. Retire le saignement.",
    "Abdomen|2|tr": "Le chirurgien suture les couches de muscle déchiré et referme la peau du flanc, puis la cible observe une convalescence. Retire le saignement et lève le malus de −20.",
    "Abdomen|3|ps": "Le secouriste comprime la plaie et maintient les entrailles à l'intérieur de la cavité pour stopper l'hémorragie. Retire le saignement.",
    "Abdomen|3|tr": "Le chirurgien referme une à une les couches de la paroi abdominale tranchée et remet les entrailles en place, puis la cible observe une longue convalescence. Retire le saignement et retire l'état Étourdi.",
    "Abdomen|4|ps": "Le secouriste comprime la cavité ouverte et tamponne les organes perforés en urgence pour contenir l'hémorragie. Retire le saignement.",
    "Abdomen|4|tr": "Le chirurgien suture les organes perforés, recoud les intestins déchirés et reconstitue la paroi du ventre, puis la cible observe une très longue convalescence. Retire le saignement, retire l'état Immobilisé et retire l'état Inconscient.",
    "Abdomen|5|ps": "Le secouriste comprime l'aorte abdominale à mains nues et maintient la cavité fermée pour tenter d'endiguer le flot. Retire le saignement.",
    "Abdomen|5|tr": "Le chirurgien réalise l'hémostase de l'aorte, retire les organes détruits et reconstruit la paroi en urgence, puis la cible observe une très longue convalescence. Le rétablissement des organes vitaux arrachés ne peut être réalisé sans organes de remplacement viables. Retire le saignement et retire l'état Inconscient, mais la perte des organes arrachés reste définitive.",

    "Torse|3|ps": "Le sauveteur comprime la plaie à pleines mains et applique un pansement compressif sur le flanc. Retire le saignement.",
    "Torse|3|tr": "Le chirurgien suture la plaie et répare la paroi thoracique déchirée, puis impose un repos de convalescence. Retire le saignement et lève le malus de −30.",
    "Torse|4|ps": "Le sauveteur draine le foyer hémorragique et redresse le volet thoracique effondré pour rétablir le souffle. Retire le saignement.",
    "Torse|4|tr": "Le chirurgien suture le poumon perforé et reconstruit le volet thoracique, puis impose une longue convalescence. Retire le saignement, retire l'état Inconscient, lève le malus de −40 et rend l'usage du torse.",
    "Torse|5|ps": "Le sauveteur draine l'hémorragie massive et s'acharne à rétablir les échanges gazeux du poumon valide. Retire le saignement.",
    "Torse|5|tr": "Le chirurgien reconstruit la cage thoracique et referme la lésion au prix d'une opération extrême, puis impose une très longue convalescence. Le poumon détruit ne peut être restauré sans un poumon de remplacement viable. Retire le saignement et retire l'état Inconscient, mais la perte du poumon et le malus de −50 restent définitifs.",
}

n = 0
for key, desc in FIX.items():
    zone, degre, fld = key.split("|")
    e = next(x for x in ds[zone] if x["degre"] == int(degre))
    target = e["premiersSecours"] if fld == "ps" else e["traitement"]
    target["description"] = desc
    n += 1

P.write_text(json.dumps(ds, ensure_ascii=False, indent=1), encoding="utf-8")
print("OK -", n, "descriptions réécrites")
