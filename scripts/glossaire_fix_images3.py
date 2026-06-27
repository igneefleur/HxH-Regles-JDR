# -*- coding: utf-8 -*-
"""3e passage : derniers récalcitrants. Fichier précis pour le supertanker
(MV Sirius Star) + recherches très ciblées pour adulte/enfant/bowling/farine.
Usage : python scripts/glossaire_fix_images3.py"""
import urllib.request, urllib.parse, json, re, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")

API = "https://commons.wikimedia.org/w/api.php"
UA = "HxH-RPG-glossary/1.0 (personal educational project)"
OUT = "docs/assets/glossaire"
IDX = f"{OUT}/_index.json"

BAD = re.compile(r"(painting|drawing|sketch|lithograph|engraving|diagram|\.svg|\.tif"
                 r"|icon|pictogram|nude|naked|newspaper|press|employees|factory|tower|advertisement|design)", re.I)

FILES = {}
REDO = {
    "farine": "dumbbell weight fitness gym",
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
                print("   429"); time.sleep(25 * (i + 1)); continue
            raise


def strip(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s or "")).strip()


def meta(p):
    ii = (p.get("imageinfo") or [{}])[0]
    thumb = ii.get("thumburl") or ii.get("url")
    em = ii.get("extmetadata", {})
    artist = re.sub(r"\s*\(.*?\)\s*$", "", strip(em.get("Artist", {}).get("value", "")))[:55]
    lic = strip(em.get("LicenseShortName", {}).get("value", ""))
    return thumb, artist, lic


def by_title(title):
    d = api({"action": "query", "titles": "File:" + title, "prop": "imageinfo",
             "iiprop": "url|extmetadata", "iiurlwidth": 500})
    for p in d.get("query", {}).get("pages", {}).values():
        if "imageinfo" in p:
            t, a, l = meta(p)
            return (t, a, l, "File:" + title) if t else None
    return None


def find(query):
    d = api({"action": "query", "generator": "search", "gsrnamespace": 6,
             "gsrsearch": query, "gsrlimit": 20, "prop": "imageinfo",
             "iiprop": "url|extmetadata", "iiurlwidth": 500})
    pages = sorted(d.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 999))
    for p in pages:
        title = p.get("title", "")
        if not re.search(r"\.(jpe?g|png)$", title, re.I) or BAD.search(title):
            continue
        t, a, l = meta(p)
        if t:
            return t, a, l, title
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
jobs = [(s, ("file", t)) for s, t in FILES.items()] + [(s, ("query", q)) for s, q in REDO.items()]
for slug, (kind, val) in jobs:
    try:
        r = by_title(val) if kind == "file" else find(val)
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
