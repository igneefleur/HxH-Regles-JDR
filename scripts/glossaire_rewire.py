# -*- coding: utf-8 -*-
"""Régénère toutes les <figure> du glossaire depuis docs/assets/glossaire/_index.json
(image locale + lien de source), en se basant sur l'attribut alt de chaque figure.
À lancer après glossaire_fix_images.py. Usage : python scripts/glossaire_rewire.py"""
import json, re, sys
sys.stdout.reconfigure(encoding="utf-8")

GLOSS = "docs/includes/glossaire.md"
res = json.load(open("docs/assets/glossaire/_index.json", encoding="utf-8"))

LABEL2SLUG = {
    "téléphone": "telephone", "bouteille": "bouteille", "ordinateur": "ordinateur",
    "nouveau-né": "bebe", "sac de farine": "farine", "bowling": "bowling",
    "sac de ciment": "ciment", "valise": "valise", "enfant": "enfant",
    "saint-bernard": "saint-bernard", "personne": "personne", "adulte": "adulte",
    "réfrigérateur": "refrigerateur", "panda": "panda", "lion": "lion", "ours": "ours",
    "cheval": "cheval", "voiture": "voiture", "voitures": "voiture",
    "rhinocéros": "rhinoceros", "éléphant": "elephant", "autobus": "autobus",
    "semi-remorque": "semi-remorque", "char": "char", "locomotive": "locomotive",
    "baleine bleue": "baleine-bleue", "baleines": "baleine-bleue",
    "statue Liberté": "statue-liberte", "A380": "a380", "cargo": "cargo",
    "péniche": "peniche", "frégate": "fregate", "tour Eiffel": "tour-eiffel",
    "sous-marin": "sous-marin", "cuirassé": "cuirasse", "Titanic": "titanic",
    "paquebot": "paquebot", "porte-avions": "porte-avions",
    "porte-conteneurs": "porte-conteneurs", "supertanker": "supertanker",
    "gratte-ciel": "gratte-ciel", "pyramide": "pyramide", "barrage": "barrage",
    "colline": "colline", "montagne": "montagne", "petit navire": "navire",
    "ralenti": "escargot", "escargot": "escargot", "marche lente": "marche",
    "flânerie": "marche", "marche": "marche", "marche rapide": "marche",
    "footing": "footing", "jogging": "footing", "course": "course",
    "coureur": "course", "sprint": "sprint", "cycliste": "cycliste", "trot": "trot",
    "Bolt": "bolt", "galop": "galop", "lévrier": "levrier", "guépard": "guepard",
    "autoroute": "autoroute", "train": "train", "sport": "sport", "TGV": "tgv",
    "hélice": "helice", "avion": "avion", "mur du son": "jet", "chasseur": "jet",
    "avion-espion": "sr71", "Mach 2,5": "jet", "Mach 3,6": "jet",
    "hypersonique": "hypersonique", "Mach 7": "jet", "Mach 10": "hypersonique",
    "Mach 12": "hypersonique", "capsule": "capsule", "satellite": "satellite",
    "sonde": "sonde", "cosmos": "cosmos", "Netero": "netero",
}

text = open(GLOSS, encoding="utf-8").read()
n = [0]


def repl(m):
    label = m.group(1)
    info = res.get(LABEL2SLUG.get(label, ""))
    if not info:
        return m.group(0)
    n[0] += 1
    src = " — ".join(x for x in [info.get("artist"), info.get("lic")] if x)
    return ('<figure class="gcard-fig">\n'
            f'<img class="gcard-img" src="../../../assets/glossaire/{info["file"]}" alt="{label}" loading="lazy">\n'
            f'<figcaption><a href="{info["page"]}">{src}</a></figcaption>\n'
            '</figure>')


text = re.sub(r'<figure class="gcard-fig">\s*<img class="gcard-img" src="[^"]*" alt="([^"]+)"[^>]*>\s*'
              r'<figcaption>.*?</figcaption>\s*</figure>', repl, text, flags=re.S)
open(GLOSS, "w", encoding="utf-8").write(text)
print("figures régénérées :", n[0])
