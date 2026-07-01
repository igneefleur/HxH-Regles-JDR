# -*- coding: utf-8 -*-
"""Deux niveaux de classement des compétences :
  - Piliers (Physique, Mental, Social) : la grande nature de l'action.
  - Groupes (Vocal) : un affinage.
Met à jour les entrées détaillées (<p class="groupes">) avec « Piliers : … » puis « Groupes : … »
(la ligne Groupes n'apparaît que s'il y a un groupe). Réécrit la section « Piliers et groupes ».
Lancer ensuite recap_competences.py pour régénérer la table.
Usage : python scripts/pilier_competences.py"""
import re
from pathlib import Path

p = Path("docs/content/regles/personnage/competences.md")
lines = p.read_text(encoding="utf-8").splitlines()

PILIER_DEFAULT = {
    "Champ Martial": "Physique",
    "Champ Athlétique": "Physique",
    "Champ de Vigueur": "Physique",
    "Champ Social": "Social",
    "Champ Intellectuel": "Mental",
    "Champ de Subsistance": "Physique",
    "Champ Sensoriel": "Physique",
    "Champ Technique": "Mental",
    "Champ Furtif": "Physique",
    "Champ Créatif": "Physique",
}
PILIER_OVERRIDE = {
    "Résistance Mentale": "Mental",
    "Médecine": "Physique, Mental",
    "Survie": "Physique, Mental",
    "Pistage": "Physique, Mental",
    "Mécanique": "Physique, Mental",
    "Électronique": "Physique, Mental",
    "Chimie": "Physique, Mental",
    "Pharmacologie": "Physique, Mental",
    "Explosifs": "Physique, Mental",
    "Conduite": "Physique",
    "Navigation": "Physique",
    "Pilotage": "Physique",
    "Équitation": "Physique",
    "Filature": "Physique, Mental",
    "Pièges": "Physique, Mental",
    "Écriture": "Mental",
    "Conte / Narration": "Social",
    "Théâtre": "Social, Physique",
    "Musique & chant": "Physique, Social",
    "Rhétorique": "Social, Mental",
}
VOCAL = {
    "Persuasion", "Rhétorique", "Négociation", "Tromperie", "Séduction", "Intimidation",
    "Interrogatoire", "Commandement", "Pédagogie", "Relation", "Étiquette",
    "Conte / Narration", "Théâtre", "Musique & chant",
}
MOUVEMENT = {"Course", "Saut", "Natation", "Escalade"}

field = None
changed = 0
for idx, l in enumerate(lines):
    if l.startswith("## Champ "):
        field = l[3:].strip()
    elif l.startswith("#### "):
        nom = l[5:].strip()
        pilier = PILIER_OVERRIDE.get(nom, PILIER_DEFAULT.get(field, "Physique"))
        groupe = ", ".join(g for g, s in (("Vocal", VOCAL), ("Mouvement", MOUVEMENT)) if nom in s)
        for k in range(idx + 1, min(idx + 6, len(lines))):
            if 'class="groupes"' in lines[k]:
                m = re.search(r"Caractéristique : (.+?)<br>", lines[k])
                carac = m.group(1)
                inner = f"Caractéristique : {carac}<br>Piliers : {pilier}"
                if groupe:
                    inner += f"<br>Groupes : {groupe}"
                lines[k] = re.sub(r'(<p class="groupes">).*(</p>)',
                                  lambda mm: mm.group(1) + inner + mm.group(2), lines[k])
                changed += 1
                break

# Réécriture de la section (ex-« Les groupes »).
i0 = next(i for i, l in enumerate(lines) if l.strip() in ("## Les groupes", "## Piliers et groupes"))
i1 = next(i for i in range(i0 + 1, len(lines)) if lines[i].startswith("## ") and i != i0)
newsec = [
    "## Piliers et groupes", "",
    "Chaque compétence relève d'un ou plusieurs piliers, et peut en plus porter un groupe. Un effet peut frapper un pilier ou un groupe entier d'un coup (« −X aux compétences Physique ») au lieu de les énumérer une à une.", "",
    "Les **piliers** sont les trois grandes natures d'une action :", "",
    "- **Physique** : ce qui sollicite le corps et ses gestes.",
    "- **Mental** : ce qui demande de savoir, de raisonner ou de se concentrer.",
    "- **Social** : ce qui agit sur autrui.", "",
    "Les **groupes** affinent ce découpage :", "",
    "- **Vocal** : ce qui passe par la voix et la parole.",
    "- **Mouvement** : ce qui consiste à se déplacer.", "",
]
lines = lines[:i0] + newsec + lines[i1:]

p.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
print("OK -", changed, "compétences (piliers + groupes)")
