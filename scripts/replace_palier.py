# -*- coding: utf-8 -*-
"""Remplace les tableaux .palier existants par des versions corrigées (résultats workflow).
Usage : python scripts/replace_palier.py <chemin_output_workflow>"""
import html
import json
import sys
from pathlib import Path

TIERS = ["Triviale", "Très facile", "Facile", "Moyenne", "Difficile", "Très difficile",
         "Absurde", "Quasi impossible", "Impossible", "Surhumaine", "Prodigieuse",
         "Insurmontable", "Irréel"]

SRC = Path("docs/content/regles/personnage/competences.md")
data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
skills = data["result"]["skills"]

def table_lines(examples):
    rows = []
    for tier, ex in zip(TIERS, examples):
        ex = (ex or "").strip()
        cell = html.escape(ex, quote=False) if ex else ""
        rows.append(f"<tr><td>{tier}</td><td>{cell}</td></tr>")
    return (['<table class="palier">',
             '<thead><tr><th>Difficulté</th><th>Exemple</th></tr></thead>',
             '<tbody>'] + rows + ['</tbody>', '</table>'])

lines = SRC.read_text(encoding="utf-8").splitlines()

def replace(name, examples):
    for i, line in enumerate(lines):
        if line.strip() == f"#### {name}":
            d = next((j for j in range(i + 1, len(lines)) if lines[j].strip() == "</div>"), None)
            if d is None:
                return False
            start = next((j for j in range(i, d) if 'class="palier"' in lines[j]), None)
            if start is None:
                return False
            end = next((j for j in range(start, d) if lines[j].strip() == "</table>"), None)
            if end is None:
                return False
            lines[start:end + 1] = table_lines(examples)
            return True
    return False

done, missing = [], []
for s in skills:
    (done if replace(s["name"], s["examples"]) else missing).append(s["name"])

SRC.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("Remplacées :", ", ".join(done) if done else "(aucune)")
if missing:
    print("Échecs :", ", ".join(missing))
