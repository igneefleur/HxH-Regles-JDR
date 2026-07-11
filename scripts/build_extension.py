"""Packe l'extension (Firefox + Chrome) en fichiers téléchargeables depuis le site.

- Firefox : extension/firefox/ (Manifest V2) -> docs/download/hxh-roll20-firefox.xpi
- Chrome  : extension/chrome/manifest.json (Manifest V3) + les fichiers PARTAGÉS
  de extension/firefox/ (render.js, content-*.js, overlay.css, icons/, popup/)
  -> docs/download/hxh-roll20-chrome.zip

Le code JS/CSS/les icônes n'existent qu'une fois (dans firefox/) : seul le manifest
diffère entre les deux navigateurs. On écrit les entrées avec des séparateurs « / »
(Compress-Archive de PowerShell 5.1 met des « \\ » que Firefox refuse) et manifest.json
est toujours à la racine de l'archive.

    python scripts/build_extension.py
"""
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FF = ROOT / "extension" / "firefox"           # source de vérité (manifest V2 + fichiers)
CHROME_MANIFEST = ROOT / "extension" / "chrome" / "manifest.json"  # manifest V3 seul
DL = ROOT / "docs" / "download"
OUT_FF = DL / "hxh-roll20-firefox.xpi"
OUT_CHROME = DL / "hxh-roll20-chrome.zip"

# La fiche de l'extension réutilise le VRAI CSS de la fiche du site (creation.css)
# pour un rendu identique : l'extension ne pouvant pas lire docs/ à l'exécution, on
# en garde une copie dans le paquet, resynchronisée depuis la source à chaque build.
CREATION_CSS_SRC = ROOT / "docs" / "stylesheets" / "creation.css"
CREATION_CSS_DST = FF / "creation.css"


# Les tailles de la fiche sont en rem, calibrées pour la racine de 20 px de mkdocs
# Material. Dans Roll20, la racine du document est bien plus petite -> tout rétrécit.
# On réécrit donc chaque « Nrem » en « calc(N * var(--pc-rem, 16px)) » : même
# sémantique que rem (chaque valeur = N × base, SANS cumul comme le ferait em), mais
# sur une base FIXE (--pc-rem, posée par sheet-extra.css) indépendante de Roll20.
# Un digit est exigé devant « rem » : ni « em » (letter-spacing) ni « --pc-rem » ne matchent.
_REM = re.compile(r"(-?[\d.]+)rem\b")


def sync_creation_css():
    css = CREATION_CSS_SRC.read_text(encoding="utf-8")
    css, n = _REM.subn(r"calc(\1 * var(--pc-rem, 16px))", css)
    CREATION_CSS_DST.write_text(css, encoding="utf-8")
    print(f"[extension] creation.css synchronisé depuis {CREATION_CSS_SRC.relative_to(ROOT)} "
          f"({n} valeurs rem -> calc(--pc-rem))")


# Le créateur de personnage tourne à l'IDENTIQUE dans Roll20 (même code) : on embarque
# creation.js et ses données. creation.js lit/écrit localStorage ; dans l'iframe de
# l'extension on redirige sa persistance vers les Attributes Roll20 en SHUNTANT son
# localStorage — sans toucher son code : on enveloppe la source dans une fonction dont
# le paramètre `localStorage` masque le global pour toute la durée de creation.js.
CREATION_JS_SRC = ROOT / "docs" / "javascripts" / "creation.js"
CREATION_JS_EMBED = FF / "creation-embed.js"
# creation.json (données de règles) est généré en mémoire par hooks/creation.py au build
# du site (écrit dans site/creation.json). On le recopie dans le paquet de l'extension.
CREATION_JSON_SRC = ROOT / "site" / "creation.json"
CREATION_JSON_DST = FF / "creation.json"


def sync_creator_assets():
    if not CREATION_JSON_SRC.exists():
        raise SystemExit("site/creation.json absent : lancer d'abord `mkdocs build` "
                         "(hooks/creation.py le génère).")
    shutil.copyfile(CREATION_JSON_SRC, CREATION_JSON_DST)
    src = CREATION_JS_SRC.read_text(encoding="utf-8")
    wrapped = (
        "/* GÉNÉRÉ par build_extension.py — NE PAS ÉDITER. */\n"
        "/* creation.js du site, enveloppé pour que son `localStorage` pointe vers le\n"
        "   shim de l'iframe (persistance -> Attributes Roll20). Le paramètre masque le\n"
        "   global sur toute la source ; aucune ligne de creation.js n'est modifiée. */\n"
        ";(function (localStorage) {\n"
        + src +
        "\n})(window.__hxhLocalStorage || window.localStorage);\n"
    )
    CREATION_JS_EMBED.write_text(wrapped, encoding="utf-8")
    print(f"[extension] creation.json ({CREATION_JSON_DST.stat().st_size} o) + "
          f"creation-embed.js (creation.js enveloppé) synchronisés")


def _write(out, files):
    """files : liste de (source_sur_disque, chemin_dans_archive)."""
    DL.mkdir(parents=True, exist_ok=True)
    if out.exists():
        out.unlink()
    arcs = []
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for src, arc in sorted(files, key=lambda p: p[1]):
            z.write(src, arc)
            arcs.append(arc)
    assert "manifest.json" in arcs, f"manifest.json absent de la racine de {out.name}"
    print(f"[extension] {out.relative_to(ROOT)} — {out.stat().st_size} octets, {len(arcs)} fichiers")
    return arcs


def build():
    sync_creation_css()
    sync_creator_assets()
    # Firefox : tout extension/firefox/ tel quel.
    ff_files = [(p, p.relative_to(FF).as_posix()) for p in FF.rglob("*") if p.is_file()]
    _write(OUT_FF, ff_files)

    # Chrome : manifest V3 + tous les fichiers partagés de firefox/ SAUF son manifest.json.
    shared = [(p, arc) for (p, arc) in ff_files if arc != "manifest.json"]
    chrome_files = [(CHROME_MANIFEST, "manifest.json")] + shared
    _write(OUT_CHROME, chrome_files)


if __name__ == "__main__":
    build()
