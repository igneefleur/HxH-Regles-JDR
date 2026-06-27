# -*- coding: utf-8 -*-
"""Remplace les anciens groupes des compétences par 3 groupes : Physique, Vocal, Réflexion.
Met à jour les entrées détaillées (<p class="groupes">) et réécrit la section « Les groupes ».
Lancer ensuite recap_competences.py pour régénérer la table récapitulative.
Usage : python scripts/regroup_competences.py"""
import re
from pathlib import Path

p = Path("docs/content/livre/competences.md")
lines = p.read_text(encoding="utf-8").splitlines()

# Groupe par défaut selon le champ.
FIELD_DEFAULT = {
    "Champ Martial": "Physique",
    "Champ Athlétique": "Physique",
    "Champ de Vigueur": "Physique",
    "Champ Social": "Vocal",
    "Champ Intellectuel": "Réflexion",
    "Champ de Subsistance": "Physique",
    "Champ Sensoriel": "aucun",
    "Champ Technique": "Réflexion",
    "Champ Furtif": "Physique",
    "Champ Créatif": "Physique",
}
# Exceptions par compétence (corps + voix + réflexion possibles ensemble).
OVERRIDE = {
    "Résistance Mentale": "Réflexion",
    "Rhétorique": "Vocal, Réflexion",
    "Style": "aucun",
    "Médecine": "Physique, Réflexion",
    "Survie": "Physique, Réflexion",
    "Pistage": "Physique, Réflexion",
    "Mécanique": "Physique, Réflexion",
    "Électronique": "Physique, Réflexion",
    "Chimie": "Physique, Réflexion",
    "Pharmacologie": "Physique, Réflexion",
    "Explosifs": "Physique, Réflexion",
    "Conduite": "Physique",
    "Navigation": "Physique",
    "Pilotage": "Physique",
    "Équitation": "Physique",
    "Filature": "Physique, Réflexion",
    "Pièges": "Physique, Réflexion",
    "Écriture": "Réflexion",
    "Conte / Narration": "Vocal",
    "Musique & chant": "Physique, Vocal",
    "Théâtre": "Vocal, Physique",
    "Peinture & dessin": "Physique, Réflexion",
}

field = None
changed = 0
for idx, l in enumerate(lines):
    if l.startswith("## Champ "):
        field = l[3:].strip()
    elif l.startswith("#### "):
        nom = l[5:].strip()
        grp = OVERRIDE.get(nom, FIELD_DEFAULT.get(field, "aucun"))
        for k in range(idx + 1, min(idx + 6, len(lines))):
            if 'class="groupes"' in lines[k]:
                lines[k] = re.sub(r"(Groupes : ).+?(</p>)", lambda m: m.group(1) + grp + m.group(2), lines[k])
                changed += 1
                break

# Réécriture de la section « Les groupes ».
i0 = next(i for i, l in enumerate(lines) if l.strip() == "## Les groupes")
i1 = next(i for i in range(i0 + 1, len(lines)) if lines[i].startswith("## ") and lines[i].strip() != "## Les groupes")
newsec = [
    "## Les groupes", "",
    "Les groupes sont des outils de modificateur : un effet peut frapper un groupe entier d'un coup (« −X à toutes les compétences du groupe Physique ») au lieu d'énumérer les compétences une à une. Une compétence peut appartenir à plusieurs groupes, ou à aucun.", "",
    "- **Physique** : les compétences qui sollicitent le corps et ses gestes.",
    "- **Vocal** : les compétences qui passent par la voix et la parole.",
    "- **Réflexion** : les compétences qui exigent une réflexion poussée.", "",
]
lines = lines[:i0] + newsec + lines[i1:]

p.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
print("OK -", changed, "compétences regroupées")
