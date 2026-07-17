# -*- coding: utf-8 -*-
"""Registre du glossaire général : chaque terme de contenu du livre, ses définitions (une par
endroit où il est défini), l'ancre de chacune, et la CARTE affichée au survol.

La carte prend la forme du bloc d'origine : la vraie carte de la manœuvre (mcard), de l'état
(sblock), ou un titre + paragraphes pour une compétence / règle. Un même nom peut porter
plusieurs définitions (le sens Toucher et la manœuvre Toucher) ; le hook choisit la bonne
selon le contexte.

Produit scripts/glossaire.json, consommé par hooks/glossaire.py.
Usage : python scripts/build_glossaire.py
"""
import json
import re
import unicodedata
from pathlib import Path

import markdown as _md

CONTENT = Path("docs/content")
OUT = Path("scripts/glossaire.json")

EXCLUDE = {
    "regles/nen/refonte_nen.md", "regles/index.md",
    "univers/index.md", "univers/cartes.md", "univers/heavens-arena.md",
    "regles/annexes/conversion-magicien-dnd.md",
}

# Priorité : quand un terme n'a qu'une définition possible mais que plusieurs pages le citent,
# la 1re page de cette liste fait foi. Sert aussi de départage final entre définitions.
PRIORITY = [
    "regles/personnage/competences.md", "regles/personnage/caracteristiques.md",
    "regles/personnage/capacites-physiques.md", "regles/personnage/sens.md",
    "regles/personnage/etats.md", "regles/personnage/eclat.md",
    "regles/personnage/influence.md", "regles/personnage/avantages.md",
    "regles/personnage/classe.md", "regles/personnage/points-formation.md",
    "regles/combat/manoeuvres.md", "regles/combat/deroulement-combat.md",
    "regles/combat/armes.md", "regles/combat/critique-blessures.md",
    "regles/monde/degats.md", "regles/monde/tailles.md", "regles/monde/formes.md",
    "regles/nen/techniques-nen.md", "regles/nen/capacites-de-nen.md",
    "regles/nen/archetypes-nen.md", "regles/nen/aura.md", "regles/nen/di.md",
    "regles/nen/renforcement.md", "regles/nen/emission.md", "regles/nen/manipulation.md",
    "regles/nen/conjuration.md", "regles/nen/transmutation.md", "regles/nen/specialisation.md",
]

STOP = {
    "action", "actions", "jet", "jets", "malus", "bonus", "tour", "round", "dé", "dés",
    "réaction", "réactions", "point", "points", "valeur", "seuil", "table", "colonne",
    "ligne", "personnage", "adversaire", "cible", "arme", "armes", "corps", "coup",
    "aucun", "spécial", "oui", "non", "capacité", "capacités",
}

# Concepts importants sans bloc-définition propre : on leur écrit une carte (prose du livre)
# et on les donne comme définition PAR DÉFAUT, devant une éventuelle homonyme (capacité de Nen).
CURATED = {
    "Compétence": ("regles/personnage/competences.md",
                   "Une compétence mesure ce qu'un personnage sait faire dans un domaine précis. "
                   "Chaque compétence repose sur une caractéristique et se teste par un jet, comparé "
                   "à un seuil de difficulté ou au jet d'un adversaire."),
    "Caractéristique": ("regles/personnage/caracteristiques.md",
                        "Les caractéristiques mesurent les aptitudes de base d'un personnage. Elles "
                        "vont de 0 à 30, où 5 est la moyenne humaine et 9 le sommet humain réel, et "
                        "fondent les compétences et les capacités."),
}
# Termes parasites (paramètres / adjectifs des pages de Nen, pas de vrais termes de glossaire).
STOP_TERMS = {
    "Grande", "Petite", "Moyenne", "Colossale", "Gigantesque", "Titanesque", "Portative",
    "Vivable", "Meuble", "Grasse", "Adjacente", "Dépendante", "Indépendante", "Instantané",
    "Instantanée", "Conscience", "Quantité", "Objets", "Créatures", "Portable",
}
BLOCK_LOWER = {
    "aura", "force", "prise", "porte", "présente", "présent", "part", "sens", "point",
    "points", "vol", "vue", "état", "états", "arme", "armes", "touche", "attaque",
    "attaques", "course", "nage", "chasse", "garde", "reste", "passe", "coup",
}

_DET = re.compile(r"^(le|la|les|l'|un|une|des|du|de|d'|au|aux|à|ce|ses|son|sa|leur)\b", re.I)
_VERBS = ("ajouter", "changer", "interagir", "répartir", "alterner", "combler", "choisir",
          "poser", "payer", "régler", "vérifier", "additionner", "empiler", "lire",
          "composer", "fixer", "franchir", "porter", "tirer", "pousser", "forcer",
          "retenir", "veiller", "employer", "utiliser", "gérer", "calculer", "résoudre")


def is_procedural(title):
    t = title.strip()
    if re.match(r"^\d", t):
        return True
    first = t.split()[0].lower() if t.split() else ""
    if first in _VERBS:
        return True
    if _DET.match(t):
        return True
    if len(t.split()) > 4:
        return True
    return False


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()


def rel_src(md):
    return str(md.relative_to(CONTENT)).replace("\\", "/")


def rel_url(md):
    p = md.relative_to("docs").with_suffix("")
    parts = [x for x in p.parts]
    if parts[-1] == "index":
        parts = parts[:-1]
    return "/".join(parts) + "/"


def qualifier(kind, src):
    if kind == "sblock":
        return "état"
    if kind == "mcard":
        if "manoeuvres" in src:
            return "manœuvre"
        if "armes" in src:
            return "propriété"
        if "/art/" in src:
            return "art"
        if "caracteristiques" in src:
            return "caractéristique"
        if "techniques-nen" in src:
            return "technique"
        if "avantages" in src:
            return "avantage"
        if "formations" in src:
            return "formation"
        return "règle"
    if kind == "head":
        if "competences" in src:
            return "compétence"
        if "capacites-physiques" in src:
            return "capacité"
        if "/nen/" in src:
            return "Nen"
        return "règle"
    if kind == "defs":
        if "formes" in src:
            return "forme"
        if "/nen/" in src:
            return "Nen"
        return "règle"
    return "règle"


def iter_divs(text, cls):
    """Blocs <div class="cls…" … markdown …>…</div> à profondeur équilibrée (gère l'imbrication)."""
    for m in re.finditer(rf'<div class="{cls}[^"]*"[^>]*\bmarkdown\b[^>]*>', text):
        start = m.end()
        depth = 1
        for mm in re.finditer(r"<div\b|</div>", text[start:]):
            if mm.group() == "</div>":
                depth -= 1
                if depth == 0:
                    yield text[start:start + mm.start()]
                    break
            else:
                depth += 1


MD_EXT = ["attr_list", "md_in_html", "tables", "abbr"]


def strip_links(md):
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", md)   # pas de lien imbriqué dans une carte


def render_card(term, inner_md, kind, anchor):
    key = "terme:" + anchor
    body = strip_links(inner_md).strip()
    if kind in ("mcard", "sblock"):
        raw = (f'<div class="{kind} gloss-card" data-key="{key}" markdown>\n\n'
               f'**{term}**\n\n{body}\n\n</div>')
        return _md.markdown(raw, extensions=MD_EXT)
    # head / defs : titre + paragraphes
    raw = (f'<div class="gcard gloss-card" data-key="{key}" markdown>\n\n'
           f'**{term}**\n<div class="gcard-text" markdown>\n\n{body}\n\n</div>\n\n</div>')
    return _md.markdown(raw, extensions=MD_EXT)


# --- Construction du registre : term -> {variants, defs:[{home,kind,qualifier,anchor,card}]} ---
def build_registry():
    raw_defs = {}

    def collect(term, home, kind, qual, inner):
        term = term.strip()
        if not term or term.lower() in STOP or term in STOP_TERMS or is_procedural(term):
            return
        raw_defs.setdefault(term, [])
        if any(d["home"] == home and d["kind"] == kind for d in raw_defs[term]):
            return
        raw_defs[term].append({"home": home, "kind": kind, "qualifier": qual, "inner": inner})

    order = {p: i for i, p in enumerate(PRIORITY)}
    all_md = [m for m in CONTENT.rglob("*.md") if rel_src(m) not in EXCLUDE]
    all_md.sort(key=lambda m: (order.get(rel_src(m), 999), rel_src(m)))

    for md in all_md:
        src = rel_src(md)
        text = md.read_text(encoding="utf-8")
        home = rel_url(md)
        is_comp = src == "regles/personnage/competences.md"

        for cls in ("mcard", "sblock"):
            for inner in iter_divs(text, cls):
                tm = re.match(r"\s*\*\*([^*]+?)\*\*", inner)
                if tm:
                    collect(tm.group(1), home, cls, qualifier(cls, src), inner[tm.end():])

        for block in re.findall(r'<div class="defs" markdown>(.*?)</div>', text, re.S):
            for m in re.finditer(r"\*\*([^*:]+?) ?:\*\*(.*?)(?=\n\s*\*\*[^*:]+ ?:\*\*|\Z)", block, re.S):
                name = m.group(1).strip()
                if "(" not in name and "," not in name and not is_procedural(name):
                    collect(name, home, "defs", qualifier("defs", src), m.group(2))

        parts = re.split(r"^(#{3,4}) +(.+)$", text, flags=re.M)
        for i in range(1, len(parts), 3):
            title = re.sub(r"\s*\{#.*\}", "", parts[i + 1]).strip()
            body = parts[i + 2] if i + 2 < len(parts) else ""
            if not is_comp and is_procedural(title):
                continue
            collect(title, home, "head", qualifier("head", src), body)

    terms = {}
    for term in set(raw_defs) | set(CURATED):
        defs = raw_defs.get(term, [])
        curated = term in CURATED
        multi = len(defs) + (1 if curated else 0) > 1
        out = []
        if curated:                              # concept écrit, donné en tête (défaut)
            src_home, prose = CURATED[term]
            anchor = slug(term) + "-concept"
            raw = (f'<div class="gcard gloss-card" data-key="terme:{anchor}" markdown>\n\n'
                   f'**{term}**\n<div class="gcard-text" markdown>\n\n{prose}\n\n</div>\n\n</div>')
            out.append({"home": "content/" + src_home[:-3] + "/", "kind": "concept",
                        "qualifier": "règle", "anchor": anchor, "card": _md.markdown(raw, extensions=MD_EXT)})
        for d in defs:
            anchor = slug(term) + ("-" + slug(d["qualifier"]) if multi else "")
            card = render_card(term, d["inner"], d["kind"], anchor)
            if card.strip():
                out.append({"home": d["home"], "kind": d["kind"],
                            "qualifier": d["qualifier"], "anchor": anchor, "card": card})
        if not out:
            continue
        vs = {term}
        low = term.lower()
        if (" " not in term and term[:1].isupper() and len(term) >= 6
                and re.fullmatch(r"[A-Za-zÀ-ÿ]+", term)
                and low not in BLOCK_LOWER and not low.endswith(("er", "ir", "re", "oir"))):
            vs.add(low)
        terms[term] = {"variants": sorted(vs), "defs": out}
    return terms


if __name__ == "__main__":
    TERMS = build_registry()
    OUT.write_text(json.dumps(TERMS, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    ndef = sum(len(t["defs"]) for t in TERMS.values())
    nmulti = sum(1 for t in TERMS.values() if len(t["defs"]) > 1)
    print(f"{len(TERMS)} termes, {ndef} définitions ({nmulti} multi-définitions) -> {OUT}")
