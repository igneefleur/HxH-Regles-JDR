#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scrape tous les utilisateurs de Nen (6 categories de type) du wiki HxH,
extrait le template {{Abilities}} de chaque page, sort dataset JSON + markdown."""
import subprocess, json, re, io, sys, os

API = "https://hunterxhunter.fandom.com/api.php"
OUT = os.path.dirname(os.path.abspath(__file__))

def call(params):
    args = ["curl", "-sS", "-m", "90", "-G", API]
    for k, v in params:
        args += ["--data-urlencode", "%s=%s" % (k, v)]
    r = subprocess.run(args, capture_output=True)
    return json.loads(r.stdout.decode("utf-8", "replace"))

# 1) union des categories de type
CATS = ["Emitters", "Enhancers", "Transmuters", "Manipulators", "Conjurers", "Specialists"]
CATFR = {"Emitters":"Émission","Enhancers":"Renforcement","Transmuters":"Transmutation",
         "Manipulators":"Manipulation","Conjurers":"Conjuration","Specialists":"Spécialisation"}
title_types = {}
for c in CATS:
    d = call([("action","query"),("list","categorymembers"),("cmtitle","Category:"+c),
              ("cmlimit","500"),("cmtype","page"),("format","json"),("formatversion","2")])
    for m in d.get("query",{}).get("categorymembers",[]):
        title_types.setdefault(m["title"], []).append(CATFR[c])
titles = sorted(title_types)
sys.stderr.write("TOTAL utilisateurs de Nen: %d\n" % len(titles))

# 2) contenu par lots de 50
def batches(lst, n):
    for i in range(0, len(lst), n): yield lst[i:i+n]
pages = {}
for b in batches(titles, 50):
    d = call([("action","query"),("prop","revisions"),("rvprop","content"),("rvslots","main"),
              ("titles","|".join(b)),("format","json"),("formatversion","2")])
    # normalization map (title redirects)
    for p in d.get("query",{}).get("pages",[]):
        rev = p.get("revisions")
        if rev:
            pages[p["title"]] = rev[0]["slots"]["main"]["content"]

# 3) parsing
def clean(t):
    if t is None: return ""
    t = re.sub(r"<ref[^>]*>.*?</ref>", "", t, flags=re.S)
    t = re.sub(r"<ref[^>]*/>", "", t)
    t = re.sub(r"\{\{Ruby\|([^|}]*)\|[^}]*\}\}", r"\1", t)
    t = re.sub(r"\{\{Jap\|([^|}]*)[^}]*\}\}", r"\1", t)
    t = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", t)
    t = re.sub(r"\[\[([^\]]*)\]\]", r"\1", t)
    t = re.sub(r"\{\{[^{}]*\}\}", "", t)
    t = t.replace("'''", "").replace("''", "")
    t = re.sub(r"<br ?/?>", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def match_brace(s, i):
    depth = 0; j = i
    while j < len(s):
        if s[j:j+2] == "{{": depth += 1; j += 2; continue
        if s[j:j+2] == "}}":
            depth -= 1; j += 2
            if depth == 0: return j
            continue
        j += 1
    return len(s)

def split_fields(body):
    """Split top-level |key=value fields respecting {{}} and [[]] depth."""
    fields = {}
    depth_c = 0; depth_l = 0; cur = ""; segs = []
    i = 0
    while i < len(body):
        two = body[i:i+2]
        if two == "{{": depth_c += 1; cur += two; i += 2; continue
        if two == "}}": depth_c -= 1; cur += two; i += 2; continue
        if two == "[[": depth_l += 1; cur += two; i += 2; continue
        if two == "]]": depth_l -= 1; cur += two; i += 2; continue
        ch = body[i]
        if ch == "|" and depth_c == 0 and depth_l == 0:
            segs.append(cur); cur = ""; i += 1; continue
        cur += ch; i += 1
    segs.append(cur)
    for seg in segs:
        if "=" in seg:
            k, v = seg.split("=", 1)
            fields[k.strip()] = v.strip()
    return fields

def jap_name(v):
    m = re.search(r"\{\{Jap\|([^|}]*)", v)
    if m: return m.group(1).strip()
    return clean(v)

def parse_abilities(wt):
    out = []
    idx = 0
    while True:
        i = wt.find("{{Abilities", idx)
        if i < 0: break
        j = match_brace(wt, i)
        body = wt[i+len("{{Abilities"):j-2]
        f = split_fields(body)
        # collect ability1..N
        n = 1
        while ("ability%d" % n) in f:
            out.append({
                "name": jap_name(f.get("ability%d" % n, "")),
                "type": clean(f.get("nentype%d" % n, "") or f.get("nentype", "")),
                "desc": clean(f.get("desc%d" % n, "")),
            })
            n += 1
        idx = j
    return out

def infobox_type(wt):
    m = re.search(r"\|\s*type\s*=\s*(.+)", wt)
    return clean(m.group(1)) if m else ""

def abilities_section(wt):
    m = re.search(r"==\s*Abilities.*?==", wt)
    if not m: return ""
    start = m.end()
    nxt = re.search(r"\n==[^=]", wt[start:])
    seg = wt[start: start + (nxt.start() if nxt else 4000)]
    return clean(seg)[:600]

data = []
for t in titles:
    wt = pages.get(t, "")
    ab = parse_abilities(wt)
    data.append({
        "name": t,
        "categories": title_types[t],
        "infoboxType": infobox_type(wt),
        "abilities": ab,
        "hasTemplate": bool(ab),
        "fallback": "" if ab else abilities_section(wt),
    })

with io.open(os.path.join(OUT, "nen_all.json"), "w", encoding="utf-8") as fh:
    json.dump(data, fh, ensure_ascii=False, indent=1)

# markdown
with io.open(os.path.join(OUT, "nen_all.md"), "w", encoding="utf-8") as fh:
    fh.write("# Utilisateurs de Nen — extraction wiki (%d)\n\n" % len(data))
    for d in data:
        fh.write("## %s — %s\n" % (d["name"], "/".join(d["categories"])))
        if d["abilities"]:
            for a in d["abilities"]:
                fh.write("- **%s** [%s] : %s\n" % (a["name"] or "?", a["type"] or "?", a["desc"]))
        elif d["fallback"]:
            fh.write("- _(pas de template)_ %s\n" % d["fallback"])
        else:
            fh.write("- _(rien extrait)_\n")
        fh.write("\n")

# summary to stderr
wt_ok = sum(1 for d in data if d["hasTemplate"])
n_ab = sum(len(d["abilities"]) for d in data)
sys.stderr.write("Avec template: %d / %d | abilities totales: %d\n" % (wt_ok, len(data), n_ab))
sys.stderr.write("Sans template (a traiter): %s\n" % ", ".join(d["name"] for d in data if not d["hasTemplate"]))
print("OK")
