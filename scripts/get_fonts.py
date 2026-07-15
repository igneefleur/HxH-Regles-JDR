# -*- coding: utf-8 -*-
"""Récupère les polices du livre chez Google Fonts et les AUTO-HÉBERGE.

Écrit les .woff2 dans docs/assets/fonts/, leurs licences dans
docs/assets/fonts/licences/, et régénère docs/stylesheets/fonts.css (@font-face
locaux). Après ça, le site ne contacte plus fonts.googleapis.com : l'adresse IP du
visiteur ne part plus chez un tiers, et le build du PDF (WeasyPrint) n'a plus
besoin du réseau.

Ne garde que les sous-ensembles latin + latin-ext : suffisant pour le français (œ
compris, il est dans « latin »), et ça évite de trimballer cyrillique, grec et
vietnamien. Les unicode-range font que le navigateur ne télécharge que ce dont il
a besoin.

Usage : python scripts/get_fonts.py   (depuis la racine du dépôt)
"""
import re
import pathlib
import urllib.request

# Un User-Agent moderne est OBLIGATOIRE : sinon Google renvoie du TTF/EOT legacy
# au lieu du woff2.
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

# Union des graisses réellement utilisées : par le livre (extra.css) ET par
# l'interface de Material (qui demandait Alegreya 300..700 + Roboto Mono).
CSS_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Alegreya:ital,wght@0,400;0,500;0,600;0,700;1,400;1,700"
    "&family=Cinzel:wght@600;700"
    "&family=EB+Garamond:ital,wght@0,400;0,600;1,400"
    "&family=IBM+Plex+Sans:wght@400;500;600;700"
    "&family=Roboto+Mono:ital,wght@0,400;0,700;1,400;1,700"
    "&display=swap"
)
SUBSETS = {"latin", "latin-ext"}

# Licences (toutes SIL Open Font License 1.1), depuis le dépôt officiel google/fonts.
LICENCES = {
    "alegreya":      "ofl/alegreya/OFL.txt",
    "cinzel":        "ofl/cinzel/OFL.txt",
    "eb-garamond":   "ofl/ebgaramond/OFL.txt",
    "ibm-plex-sans": "ofl/ibmplexsans/OFL.txt",
    "roboto-mono":   "ofl/robotomono/OFL.txt",   # Roboto est passée d'Apache 2.0 à l'OFL
}

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = ROOT / "docs" / "assets" / "fonts"
LIC = FONTS / "licences"
CSS_OUT = ROOT / "docs" / "stylesheets" / "fonts.css"

HEADER = """/* ============================================================================
   POLICES AUTO-HÉBERGÉES — aucune requête vers Google.
   Les .woff2 vivent dans docs/assets/fonts/ et leurs licences (toutes SIL Open
   Font License 1.1) dans docs/assets/fonts/licences/. Voir le LISEZMOI de ce
   dossier pour la liste et les conditions.
   Le visiteur ne contacte donc plus fonts.googleapis.com / fonts.gstatic.com :
   son adresse IP n'est plus transmise à un tiers. Le build du PDF (WeasyPrint)
   n'a plus besoin du réseau non plus.
   Sous-ensembles embarqués : latin + latin-ext (suffisant pour le français, œ
   compris) ; les unicode-range font que le navigateur ne charge que le
   nécessaire. NE PAS éditer à la main : régénéré par scripts/get_fonts.py.
   ============================================================================ */
"""


def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as f:
        return f.read() if binary else f.read().decode()


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def main():
    FONTS.mkdir(parents=True, exist_ok=True)
    LIC.mkdir(parents=True, exist_ok=True)

    css = fetch(CSS_URL)
    blocks = re.findall(r"/\*\s*([a-z-]+)\s*\*/\s*(@font-face\s*\{[^}]*\})", css)

    faces, count = [], {}
    for subset, blk in blocks:
        if subset not in SUBSETS:
            continue
        fam = re.search(r"font-family:\s*'([^']+)'", blk).group(1)
        wght = re.search(r"font-weight:\s*(\d+)", blk).group(1)
        ital = "i" if re.search(r"font-style:\s*italic", blk) else ""
        url = re.search(r"url\((https://[^)]+\.woff2)\)", blk).group(1)
        urange = re.search(r"unicode-range:\s*([^;]+);", blk).group(1).strip()

        name = f"{slug(fam)}-{wght}{ital}-{subset}.woff2"
        path = FONTS / name
        if not path.exists():
            path.write_bytes(fetch(url, binary=True))
        count[fam] = count.get(fam, 0) + 1
        faces.append((fam, wght, "italic" if ital else "normal", name, urange, subset))

    out = [HEADER]
    for fam, wght, style, name, urange, subset in faces:
        it = " italic" if style == "italic" else ""
        out.append(
            f"\n/* {fam} {wght}{it} — {subset} */\n"
            f"@font-face {{\n"
            f"  font-family: '{fam}';\n"
            f"  font-style: {style};\n"
            f"  font-weight: {wght};\n"
            f"  font-display: swap;\n"
            f"  src: url('../assets/fonts/{name}') format('woff2');\n"
            f"  unicode-range: {urange};\n"
            f"}}"
        )
    CSS_OUT.write_text("\n".join(out) + "\n", encoding="utf-8")

    for key, path in LICENCES.items():
        dest = LIC / f"{key}-OFL.txt"
        dest.write_text(
            fetch(f"https://raw.githubusercontent.com/google/fonts/main/{path}"),
            encoding="utf-8",
        )

    total = sum(f.stat().st_size for f in FONTS.glob("*.woff2"))
    print(f"[fonts] {len(faces)} faces, {total/1024:.0f} Ko -> {FONTS}")
    for fam, n in count.items():
        print(f"        {fam}: {n} fichiers")
    print(f"[fonts] {len(LICENCES)} licences -> {LIC}")
    print(f"[fonts] CSS regénéré -> {CSS_OUT}")


if __name__ == "__main__":
    main()
