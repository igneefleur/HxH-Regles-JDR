"""Hook MkDocs : extrait le barème des armes des règles et expose forge.json.

C'est le pont de synchronisation entre les règles (armes.md) et la Forge (page
« Forge », outil de création d'armes). Les coûts, les paliers et les descriptions
des pièces d'une arme sont écrits une seule fois, dans les fiches « Propriétés
obligatoires » et « Propriétés supplémentaires » d'armes.md ; ce hook les relit au
build et en fait un JSON que la Forge consomme. Une valeur changée dans les règles
se répercute donc dans l'outil : aucune double saisie, aucune dérive.

Seule la bibliothèque standard est utilisée (comme hooks/nen_atelier.py) : la CI
n'installe que mkdocs-material et le moteur PDF. Le fichier est ajouté via l'API
Files (en mémoire) — on n'écrit PAS dans docs/.

Structure d'une fiche dans armes.md :

    <div class="mcard" markdown>
    **Nom** <span class="prereq">Coût : +10</span> <span class="prereq">Nécessite : …</span>

    Description en une ou deux phrases…

    | Palier | Coût |      (facultatif ; une ou plusieurs tables markdown)
    |---|:---:|
    | 3 m | +20 |
    </div>

La dernière colonne d'une table porte toujours le coût. Le libellé de la première
colonne identifie le palier. La Forge (forge.js) porte la sémantique d'interface
(curseur, choix simple, choix multiple, bascule) ; ce hook ne fournit que le
contenu (noms, coûts, paliers, descriptions).
"""
import html
import json
import re
from pathlib import Path

from mkdocs.structure.files import File

ARMES = "content/regles/combat/armes.md"
MINUS = "−"  # signe moins typographique employé dans les règles


def _slug(name):
    t = name.lower().replace(MINUS, "-")
    for a, b in (("é", "e"), ("è", "e"), ("ê", "e"), ("à", "a"), ("â", "a"),
                 ("î", "i"), ("ï", "i"), ("ô", "o"), ("û", "u"), ("ù", "u"),
                 ("ç", "c"), ("œ", "oe")):
        t = t.replace(a, b)
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t


def _cost(cell):
    """« +10 »/« −20 »/« 0 » -> int (gère le moins typographique). Un tiret seul
    (– / — / - / −) vaut coût nul (0). None si vide ou « var. »."""
    t = (cell or "").replace(MINUS, "-").strip()
    m = re.search(r"-?\s*\d+", t)
    if m:
        return int(m.group().replace(" ", ""))
    return 0 if t in ("-", "–", "—") else None


def _clean(text):
    """Prose lisible : retire balises, liens markdown, gras, espaces multiples."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)   # lien markdown -> texte
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"[*_]", "", text)
    return html.unescape(re.sub(r"\s+", " ", text)).strip()


_MCARD = re.compile(r'<div class="mcard"[^>]*>(.*?)</div>', re.S)
_NAME = re.compile(r"\*\*(.+?)\*\*")
_PREREQ = re.compile(r'<span class="prereq">(.*?)</span>', re.S)


def _tables(lines):
    """Extrait les tables markdown d'un bloc (listes de lignes)."""
    tables, cur = [], []
    for ln in lines:
        if ln.lstrip().startswith("|"):
            cur.append(ln)
        elif cur:
            tables.append(cur)
            cur = []
    if cur:
        tables.append(cur)
    out = []
    for tb in tables:
        rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in tb]
        if len(rows) < 2:
            continue
        header = rows[0]
        body = [r for r in rows[2:] if any(r)]   # rows[1] = séparateur |---|
        parsed = []
        for r in body:
            if len(r) < 2:
                continue
            parsed.append({
                "label": _clean(r[0]),
                "cost": _cost(r[-1]),
                "note": _clean(r[1]) if len(r) > 2 else None,
            })
        if parsed:
            out.append({"cols": [_clean(c) for c in header], "rows": parsed})
    return out


def _parse_card(inner):
    nm = _NAME.search(inner)
    if not nm:
        return None
    name = _clean(nm.group(1))
    spans = [_clean(s) for s in _PREREQ.findall(inner)]
    cout = next((s.split(":", 1)[1].strip() for s in spans
                 if s.lower().startswith("coût") or s.lower().startswith("cout")), "")
    prereqs = [s for s in spans if not (s.lower().startswith("coût")
                                        or s.lower().startswith("cout"))]

    # Retire la ligne de titre (nom + spans) ; le reste = prose puis tables.
    body = inner[nm.end():]
    body = _PREREQ.sub("", body)
    lines = body.splitlines()
    prose = "\n".join(l for l in lines if not l.lstrip().startswith("|"))
    desc = _clean(prose)

    tables = _tables(lines)
    fixed = _cost(cout) if re.fullmatch(r"[+-−]?\s*\d+", cout.strip()) else None
    return {
        "id": _slug(name),
        "name": name,
        "coutLabel": cout,
        "fixedCost": fixed,      # coût fixe si « Coût : +10 », sinon None (var./portée)
        "prereqs": prereqs,      # « Nécessite … », « Incompatible … »
        "desc": desc,
        "tables": tables,
    }


def _section(text, title):
    """Contenu entre « ## <title> » et le prochain « ## » ou « --- » de niveau bloc."""
    m = re.search(r"^##\s+" + re.escape(title) + r"\b.*?$", text, re.M)
    if not m:
        return ""
    start = m.end()
    nxt = re.search(r"^(?:##\s|---\s*$)", text[start:], re.M)
    return text[start:start + nxt.start()] if nxt else text[start:]


def _cards(section):
    return [c for c in (_parse_card(m.group(1)) for m in _MCARD.finditer(section)) if c]


# Armes du tableau (colonnes Arme | AM | Portée | Mains | Dégâts | Mod. | Type |
# Illégalité | Propriétés). Les 3 armes de corps sont hors barème : on les écarte.
# Fiche calquée sur celle produite par la Forge (mêmes clés), pour un affichage
# uniforme des nodes « Arme » dans l'atelier.
_BODY = {"Main", "Pied", "Tête"}


def _armes(text):
    out = []
    for ln in text.splitlines():
        s = ln.strip()
        if not (s.startswith("|") and s.endswith("|")):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) != 10:
            continue
        name = cells[0]
        if name in ("Arme", "") or set(name) <= set("-: "):   # en-tête / séparateur
            continue
        if name in _BODY:
            continue
        out.append({
            "name": name, "total": 100,
            "fiche": {
                "am": cells[1], "portee": cells[2].replace("<br>", " · "), "munitions": cells[3].replace("<br>", " "), "mains": cells[4],
                "degats": cells[5], "mod": cells[6] or "×0", "type": cells[7],
                "illeg": cells[8], "props": cells[9] or "Aucune",
            },
        })
    return out


def _extract(docs_dir):
    text = (docs_dir / ARMES).read_text(encoding="utf-8")
    return {
        "obligatoires": _cards(_section(text, "Propriétés obligatoires")),
        "supplementaires": _cards(_section(text, "Propriétés supplémentaires")),
        "armes": _armes(text),
    }


def on_files(files, config, **kwargs):
    data = _extract(Path(config["docs_dir"]))
    n = len(data["obligatoires"]) + len(data["supplementaires"])
    print(f"[forge] {n} fiches extraites "
          f"(obligatoires={len(data['obligatoires'])}, "
          f"supplementaires={len(data['supplementaires'])}, "
          f"armes={len(data['armes'])})")
    content = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    files.append(File.generated(config, "forge.json", content=content))
    return files


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    root = Path(__file__).resolve().parent.parent
    data = _extract(root / "docs")
    out = sys.argv[1] if len(sys.argv) > 1 else "forge.debug.json"
    Path(out).write_text(json.dumps(data, ensure_ascii=False, indent=2),
                         encoding="utf-8")
    for sec in ("obligatoires", "supplementaires"):
        print(f"\n=== {sec} ({len(data[sec])}) ===")
        for c in data[sec]:
            tb = " ".join(f"[{t['cols'][0]}:{len(t['rows'])}]" for t in c["tables"])
            print(f"  {c['id']:26} coût={c['coutLabel'] or '—':6} "
                  f"fix={c['fixedCost']!s:5} tables={tb or '—'} prereq={c['prereqs']}")
