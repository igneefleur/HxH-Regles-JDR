# -*- coding: utf-8 -*-
"""Dans competences.md : retire la classe 'palier' (tableaux verts classiques) et
supprime les paliers au-dessus de Surhumaine (Prodigieuse, Insurmontable, Irréel)
des échelles par compétence. N'affecte que les tableaux class="palier"."""
import re
from pathlib import Path

SRC = Path("docs/content/livre/competences.md")
DROP = ("Prodigieuse", "Insurmontable", "Irréel")
drop_re = re.compile(r"^<tr><td>(" + "|".join(DROP) + r")</td>")

lines = SRC.read_text(encoding="utf-8").splitlines()
out = []
inside = False
for line in lines:
    if line.strip() == '<table class="palier">':
        out.append("<table>")          # tableau classique (vert)
        inside = True
        continue
    if inside and line.strip() == "</table>":
        inside = False
        out.append(line)
        continue
    if inside and drop_re.match(line.strip()):
        continue                        # on saute les paliers au-dessus de Surhumaine
    out.append(line)

SRC.write_text("\n".join(out) + "\n", encoding="utf-8")
print("OK")
