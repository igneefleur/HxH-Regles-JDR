"""Télécharge une illustration SFW par archétype depuis l'API Danbooru.

Garde-fous : recherche filtrée sur rating:general uniquement (contenu tout
public). Images sous copyright — usage privé du projet de fan.
"""
import io
import json
import os
import sys
import urllib.parse
import urllib.request

from PIL import Image

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "assets", "archetypes")
OUT = os.path.abspath(OUT)

UA = "hxh-jdr-fanproject/1.0 (private fan rpg, contact via github)"

# Toutes les vignettes au même format portrait (recadrage « cover », tête en haut).
BOX_W, BOX_H = 600, 760

# slug d'archétype -> tag de personnage sur Danbooru
CHARS = {
    "renforceur":               "gon_freecss",
    "emitteur":                 "franklin_bordeau",
    "transmuteur":              "hisoka_morow",
    "manipulateur":             "illumi_zoldyck",
    "conjurateur":              "shizuku_murasaki",
    "specialiste":              "chrollo_lucilfer",
    "renforceur-emitteur":      "leorio_paladiknight",
    "renforceur-transmuteur":   "killua_zoldyck",
    "emitteur-manipulateur":    "kalluto_zoldyck",
    "transmuteur-conjurateur":  "hanzo_(hunter_x_hunter)",
    "manipulateur-specialiste": "neferpitou",
    "conjurateur-specialiste":  "kurapika",
}

# Posts Danbooru imposés (priment sur la recherche) — slug -> id de post.
POST_OVERRIDE = {
    "transmuteur-conjurateur": 7350507,   # Kite, choisi à la main
}


def api(tag):
    q = urllib.parse.urlencode({"tags": f"{tag} rating:general", "limit": 100})
    url = f"https://danbooru.donmai.us/posts.json?{q}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def api_post(post_id):
    url = f"https://danbooru.donmai.us/posts/{post_id}.json"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def cover_crop(img, w, h):
    """Remplit la boîte w×h en gardant le ratio (façon object-fit: cover),
    ancré en haut au centre pour préserver le visage."""
    scale = max(w / img.width, h / img.height)
    new = (round(img.width * scale), round(img.height * scale))
    img = img.resize(new, Image.LANCZOS)
    left = (img.width - w) // 2          # centré horizontalement
    top = 0                              # ancré en haut (on garde la tête)
    return img.crop((left, top, left + w, top + h))


def score(post):
    """Préférence : solo, portrait (ratio 0.5–1.05), bonne résolution, score haut."""
    w, h = post.get("image_width", 0), post.get("image_height", 0)
    if not w or not h:
        return -1
    tags = post.get("tag_string", "")
    ratio = w / h
    s = post.get("score", 0)
    bonus = 0
    if "solo" in tags:
        bonus += 300
    if 0.5 <= ratio <= 1.05:      # portrait ou carré
        bonus += 200
    elif ratio <= 1.4:
        bonus += 60
    if min(w, h) >= 700:
        bonus += 80
    return bonus + s


def best_url(post):
    for key in ("file_url", "large_file_url"):
        u = post.get(key)
        if u and post.get("file_ext") in ("jpg", "jpeg", "png", "webp"):
            return u
    return None


def fetch_image(url):
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Referer": "https://danbooru.donmai.us/"}
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main():
    os.makedirs(OUT, exist_ok=True)
    only = set(sys.argv[1:])  # ne traiter que ces slugs si précisés
    for slug, tag in CHARS.items():
        if only and slug not in only:
            continue

        # Post imposé à la main : priorité absolue.
        if slug in POST_OVERRIDE:
            try:
                p = api_post(POST_OVERRIDE[slug])
                raw = fetch_image(best_url(p))
                img = cover_crop(Image.open(io.BytesIO(raw)).convert("RGB"), BOX_W, BOX_H)
                img.save(os.path.join(OUT, f"{slug}.png"), "PNG")
                print(f"[FIX ] {slug:26} <- post #{p['id']:>8}  (imposé)")
            except Exception as e:
                print(f"[ERR ] {slug:26} — post imposé {POST_OVERRIDE[slug]}: {e}")
            continue

        try:
            posts = api(tag)
        except Exception as e:
            print(f"[ERR ] {slug:26} ({tag}) — API: {e}")
            continue
        posts = [p for p in posts if best_url(p)]
        if not posts:
            print(f"[MISS] {slug:26} ({tag}) — aucun résultat exploitable")
            continue
        posts.sort(key=score, reverse=True)
        for p in posts[:8]:
            url = best_url(p)
            try:
                raw = fetch_image(url)
                img = cover_crop(Image.open(io.BytesIO(raw)).convert("RGB"), BOX_W, BOX_H)
            except Exception as e:
                print(f"        retry {slug}: {e}")
                continue
            dest = os.path.join(OUT, f"{slug}.png")
            img.save(dest, "PNG")
            print(f"[ OK ] {slug:26} <- post #{p['id']:>8}  {p['image_width']}x{p['image_height']}  score={p.get('score',0)}")
            break
        else:
            print(f"[MISS] {slug:26} ({tag}) — échec de tous les candidats")


if __name__ == "__main__":
    main()
