# -*- coding: utf-8 -*-
"""Re-télécharge les images inadaptées du glossaire avec de meilleures requêtes
et un filtre strict (exclut tableaux/dessins/icônes/diagrammes/plages...).
Met à jour docs/assets/glossaire/_index.json. Usage : python scripts/glossaire_fix_images.py"""
import urllib.request, urllib.parse, json, re, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")

API = "https://commons.wikimedia.org/w/api.php"
UA = "HxH-RPG-glossary/1.0 (personal educational project)"
OUT = "docs/assets/glossaire"
IDX = f"{OUT}/_index.json"

BAD = re.compile(r"(painting|drawing|sketch|engraving|lithograph|etching|illustration"
                 r"|\bart\b|artwork|google_art|icon|pictogram|symbol|silhouette|outline"
                 r"|diagram|comparison|\bchart\b|\bmap\b|beach|fresco|mural|cartoon|logo"
                 r"|seal|coat[_ ]of[_ ]arms|flag|emblem|\.svg|\.tif|museum|drawing)", re.I)

REDO = {
    "farine": "flour bag baking white sack",
    "galop": "racehorse running gallop",
    "trot": "trotting horse harness racing",
    "cuirasse": "Iowa class battleship warship sea",
    "adulte": "man standing full length portrait photograph",
    "semi-remorque": "semi trailer truck motorway road",
    "sonde": "Voyager spacecraft space probe",
    "statue-liberte": "Statue of Liberty New York harbor",
    "personne": "woman standing full length portrait photograph",
    "pyramide": "Pyramids of Giza Necropolis",
    "porte-avions": "Nimitz class aircraft carrier underway sea",
    "cheval": "brown horse standing meadow",
    "enfant": "young boy standing portrait child",
    "sprint": "sprinter sprint running track athletics 100 metres",
    "marche": "pedestrian walking sidewalk street",
    "satellite": "communications satellite orbit Earth space",
    "bowling": "ten pin bowling ball",
    "supertanker": "crude oil supertanker tanker ship sea",
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
                print("   429, pause", 25 * (i + 1), "s"); time.sleep(25 * (i + 1)); continue
            raise


def strip(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s or "")).strip()


def find(query):
    d = api({"action": "query", "generator": "search", "gsrnamespace": 6,
             "gsrsearch": query, "gsrlimit": 15, "prop": "imageinfo",
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
        # supprime l'ancien fichier (extension éventuellement différente)
        old = res.get(slug, {}).get("file")
        if old and os.path.exists(f"{OUT}/{old}"):
            os.remove(f"{OUT}/{old}")
        m = re.search(r"\.(jpe?g|png)", thumb.split("?")[0], re.I)
        ext = m.group(1).lower() if m else "jpg"
        download(thumb, f"{OUT}/{slug}.{ext}")
        res[slug] = {"file": f"{slug}.{ext}", "artist": artist or "Wikimedia Commons",
                     "lic": lic, "page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))}
        print("OK ", slug, "->", res[slug]["file"], "|", artist, "|", lic, "|", title[:50])
        json.dump(res, open(IDX, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        time.sleep(3)
    except Exception as e:
        print("ERR", slug, "|", repr(e)[:80]); time.sleep(3)
print("FAIT")
