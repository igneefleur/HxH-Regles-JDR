# -*- coding: utf-8 -*-
"""Retire les tableaux d'échelle de difficulté (Difficulté | Exemple) des compétences
du Champ Martial uniquement."""
from pathlib import Path

SRC = Path("docs/content/regles/personnage/competences.md")
lines = SRC.read_text(encoding="utf-8").splitlines()

start = next(i for i, l in enumerate(lines) if l.strip() == "## Champ Martial")
end = next(i for i, l in enumerate(lines) if l.strip() == "## Champ Athlétique")

out = []
i = 0
removed = 0
while i < len(lines):
    in_martial = start <= i < end
    if (in_martial and lines[i].strip() == "<table>"
            and i + 1 < len(lines)
            and "Difficulté</th><th>Exemple" in lines[i + 1]):
        # saute jusqu'à </table>
        while i < len(lines) and lines[i].strip() != "</table>":
            i += 1
        i += 1  # passe </table>
        if i < len(lines) and lines[i].strip() == "":
            i += 1  # et la ligne vide suivante
        removed += 1
        continue
    out.append(lines[i])
    i += 1

SRC.write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"Tableaux retirés du Champ Martial : {removed}")
