"""Hook MkDocs : extrait les modules de Nen des règles et expose nen-atelier.json.

C'est le pont de synchronisation entre les règles et l'atelier de création de
pouvoir (page « Création de pouvoir »). Les fiches de module sont écrites une
seule fois, dans les .md des six catégories de Nen ; ce hook les relit au build
et en fait un JSON que le GUI consomme. Ainsi une valeur modifiée dans les
règles se répercute automatiquement dans l'atelier : aucune double saisie, aucun
risque de dérive.

On n'utilise que la bibliothèque standard (pas de bs4) : la CI n'installe que
mkdocs-material et le moteur PDF. Le fichier est ajouté via l'API Files (en
mémoire) — on n'écrit PAS dans docs/, sinon `mkdocs serve` reconstruirait en
boucle.

Structure d'un module dans les règles (voir p.ex. emission.md) :

    <div class="cj-modules anima" markdown>
    <div class="keep" markdown>
    #### Nom du module
    <p class="mod-type">Catégorie : renforcement<br>Types : attaque</p>
    Description en une ou deux phrases…
    <table>
      <thead><tr><th>Bonus</th><th>DI</th><th>CAR</th><th>UA</th><th>MA</th><th>AE</th></tr></thead>
      <tbody>
        <tr class="cat"><td>Sous-groupe</td>…</tr>   (facultatif)
        <tr><td>+10</td><td>5</td>…</tr>
      </tbody>
    </table>
    </div></div>

Un module = un ou plusieurs tableaux (« grilles »). Chaque grille se découpe en
« groupes » : soit le tableau entier (pas de ligne .cat), soit chaque sous-bloc
introduit par une ligne <tr class="cat">. On retient une ligne par groupe (ou
plusieurs si le groupe est « cumulable »). DI/UA/MA/AE se somment sur les lignes
retenues.
"""
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path

from mkdocs.structure.files import File

# ---------------------------------------------------------------------------
# Fichiers de règles à scanner, avec la catégorie par défaut de leurs modules.
# capacites-de-nen.md porte les modules de raccord (catégorie « aucune »), lue
# sur la fiche elle-même. ancienne-version.md et refonte_nen.md sont exclus.
# ---------------------------------------------------------------------------
SOURCES = [
    ("content/regles/nen/renforcement.md", "renforcement"),
    ("content/regles/nen/emission.md", "émission"),
    ("content/regles/nen/transmutation.md", "transmutation"),
    ("content/regles/nen/manipulation.md", "manipulation"),
    ("content/regles/nen/conjuration.md", "conjuration"),
    ("content/regles/nen/specialisation.md", "spécialisation"),
    ("content/regles/nen/capacites-de-nen.md", None),
]

# ---------------------------------------------------------------------------
# Archétypes : affinités d'emploi (AE %) par catégorie, transcrites depuis
# archetypes-nen.md. La spécialisation est notée « 0 % ou X* » : on garde la
# valeur haute (X), atteignable avec l'avantage Spécialiste ; sans lui, 0.
# Ordre des catégories : renf, émis, transm, manip, conj, spé.
# ---------------------------------------------------------------------------
CATS = ["renforcement", "émission", "transmutation", "manipulation",
        "conjuration", "spécialisation"]

ARCHETYPES = [
    ("Renforceur",              [100, 80, 80, 60, 60, 40], False),
    ("Émitteur",                [80, 100, 60, 80, 40, 60], False),
    ("Transmuteur",             [80, 60, 100, 40, 80, 60], False),
    ("Manipulateur",            [60, 80, 40, 100, 60, 80], False),
    ("Conjurateur",             [60, 40, 80, 60, 100, 80], False),
    ("Spécialiste",             [40, 60, 60, 80, 80, 100], True),
    ("Renforceur-Émitteur",     [90, 90, 70, 70, 50, 50], False),
    ("Renforceur-Transmuteur",  [90, 70, 90, 50, 70, 50], False),
    ("Émitteur-Manipulateur",   [70, 90, 50, 90, 50, 70], False),
    ("Transmuteur-Conjurateur", [70, 50, 90, 50, 90, 70], False),
    ("Manipulateur-Spécialiste", [50, 70, 50, 90, 70, 90], True),
    ("Conjurateur-Spécialiste", [50, 50, 70, 70, 90, 90], True),
]

MINUS = "−"  # signe moins typographique (−) utilisé dans les règles


def _num(text, default=0):
    """« 120 » -> 120 ; « — »/vide -> default ; gère le moins typographique."""
    t = (text or "").replace(MINUS, "-").strip()
    m = re.search(r"-?\d+", t)
    return int(m.group()) if m else default


def _car(text):
    """CAR : entier, ou None si « — »."""
    t = (text or "").replace(MINUS, "-").strip()
    m = re.search(r"-?\d+", t)
    return int(m.group()) if m else None


def _ae(text):
    """AE : décalage en points de %, signé. « — » -> 0."""
    t = (text or "").replace(MINUS, "-").strip()
    m = re.search(r"(-?\d+)\s*%", t)
    return int(m.group(1)) if m else 0


def _slug(name):
    t = name.lower().replace(MINUS, "-")
    t = (t.replace("é", "e").replace("è", "e").replace("ê", "e").replace("à", "a")
          .replace("â", "a").replace("î", "i").replace("ï", "i").replace("ô", "o")
          .replace("û", "u").replace("ù", "u").replace("ç", "c").replace("œ", "oe"))
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t


class _TableParser(HTMLParser):
    """Extrait un <table> en (header, rows) où chaque row = (is_cat, [cells])."""

    def __init__(self):
        super().__init__()
        self.header = []
        self.rows = []
        self._section = None       # 'thead' | 'tbody' | None
        self._in_tr = False
        self._tr_is_cat = False
        self._cells = None
        self._cell = None          # buffer texte de la cellule courante

    def handle_starttag(self, tag, attrs):
        if tag in ("thead", "tbody"):
            self._section = tag
        elif tag == "tr":
            self._in_tr = True
            self._cells = []
            self._tr_is_cat = any(k == "class" and "cat" in (v or "")
                                  for k, v in attrs)
        elif tag in ("td", "th") and self._in_tr:
            self._cell = []

    def handle_endtag(self, tag):
        if tag in ("thead", "tbody"):
            self._section = None
        elif tag in ("td", "th") and self._cell is not None:
            txt = html.unescape("".join(self._cell)).strip()
            self._cells.append(txt)
            self._cell = None
        elif tag == "tr" and self._in_tr:
            if self._section == "thead":
                self.header = self._cells
            else:
                self.rows.append((self._tr_is_cat, self._cells))
            self._in_tr = False
            self._cells = None

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)


def _parse_table(table_html):
    p = _TableParser()
    p.feed(table_html)
    return p.header, p.rows


def _build_groups(header, rows):
    """Découpe les lignes d'un tableau en groupes selon les lignes .cat.

    Renvoie une liste de groupes : {label, cumulable, mandatory, column, rows}.
    """
    column = header[0] if header else "Effet"
    # Une seule colonne d'affinité, dont l'en-tête dit la portée : « AEG » (décalage
    # global, socles et raccord) ou « AEL » (décalage local, modules). On la lit sur
    # l'en-tête et on range la valeur dans le bon champ ; le GUI choisit l'affichage
    # via aeScope.
    ae_hdr = (header[-1] if header else "").strip().upper()
    scope = "ael" if "AEL" in ae_hdr else "aeg"
    # En-tête de la colonne d'aura (position 3) : « UA » d'ordinaire, « UAA » (unité d'aura
    # accumulée) pour un module qui se paie en aura accumulée (ex. Réserve de Nen).
    ua_label = header[3].strip() if len(header) > 3 and header[3].strip() else "UAA"
    groups = []
    cur = None

    def new_group(label):
        low = (label or "").lower()
        return {
            "label": label or None,
            "cumulable": "cumulable" in low,
            "mandatory": "obligatoire" in low,
            "column": column,
            "aeScope": scope,
            "uaLabel": ua_label,
            "rows": [],
        }

    for is_cat, cells in rows:
        if is_cat:
            cur = new_group(cells[0] if cells else "")
            groups.append(cur)
            continue
        if cur is None:
            cur = new_group(None)
            groups.append(cur)
        if len(cells) < 6:
            continue  # ligne mal formée : on l'ignore
        label = cells[0]
        ae_val = _ae(cells[5])
        row = {
            "label": label,
            "di": _num(cells[1]),
            "car": _car(cells[2]),
            "ua": _num(cells[3]),
            "ma": _num(cells[4]),
            "aeg": ae_val if scope == "aeg" else 0,
            "ael": ae_val if scope == "ael" else 0,
        }
        m = re.match(r"\s*([+-]?\d+)", label.replace(MINUS, "-"))
        if m:
            row["value"] = int(m.group(1))
        cur["rows"].append(row)

    # Purge des groupes vides (p. ex. en-tête .cat sans lignes derrière).
    return [g for g in groups if g["rows"]]


def _parse_modtype(inner, default_cat):
    """Analyse <p class="mod-type"> : catégorie, chaîne de types, types std."""
    text = re.sub(r"<br\s*/?>", "\n", inner)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    category = default_cat
    types_raw = ""
    special = None
    for line in (l.strip() for l in text.splitlines() if l.strip()):
        m = re.match(r"cat[ée]gorie\s*:\s*(.+)", line, re.I)
        if m:
            val = m.group(1).strip().lower()
            category = None if val in ("aucune", "—", "-") else val
            continue
        m = re.match(r"types?\s*:\s*(.+)", line, re.I)
        if m:
            types_raw = m.group(1).strip()
            continue
        # Ni catégorie ni types : mention libre (« Obligatoire », etc.).
        special = line
    std = []
    for pat, canon in (("attaque", "attaque"), ("défense", "défense"), ("effet", "effet"),
                       (r"cr[ée]ature|b[êe]te", "créature"), ("objet", "objet")):
        if re.search(pat, types_raw, re.I):
            std.append(canon)
    return category, types_raw, std, special


def _is_scaled(name, desc):
    """L'effet est-il chiffré (multiplié par l'affinité d'emploi effective) ?

    Règle du livre : l'affinité multiplie les seuls effets chiffrés (un bonus,
    des dégâts, un seuil) ; un effet descriptif ou un *nombre* (d'actions, de
    capacités) n'est jamais multiplié. On lit donc la fiche :

    - signal explicite : « effet chiffré », « multiplié par l'affinité » ;
    - sinon, magnitude : la fiche ajoute/retranche un « bonus » ou un « montant »
      à un jet, à des dégâts, à une caractéristique ou compétence — sauf si elle
      décrit un *nombre* (« nombre indiqué d'actions », module « … supplémentaires »).
    """
    if re.search(r"chiffr|multipli\w*\s+par\s+l.?affinit|affinit\w+\s+effective",
                 desc, re.I):
        return True
    is_count = re.search(
        r"nombre indiqu|\bde plus\b|suppl[ée]mentaires?|nombre d[e'’]", name + " " + desc,
        re.I)
    if is_count:
        return False
    magnitude = re.search(
        r"\bbonus\b|\bmontant\b|retranch\w+|ajoute .{0,40}d[ée]g[âa]ts|"
        r"[àa] (?:une|la|toutes?|ses) (?:attaques?|esquives?|parades?|"
        r"caract[ée]ristique|comp[ée]tence)",
        desc, re.I)
    return bool(magnitude)


def _clean_desc(seg):
    """Texte lisible d'un segment de prose : retire les blocs de defs, les
    balises HTML et les marqueurs gras markdown."""
    seg = re.sub(r'<div class="defs".*?</div>', " ", seg, flags=re.S)
    seg = re.sub(r"<[^>]+>", " ", seg)
    seg = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", seg)   # liens markdown -> texte
    seg = re.sub(r"\*\*(.*?)\*\*", r"\1", seg)
    return html.unescape(re.sub(r"\s+", " ", seg)).strip()


_DEFSBLOCK = re.compile(r'<div class="defs".*?</div>', re.S)
_DEFPAIR = re.compile(r"\*\*\s*(.+?)\s*:\s*\*\*\s*(.*?)(?=\*\*|\Z)", re.S)


def _nk(s):
    """Clé de rapprochement légende <-> ligne : minuscule, espaces normalisés."""
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def _parse_defs(seg):
    """Paires (**Terme :** définition) des blocs <div class="defs"> d'un segment."""
    out = []
    for dm in _DEFSBLOCK.finditer(seg):
        inner = re.sub(r"<[^>]+>", " ", dm.group(0))
        inner = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", inner)
        inner = html.unescape(inner)
        for m in _DEFPAIR.finditer(inner):
            term = re.sub(r"\s+", " ", m.group(1)).strip()
            text = re.sub(r"\s+", " ", m.group(2)).strip()
            if term and text:
                out.append((term, text))
    return out


# Un bloc module = un titre #### suivi, avant le prochain ####, d'un mod-type.
_HEADING = re.compile(r"^####\s+(.+?)\s*$", re.M)
_MODTYPE = re.compile(r'<p class="mod-type">(.*?)</p>', re.S)
_TABLE = re.compile(r"<table\b.*?</table>", re.S)


def _parse_file(text, default_cat, source):
    heads = list(_HEADING.finditer(text))
    modules = []
    for i, h in enumerate(heads):
        start = h.end()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        block = text[start:end]
        mt = _MODTYPE.search(block)
        if not mt:
            continue  # titre de prose, pas un module
        name = re.sub(r"\s*\{:.*?\}\s*$", "", h.group(1)).strip()
        category, types_raw, std, special = _parse_modtype(mt.group(1), default_cat)

        # Description du module : texte entre </p> du mod-type et le 1er <table>.
        after = block[mt.end():]
        tpos = after.find("<table")
        desc = _clean_desc(after[:tpos] if tpos != -1 else after)

        # Chaque grille porte la prose qui la précède (le 1er tableau est couvert
        # par la description du module ; les suivants gardent leur paragraphe).
        grids = []
        tms = list(_TABLE.finditer(block))
        prev_end = mt.end()
        for ti, tm in enumerate(tms):
            header, rows = _parse_table(tm.group(0))
            groups = _build_groups(header, rows)
            if groups:
                # chaque GROUPE porte sa propre description : la légende de son nom de
                # colonne si elle existe, sinon la prose qui précède son tableau (1er
                # groupe). Les légendes de LIGNE restent sur la ligne (affichées à la
                # sélection). Le 1er tableau est couvert par la description du module.
                prose = "" if not grids else _clean_desc(block[prev_end:tm.start()])
                nxt = tms[ti + 1].start() if ti + 1 < len(tms) else len(block)
                defs = _parse_defs(block[tm.end():nxt])
                dmap = {_nk(t): txt for t, txt in defs}
                used = set()
                for pi, grp in enumerate(groups):
                    gk = _nk(grp.get("label") or grp.get("column", ""))
                    if gk in dmap:
                        grp["desc"] = dmap[gk]
                        used.add(gk)
                    else:
                        grp["desc"] = prose if pi == 0 else ""
                    for row in grp["rows"]:
                        rk = _nk(row["label"])
                        if rk in dmap:
                            row["def"] = dmap[rk]
                            used.add(rk)
                extras = [t + " : " + txt for t, txt in defs if _nk(t) not in used]
                if extras:
                    groups[0]["desc"] = (groups[0]["desc"] + " " + " ".join(extras)).strip()
                grids.append({"groups": groups})
            prev_end = tm.end()
        # un socle de base (attaque/défense/effet) est une fiche « Socle : … » sans table :
        # on le garde quand même (coût nul, pas de grille) ; les autres modules sans table sont
        # de la prose, on les ignore.
        if not grids and not (special and special.strip().lower().startswith("socle")):
            continue

        scaled = _is_scaled(name, desc)
        modules.append({
            "id": f"{(category or 'raccord')}-{_slug(name)}",
            "name": name,
            "category": category,           # None = raccord / structurel
            "typesRaw": types_raw,
            "types": std,                   # sous-ensemble std attaque/défense/effet
            "special": special,             # ex. « Obligatoire », « conjuration de créature »
            "description": desc,
            "scaled": scaled,               # l'effet chiffré est-il multiplié par l'AE ?
            "grids": grids,
            "source": source,
        })
    return modules


def _extract(docs_dir):
    modules = []
    per_file = {}
    for rel, default_cat in SOURCES:
        p = docs_dir / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        found = _parse_file(text, default_cat, rel)
        per_file[rel] = len(found)
        modules.extend(found)
    archetypes = [
        {"name": n, "affinities": dict(zip(CATS, aff)), "specialist": spec}
        for n, aff, spec in ARCHETYPES
    ]
    data = {
        "categories": CATS,
        "archetypes": archetypes,
        "modules": modules,
    }
    return data, per_file


def on_files(files, config, **kwargs):
    docs_dir = Path(config["docs_dir"])
    data, per_file = _extract(docs_dir)
    summary = ", ".join(f"{Path(k).stem}={v}" for k, v in per_file.items())
    print(f"[nen_atelier] {len(data['modules'])} modules extraits ({summary})")
    content = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    files.append(File.generated(config, "nen-atelier.json", content=content))
    return files


if __name__ == "__main__":
    # Exécution directe pour inspection : dump vers scratch + résumé lisible.
    import sys
    root = Path(__file__).resolve().parent.parent
    data, per_file = _extract(root / "docs")
    out = sys.argv[1] if len(sys.argv) > 1 else "nen-atelier.debug.json"
    Path(out).write_text(json.dumps(data, ensure_ascii=False, indent=2),
                         encoding="utf-8")
    print(f"{len(data['modules'])} modules -> {out}")
    for k, v in per_file.items():
        print(f"  {v:3d}  {k}")
    for m in data["modules"]:
        ng = sum(len(g["groups"]) for g in m["grids"])
        print(f"    [{m['category'] or 'raccord':13}] {m['name']:32} "
              f"types={m['types'] or m['special']!s:18} grilles={len(m['grids'])} "
              f"groupes={ng} scaled={m['scaled']}")
