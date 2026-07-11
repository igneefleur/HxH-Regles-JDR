"""Packe l'extension Firefox en .xpi téléchargeable depuis le site.

Zippe extension/firefox/ vers docs/download/hxh-roll20-firefox.xpi avec des
séparateurs « / » (Compress-Archive de PowerShell 5.1 écrit des « \\ » que
Firefox ne sait pas lire). Le manifest.json doit se trouver à la racine de
l'archive.

    python scripts/build_extension.py
"""
import os
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "extension" / "firefox"
OUT = ROOT / "docs" / "download" / "hxh-roll20-firefox.xpi"


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        OUT.unlink()
    entries = []
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(SRC.rglob("*")):
            if path.is_file():
                arc = path.relative_to(SRC).as_posix()
                z.write(path, arc)
                entries.append(arc)
    assert "manifest.json" in entries, "manifest.json absent de la racine de l'archive"
    print(f"[extension] {OUT.relative_to(ROOT)} — {OUT.stat().st_size} octets, {len(entries)} fichiers")
    return entries


if __name__ == "__main__":
    build()
