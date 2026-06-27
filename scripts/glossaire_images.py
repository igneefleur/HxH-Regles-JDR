# -*- coding: utf-8 -*-
"""Télécharge une image libre (Wikimedia Commons) par sujet du glossaire dans
docs/assets/glossaire/, avec auteur + licence + lien de la fiche. Phase 1 :
recherche + téléchargement. Usage : python scripts/glossaire_images.py"""
import urllib.request, urllib.parse, json, re, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")

API = "https://commons.wikimedia.org/w/api.php"
UA = "HxH-RPG-glossary/1.0 (personal educational project)"
OUT = "docs/assets/glossaire"
os.makedirs(OUT, exist_ok=True)


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
                print("   429, pause", 25 * (i + 1), "s...")
                time.sleep(25 * (i + 1))
                continue
            raise


def strip(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s or "")).strip()


BAD = re.compile(r"(logo|map|diagram|chart|icon|seal|coat[_ ]of[_ ]arms|flag|emblem|svg|\.tif)", re.I)


def find(query):
    # recherche + métadonnées en UNE requête (generator=search)
    d = api({"action": "query", "generator": "search", "gsrnamespace": 6,
             "gsrsearch": query, "gsrlimit": 12, "prop": "imageinfo",
             "iiprop": "url|extmetadata", "iiurlwidth": 500})
    pages = list(d.get("query", {}).get("pages", {}).values())
    pages.sort(key=lambda p: p.get("index", 999))
    for p in pages:
        title = p.get("title", "")
        if not re.search(r"\.(jpe?g|png)$", title, re.I):
            continue
        if BAD.search(title):
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
            return True
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < tries - 1:
                time.sleep(20 * (i + 1))
                continue
            raise


SLUG_Q = {
    "telephone": "smartphone phone", "bouteille": "plastic water bottle",
    "ordinateur": "laptop computer", "bebe": "newborn infant baby",
    "farine": "flour bag", "bowling": "bowling ball", "ciment": "cement bag",
    "valise": "suitcase travel", "enfant": "child kid portrait",
    "saint-bernard": "Saint Bernard dog", "personne": "woman standing full length",
    "adulte": "man standing full length", "refrigerateur": "refrigerator fridge",
    "panda": "giant panda", "lion": "male lion", "ours": "brown bear",
    "cheval": "draft horse", "voiture": "compact car hatchback",
    "rhinoceros": "white rhinoceros", "elephant": "African bush elephant",
    "autobus": "city bus", "semi-remorque": "semi truck trailer",
    "char": "main battle tank", "locomotive": "diesel locomotive",
    "baleine-bleue": "blue whale", "statue-liberte": "Statue of Liberty",
    "a380": "Airbus A380 aircraft", "cargo": "cargo ship", "peniche": "river barge",
    "fregate": "frigate warship", "tour-eiffel": "Eiffel Tower",
    "sous-marin": "submarine navy", "cuirasse": "battleship",
    "titanic": "RMS Titanic ship", "paquebot": "cruise ship ocean liner",
    "porte-avions": "aircraft carrier", "porte-conteneurs": "container ship",
    "supertanker": "oil tanker ship", "gratte-ciel": "skyscraper",
    "pyramide": "Great Pyramid Giza", "barrage": "Three Gorges Dam",
    "colline": "green hill landscape", "montagne": "mountain peak",
    "navire": "small cargo ship", "escargot": "garden snail",
    "marche": "pedestrian walking", "footing": "jogging runner park",
    "course": "running race athletics", "sprint": "sprint athletics track",
    "cycliste": "road bicycle racing", "trot": "horse trotting",
    "bolt": "Usain Bolt", "galop": "galloping horse", "levrier": "greyhound dog",
    "guepard": "cheetah running", "autoroute": "highway motorway traffic",
    "train": "high-speed train", "sport": "sports car", "tgv": "TGV train",
    "helice": "propeller aircraft", "avion": "airliner aircraft flying",
    "jet": "fighter jet aircraft", "sr71": "SR-71 Blackbird",
    "hypersonique": "hypersonic missile", "capsule": "space capsule reentry",
    "satellite": "satellite spacecraft orbit", "sonde": "space probe spacecraft",
    "cosmos": "stars night sky", "netero": "lightning bolt",
}

IDX = f"{OUT}/_index.json"
res = json.load(open(IDX, encoding="utf-8")) if os.path.exists(IDX) else {}
for slug, q in SLUG_Q.items():
    if slug in res and os.path.exists(f"{OUT}/{res[slug]['file']}"):
        continue  # reprise : déjà fait
    try:
        r = find(q)
        if not r:
            print("MISS", slug, "|", q)
            continue
        thumb, artist, lic, title = r
        m = re.search(r"\.(jpe?g|png)", thumb.split("?")[0], re.I)
        ext = m.group(1).lower() if m else "jpg"
        download(thumb, f"{OUT}/{slug}.{ext}")
        res[slug] = {"file": f"{slug}.{ext}",
                     "artist": artist or "Wikimedia Commons", "lic": lic,
                     "page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))}
        print("OK ", slug, "->", res[slug]["file"], "|", artist, "|", lic)
        json.dump(res, open(IDX, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        time.sleep(2.5)
    except Exception as e:
        print("ERR", slug, "|", repr(e)[:80])
        time.sleep(2.5)

print("TOTAL", len(res), "/", len(SLUG_Q))
