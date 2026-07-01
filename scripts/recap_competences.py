# -*- coding: utf-8 -*-
"""Remplace le bloc .comp-recap par un tableau par champ (titré par <caption>)."""
import re
from pathlib import Path

p = Path("docs/content/regles/personnage/competences.md")
lines = p.read_text(encoding="utf-8").splitlines()

# --- Extraire les compétences depuis les modules ---
rows = []          # (champ, nom, carac, piliers, groupes)
field = None
for idx, l in enumerate(lines):
    if l.startswith("## Champ "):
        field = l[3:].strip()
    elif l.startswith("#### "):
        nom = l[5:].strip()
        for k in range(idx + 1, min(idx + 6, len(lines))):
            if 'class="groupes"' in lines[k]:
                m = re.search(r"Caractéristique : (.+?)<br>Piliers : (.+?)(?:<br>Groupes : (.+?))?</p>", lines[k])
                rows.append((field, nom, m.group(1), m.group(2), m.group(3) or ""))
                break

champs = list(dict.fromkeys(c for c, *_ in rows))

# --- Construire le nouveau bloc : un tableau par champ ---
blk = ['<div class="comp-recap" markdown>', ""]
for champ in champs:
    blk.append(f"### {champ}")
    blk.append("")
    blk.append("<table>")
    blk.append("<thead><tr><th>Compétence</th><th>Caractéristique</th><th>Piliers</th><th>Groupes</th></tr></thead>")
    blk.append("<tbody>")
    for c, nom, carac, piliers, groupes in rows:
        if c == champ:
            blk.append(f"<tr><td>{nom}</td><td>{carac}</td><td>{piliers}</td><td>{groupes}</td></tr>")
    blk.append("</tbody>")
    blk.append("</table>")
    blk.append("")
blk.append("</div>")

# --- Remplacer l'ancien bloc .comp-recap ---
i0 = next(i for i, l in enumerate(lines) if l.strip() == '<div class="comp-recap" markdown>')
i1 = next(i for i in range(i0 + 1, len(lines)) if lines[i].strip() == "</div>")
new_lines = lines[:i0] + blk + lines[i1 + 1:]
p.write_text("\n".join(new_lines).rstrip() + "\n", encoding="utf-8")
print("OK — tableaux:", len(champs))
