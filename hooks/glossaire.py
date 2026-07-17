# -*- coding: utf-8 -*-
"""Glossaire général : à la construction, pose une ancre sur chaque bloc-définition et lie
toutes les occurrences des termes de contenu. Un même nom peut avoir plusieurs définitions
(le sens Toucher et la manœuvre Toucher) : le contexte tranche.

Registre : scripts/glossaire.json (scripts/build_glossaire.py).
La carte au survol prend la forme du bloc d'origine (vraie mcard d'une manœuvre, sblock d'un
état, titre + paragraphes d'une compétence). Injectée, masquée, en pied de page.
"""
import re
import sys
from pathlib import Path

# Registre construit à chaud depuis les sources markdown (frais à chaque build, CI comprise).
sys.path.insert(0, str(Path("scripts").resolve()))
import build_glossaire  # noqa: E402

_REG = build_glossaire.build_registry()

# variant -> terme (nom affiché) ; terme -> {variants, defs}
V2TERM = {}
for _term, _e in _REG.items():
    for v in _e["variants"]:
        V2TERM.setdefault(v, _term)


def _piece(v):
    esc = re.escape(v)
    return esc + "s?" if re.fullmatch(r"[^\W\d_]+", v) else esc


_VARIANTS = sorted(V2TERM, key=len, reverse=True)
_PAT = re.compile(r"(?<!\w)(" + "|".join(_piece(v) for v in _VARIANTS) + r")(?!\w)")

_SKIP_TAGS = {"a", "code", "pre", "script", "style", "h1", "h2", "h3", "h4", "h5", "h6"}
_SKIP_CLASSES = {"gloss-defs", "gcard", "gloss-anchor", "gloss-source", "gloss-card"}

# Indices de contexte -> qualifieur préféré, pour départager un nom à plusieurs définitions.
_CUES = [
    ("manœuvre", "manœuvre"), ("manœuvres", "manœuvre"),
    ("l'état", "état"), ("état ", "état"), ("états", "état"),
    ("compétence", "compétence"), ("sens ", "compétence"), ("perception", "compétence"),
    ("jet de ", "compétence"), ("jet d'", "compétence"),
    ("capacité", "capacité"),
    ("propriété", "propriété"), ("dotée", "propriété"), ("possédant", "propriété"),
    ("caractéristique", "caractéristique"),
    ("technique", "technique"),
]

try:
    from bs4 import BeautifulSoup, NavigableString
except Exception:
    BeautifulSoup = None


def _term_for(text):
    if text in V2TERM:
        return V2TERM[text]
    if text and text[-1] in "sx" and text[:-1] in V2TERM:
        return V2TERM[text[:-1]]
    return None


def _choose(defs, before, page_url):
    if len(defs) == 1:
        return defs[0]
    ctx = before[-30:].lower()
    for cue, qual in _CUES:
        if cue in ctx:
            for d in defs:
                if d["qualifier"] == qual:
                    return d
    for d in defs:                      # sinon, la définition locale à la page
        if d["home"] == page_url:
            return d
    return defs[0]                       # sinon, priorité (ordre du registre)


def _first_strong(el):
    st = el.find("strong")
    return st.get_text().strip().rstrip(":").strip() if st else None


def _rel_prefix(url):
    return "../" * url.strip("/").count("/") if url.strip("/") else ""


def on_page_content(html, page, config, files, **kw):
    if BeautifulSoup is None or not html:
        return html
    src = str(getattr(page.file, "src_uri", "") or "")
    if not src.startswith("content/") or not src.endswith(".md"):
        return html
    page_url = page.url or ""
    soup = BeautifulSoup(html, "html.parser")

    # 1) Ancres des définitions présentes sur cette page.
    home_blocks = {}   # anchor -> élément défini ici
    for term, e in _REG.items():
        for d in e["defs"]:
            if d["home"] != page_url:
                continue
            block = None
            if d["kind"] in ("mcard", "sblock"):
                for el in soup.select("." + d["kind"]):
                    if el.get("data-key"):          # ne pas cibler une carte injectée
                        continue
                    if _first_strong(el) == term:
                        block = el
                        break
            elif d["kind"] == "defs":
                for p in soup.select(".defs p"):
                    st = p.find("strong")
                    if st and st.get_text().strip().rstrip(":").strip() == term:
                        block = p
                        break
            else:  # head
                for h in soup.find_all(["h2", "h3", "h4", "h5"]):
                    if h.get_text().strip() == term:
                        block = h
                        break
            if block is None:
                continue
            anc = soup.new_tag("span")
            anc["class"] = "gloss-anchor"
            anc["id"] = "gloss-" + d["anchor"]
            block.insert_before(anc)
            home_blocks[d["anchor"]] = block

    # 2) Liaison des occurrences.
    used = {}   # anchor -> card html
    rel = _rel_prefix(page_url)

    def inside(node, blk):
        for anc in node.parents:
            if anc is blk:
                return True
        return False

    for tn in list(soup.find_all(string=True)):
        skip = False
        for anc in tn.parents:
            if getattr(anc, "name", None) in _SKIP_TAGS:
                skip = True
                break
            cls = set(anc.get("class", []) or []) if hasattr(anc, "get") else set()
            if cls & _SKIP_CLASSES:
                skip = True
                break
        if skip:
            continue
        s = str(tn)
        if not _PAT.search(s):
            continue
        pieces, last, changed = [], 0, False
        for m in _PAT.finditer(s):
            term = _term_for(m.group(1))
            if not term:
                continue
            d = _choose(_REG[term]["defs"], s[:m.start()], page_url)
            blk = home_blocks.get(d["anchor"])
            if blk is not None and inside(tn, blk):     # pas d'auto-lien dans la définition
                continue
            frag = "" if d["kind"] == "concept" else "#gloss-" + d["anchor"]
            href = frag if (d["home"] == page_url and frag) else (rel + d["home"] + frag)
            if m.start() > last:
                pieces.append(NavigableString(s[last:m.start()]))
            a = soup.new_tag("a", href=href)
            a["class"] = "gloss-link"
            a["data-key"] = "terme:" + d["anchor"]
            a.string = m.group(1)
            pieces.append(a)
            used[d["anchor"]] = d["card"]
            last, changed = m.end(), True
        if not changed:
            continue
        if last < len(s):
            pieces.append(NavigableString(s[last:]))
        tn.replace_with(*pieces)

    # 3) Cartes utilisées (vraies cartes des blocs), masquées en pied de page.
    if used:
        defs = soup.new_tag("div")
        defs["class"] = "gloss-defs"
        defs.append(BeautifulSoup("".join(used.values()), "html.parser"))
        soup.append(defs)

    return str(soup)
