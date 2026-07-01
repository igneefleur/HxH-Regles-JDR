# -*- coding: utf-8 -*-
"""Ajoute une colonne 'Classe' (classes chevauchantes, façon Anima) aux tables d'armes.
Usage : python scripts/armes_add_classe.py"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
ARMES = "docs/content/regles/combat/armes.md"

CLASSES = {
    "Dague": "Arme courte",
    "Katar": "Arme courte",
    "Épée courte": "Épée, Arme courte",
    "Épée longue": "Épée, Deux mains",
    "Épée à deux mains": "Épée, Deux mains",
    "Sabre": "Épée",
    "Rapière": "Épée",
    "Falchion": "Épée",
    "Macuahuitl": "Épée, Deux mains",
    "Hache à une main": "Hache",
    "Hache à deux mains": "Hache, Deux mains",
    "Gourdin / matraque": "Masse",
    "Masse d'armes": "Masse",
    "Marteau de guerre": "Masse",
    "Masse lourde": "Masse, Deux mains",
    "Fléau d'armes": "Masse, Corde",
    "Arme articulée (nunchaku)": "Corde",
    "Chaîne lestée": "Corde",
    "Kusarigama": "Corde, Arme courte",
    "Fouet": "Corde",
    "Lance": "Hast",
    "Pique": "Hast, Deux mains",
    "Hallebarde": "Hast, Deux mains",
    "Glaive d'hast": "Hast, Deux mains",
    "Trident / fourche": "Hast",
    "Arme de capture": "Hast, Corde",
    "Bâton": "Hast",
    "Javelot": "Hast, Jet",
    "Projectile léger de jet": "Arme courte, Jet",
    "Hache de jet": "Hache, Jet",
    "Boomerang": "Jet",
    "Arme enchevêtrante": "Corde, Jet",
    "Fronde": "Projectile",
    "Sarbacane": "Projectile",
    "Arc court": "Projectile",
    "Arc long": "Projectile",
    "Arc composite": "Projectile",
    "Arc à poulies": "Projectile",
    "Arbalète de poing": "Projectile",
    "Arbalète légère": "Projectile",
    "Arbalète lourde": "Projectile",
    "Arbalète à chargeur": "Projectile",
    "Pistolet à poudre noire": "Arme à feu",
    "Mousquet": "Arme à feu",
    "Tromblon": "Arme à feu",
    "Pistolet semi-auto": "Arme à feu",
    "Revolver": "Arme à feu",
    "Derringer": "Arme à feu",
    "Derringer 4 canons": "Arme à feu",
    "Pistolet-mitrailleur": "Arme à feu",
    "Fusil d'assaut": "Arme à feu",
    "Fusil de combat": "Arme à feu",
    "Fusil de précision": "Arme à feu",
    "Fusil anti-matériel": "Arme à feu",
    "Fusil à pompe": "Arme à feu",
    "Fusil à canon double": "Arme à feu",
    "Carabine civile": "Arme à feu",
    "Mitrailleuse légère": "Arme à feu",
    "Grenade à main": "Arme lourde",
    "Lance-grenades": "Arme lourde",
    "Lance-roquettes": "Arme lourde",
    "Charge explosive": "Arme lourde",
    "Lance-flammes": "Arme lourde",
    "Arme à impulsion électrique": "Arme à feu",
    "Lanceur à létalité réduite": "Arme à feu",
    "Agent chimique": "Arme lourde",
    "Arme de poing renforcée": "Arme courte, Mains nues",
    "Griffes": "Arme courte, Mains nues",
    "Faucille de combat": "Arme courte",
    "Sai / Jutte": "Arme courte",
    "Éventail de fer": "Arme courte",
    "Crochets chinois": "Arme courte",
    "Bouclier offensif": "Bouclier",
    "Garrot": "Corde, Deux mains",
}

lines = open(ARMES, encoding="utf-8").read().split("\n")
out, state, missing, done = [], None, [], 0
for line in lines:
    s = line.strip()
    if s.startswith("| Arme | AM | Portée"):
        out.append(line.replace("| Arme |", "| Arme | Classe |", 1))
        state = "weap"
        continue
    if state == "weap":
        if s.startswith("|"):
            if set(s) <= set("|-: "):  # ligne séparatrice
                out.append(line.replace("|---|", "|---|---|", 1))
            else:
                parts = line.split("|")
                name = parts[1].strip()
                cls = CLASSES.get(name)
                if cls is None:
                    missing.append(name)
                    cls = ""
                else:
                    done += 1
                parts.insert(2, " " + cls + " ")
                out.append("|".join(parts))
            continue
        else:
            state = None
    out.append(line)

open(ARMES, "w", encoding="utf-8").write("\n".join(out))
print("armes classées :", done, "/", len(CLASSES))
if missing:
    print("NOMS NON MAPPÉS :", missing)
