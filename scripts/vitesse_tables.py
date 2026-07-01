# -*- coding: utf-8 -*-
"""Génère les tableaux de « vitesse d'apprentissage » (cadence par Éclat + niveau
atteint au fil du temps) et les insère, entre des marqueurs <!-- AUTO:… -->, dans
les pages où ils s'appliquent : points-formation.md (niveau/PF) et di.md
(prestige/DI). La courbe vit dans les constantes ci-dessous ; le texte explicatif,
lui, est en dur dans les pages.
Usage : python scripts/vitesse_tables.py"""
import math, re, sys
sys.stdout.reconfigure(encoding="utf-8")

PF = "docs/content/regles/personnage/points-formation.md"
DI = "docs/content/regles/nen/di.md"

W = 3                                            # niveaux par cran de cadence
COLS = ["1-3", "4-6", "7-9", "10-12", "13-15", "16-18"]
NC = len(COLS)
DURS = [("1 mois", 1 / 12), ("2 mois", 2 / 12), ("3 mois", 3 / 12), ("6 mois", 6 / 12),
        ("1 an", 1), ("2 ans", 2), ("3 ans", 3), ("5 ans", 5), ("10 ans", 10),
        ("20 ans", 20), ("30 ans", 30), ("50 ans", 50), ("100 ans", 100)]
LADDER = {1: "10/décennie", 2: "10/an", 3: "10/semestre", 4: "10/trimestre", 5: "10/mois",
          6: "10/semaine", 7: "10/jour", 8: "10/demi-journée", 9: "10/heure", 10: "10/minute"}
RATE = {1: 1.0, 2: 10.0, 3: 20.0, 4: 40.0, 5: 120.0, 6: 521.4, 7: 3652.5, 8: 7305.0,
        9: 87660.0, 10: 5259600.0}
INST = 11   # rangs >= INST : instantané


def period(r):
    return "−" if r <= 0 else ("instantané" if r >= INST else LADDER[r])


def rate(r):
    return 0.0 if r <= 0 else (float("inf") if r >= INST else RATE[r])


def acc(base, T):
    ct = cpf = 0.0
    P = 0
    while True:
        r = rate(base - P)
        hi = (P + 1) * 100 * W
        if r == 0:
            return cpf
        if math.isinf(r):
            cpf = hi
            P += 1
            continue
        dt = (hi - cpf) / r
        if ct + dt > T:
            return cpf + (T - ct) * r
        ct += dt
        cpf = hi
        P += 1


def lvl(p):
    return 0 if p <= 0 else math.ceil(p / 100)


def htable(group, off, dur=False, prefix=""):
    """Tableau HTML à double en-tête (titre de groupe + libellés de colonnes),
    « Éclat » à gauche sur deux rangs. Sans classe de table, pour hériter du style."""
    if dur:
        col_headers = [lbl for lbl, _ in DURS]
        rows = [[str(e)] + [str(lvl(acc(e // 5 + off, yr))) for _, yr in DURS] for e in range(0, 51, 5)]
    else:
        col_headers = [f"{prefix} {c}" for c in COLS]
        rows = [[str(e)] + [period(e // 5 + off - P) for P in range(NC)] for e in range(0, 51, 5)]
    n = len(col_headers)
    h = '<div class="eclat-grid">\n<table>\n<thead>\n'
    h += f'<tr><th rowspan="2">Éclat</th><th colspan="{n}">{group}</th></tr>\n'
    h += "<tr>" + "".join(f"<th>{c}</th>" for c in col_headers) + "</tr>\n"
    h += "</thead>\n<tbody>\n"
    for r in rows:
        h += "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>\n"
    h += "</tbody>\n</table>\n</div>"
    return h


def insert(path, key, html):
    text = open(path, encoding="utf-8").read()
    s, e = f"<!-- AUTO:{key} -->", f"<!-- /AUTO:{key} -->"
    pat = re.compile(re.escape(s) + r".*?" + re.escape(e), re.DOTALL)
    if not pat.search(text):
        raise SystemExit(f"marqueur « {key} » introuvable dans {path}")
    text = pat.sub(lambda _m: s + "\n" + html + "\n" + e, text, count=1)
    open(path, "w", encoding="utf-8", newline="\n").write(text)
    print(f"  {path} : {key} mis à jour")


# Niveau / Points de formation et Prestige / Développement intérieur partagent la
# même courbe (offset 4) : seuls les libellés diffèrent.
insert(PF, "pf-cadence", htable("Points de formation", 4, prefix="Niveau"))
insert(PF, "pf-temps", htable("Niveau", 4, dur=True))
insert(DI, "di-cadence", htable("Développement intérieur (Nen)", 4, prefix="Prestige"))
insert(DI, "di-temps", htable("Prestige", 4, dur=True))
print("Tables de vitesse régénérées.")
