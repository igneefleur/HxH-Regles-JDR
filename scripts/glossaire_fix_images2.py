# -*- coding: utf-8 -*-
"""2e passage : re-télécharge les images encore inadaptées, avec des requêtes à
exclusions ciblées (-museum -painting -jupiter ...) et un filtre allégé.
Usage : python scripts/glossaire_fix_images2.py"""
import urllib.request, urllib.parse, json, re, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")

API = "https://commons.wikimedia.org/w/api.php"
UA = "HxH-RPG-glossary/1.0 (personal educational project)"
OUT = "docs/assets/glossaire"
IDX = f"{OUT}/_index.json"

BAD = re.compile(r"(painting|drawing|sketch|lithograph|engraving|etching|art_project"
                 r"|\.svg|\.tif|icon|pictogram|woodcut|chromolithograph)", re.I)

REDO = {
    "farine": "wheat flour paper bag",
    "trot": "horse trotting race -drawing -lithograph -print -currier -engraving",
    "cuirasse": "battleship warship underway -museum -horse -race",
    "adulte": "man standing full body -blind -paralysed -wellcome -medical -patient",
    "sonde": "Voyager spacecraft probe model -jupiter -saturn -planet -spot -neptune",
    "statue-liberte": "Statue of Liberty island -fire -attack -WTC -trade",
    "enfant": "child boy standing -dyck -portrait -painting -drawing",
    "satellite": "artificial satellite spacecraft -diagram -molniya -orbit -planet -saturn",
    "supertanker": "crude oil tanker ship underway -museum -model -inland",
}


def api(params, tries=6):
    params = {**params, "format": "json"}
    url = API + "?" + urllib.parse.urlencode(params)
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < tries - 1:
                print("   429, pause", 25 * (i + 1)); time.sleep(25 * (i + 1)); continue
            raise


def strip(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s or "")).strip()


def find(query):
    d = api({"action": "query", "generator": "search", "gsrnamespace": 6,
             "gsrsearch": query, "gsrlimit": 20, "prop": "imageinfo",
             "iiprop": "url|extmetadata", "iiurlwidth": 500})
    pages = list(d.get("query", {}).get("pages", {}).values())
    pages.sort(key=lambda p: p.get("index", 999))
    for p in pages:
        title = p.get("title", "")
        if not re.search(r"\.(jpe?g|png)$", title, re.I) or BAD.search(title):
            continue
        ii = (p.get("imageinfo") or [{}])[0]
        thumb = ii.get("thumburl") or ii.get("url")
        if not thumb:
            continue
        em = ii.get("extmetadata", {})
        artist = re.sub(r"\s*\(.*?\)\s*$", "", strip(em.get("Artist", {}).get("value", "")))[:55]
        lic = strip(em.get("LicenseShortName", {}).get("value", ""))
        return thumb, artist, lic, title
    return None


def download(url, path, tries=5):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as rr, open(path, "wb") as f:
                f.write(rr.read())
            return
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < tries - 1:
                time.sleep(20 * (i + 1)); continue
            raise


res = json.load(open(IDX, encoding="utf-8"))
for slug, q in REDO.items():
    try:
        r = find(q)
        if not r:
            print("MISS", slug); continue
        thumb, artist, lic, title = r
        old = res.get(slug, {}).get("file")
        if old and os.path.exists(f"{OUT}/{old}"):
            os.remove(f"{OUT}/{old}")
        m = re.search(r"\.(jpe?g|png)", thumb.split("?")[0], re.I)
        ext = m.group(1).lower() if m else "jpg"
        download(thumb, f"{OUT}/{slug}.{ext}")
        res[slug] = {"file": f"{slug}.{ext}", "artist": artist or "Wikimedia Commons",
                     "lic": lic, "page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))}
        print("OK ", slug, "->", res[slug]["file"], "|", artist, "|", title[:55])
        json.dump(res, open(IDX, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        time.sleep(3)
    except Exception as e:
        print("ERR", slug, "|", repr(e)[:80]); time.sleep(3)
print("FAIT")
