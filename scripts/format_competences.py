# -*- coding: utf-8 -*-
"""Ré-aère competences.md : une ligne vide entre chaque bloc (requis par md_in_html)."""
from pathlib import Path

p = Path("docs/content/livre/competences.md")
lines = p.read_text(encoding="utf-8").splitlines()

start = next(i for i, l in enumerate(lines) if l.startswith("## Champ "))
last_div = max(i for i, l in enumerate(lines) if l.strip() == "</div>")

head = "\n".join(lines[:start]).rstrip() + "\n\n"
body_lines = [l.strip() for l in lines[start:last_div] if l.strip()]
body = "\n\n".join(body_lines)

p.write_text(head + body + "\n\n</div>\n", encoding="utf-8")
print("OK — keeps:", body.count('<div class="keep"'), "comps:", body.count('<div class="comp"'))
