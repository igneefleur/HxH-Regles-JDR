# -*- coding: utf-8 -*-
"""Injecte les échelles de difficulté (résultats du workflow) dans competences.md.
Usage : python scripts/inject_palier.py <chemin_du_fichier_output_du_workflow>"""
import html
import json
import sys
from pathlib import Path

TIERS = ["Triviale", "Très facile", "Facile", "Moyenne", "Difficile", "Très difficile",
         "Absurde", "Quasi impossible", "Impossible", "Surhumaine", "Prodigieuse",
         "Insurmontable", "Irréel"]

SRC = Path("docs/content/livre/competences.md")
out_path = Path(sys.argv[1])

data = json.loads(out_path.read_text(encoding="utf-8"))
skills = data["result"]["skills"]

def table_lines(examples):
    rows = []
    for tier, ex in zip(TIERS, examples):
        ex = (ex or "").strip()
        cell = html.escape(ex, quote=False) if ex else ""
        rows.append(f"<tr><td>{tier}</td><td>{cell}</td></tr>")
    return ([
        '<table class="palier">',
        '<thead><tr><th>Difficulté</th><th>Exemple</th></tr></thead>',
        '<tbody>',
    ] + rows + ['</tbody>', '</table>'])

lines = SRC.read_text(encoding="utf-8").splitlines()

def inject(name, examples):
    """Insère le tableau dans le module #### name. Retourne True si fait."""
    for i, line in enumerate(lines):
        if line.strip() == f"#### {name}":
            # fin du module = prochain </div>
            d = next((j for j in range(i + 1, len(lines)) if lines[j].strip() == "</div>"), None)
            if d is None:
                return False
            # déjà un tableau ? on saute
            if any('class="palier"' in lines[j] for j in range(i, d)):
                return False
            block = table_lines(examples)
            lines[i:d] = lines[i:d] + block + [""]
            return True
    return False

done, missing = [], []
for s in skills:
    if inject(s["name"], s["examples"]):
        done.append(s["name"])
    else:
        missing.append(s["name"])

SRC.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Injectées : {len(done)} / {len(skills)}")
if missing:
    print("Non injectées (introuvables ou déjà présentes) :", ", ".join(missing))
