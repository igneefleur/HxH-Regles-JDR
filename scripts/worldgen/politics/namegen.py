# -*- coding: utf-8 -*-
"""Archetypes culturels (familles), banques phonetiques (noms INVENTES evoquant une sonorite
reelle sans emprunter de mots reels), et pool de TRADITIONS avec axes de CONFLIT.

Utilise par cultures.py, religions.py, country_names.py.
"""

# ---- TRADITIONS : (id, libelle FR, axe, pole). Deux cultures s'opposent si elles tiennent
#      des poles CONTRAIRES du meme axe (explique pourquoi elles ne se melangent pas). ----
TRADITIONS = {
    'hier':   ("Hiérarchie stricte", "autorite", +1),
    'egal':   ("Assemblées égalitaires", "autorite", -1),
    'clan':   ("Clans et lignages", "parente", +1),
    'cite':   ("Cité et citoyen", "parente", -1),
    'honn':   ("Honneur guerrier", "guerre", +1),
    'paix':   ("Voie pacifique", "guerre", -1),
    'march':  ("Vocation marchande", "echange", +1),
    'autar':  ("Repli et autarcie", "echange", -1),
    'ecrit':  ("Loi écrite", "savoir", +1),
    'oral':   ("Mémoire orale", "savoir", -1),
    'mer':    ("Gens de la mer", "milieu", +1),
    'terre':  ("Gens de la terre", "milieu", -1),
    'purte':  ("Rites de pureté", "purete", +1),
    'syncr':  ("Syncrétisme ouvert", "purete", -1),
    'matri':  ("Matrilinéarité", "genre", +1),
    'patri':  ("Patrilinéarité", "genre", -1),
    'talion': ("Loi du talion", "justice", +1),
    'repar':  ("Justice réparatrice", "justice", -1),
    'hosp':   ("Hospitalité rituelle", "hospit", 0),
    'ancet':  ("Culte des ancêtres", "temps", 0),
    'nomad':  ("Errance saisonnière", "sol", 0),
    'monum':  ("Bâtisseurs de monuments", "oeuvre", 0),
}

# ---- ARCHETYPES : affinite geographique + phonemes + traditions probables ----
# features: cold, warm, equator, interior, coastal, highland, island, large  (poids)
def _b(onset, vowel, coda, end):
    return dict(onset=onset.split(), vowel=vowel.split(), coda=coda.split(), end=end.split())

ARCH = {
 'boreal': dict(label="boréal", aff=dict(cold=2.2, coastal=1.0, large=0.3),
    phon=_b("sk st fr gr hv thr br dr vr sn hj",
            "a o u ei au y ja", "rn ld rk st nn ss rd", "-a -orn -und -ek -reth -veld"),
    trad=['terre', 'honn', 'clan', 'oral', 'ancet']),
 'steppe': dict(label="steppique", aff=dict(warm=0.6, interior=2.0, large=1.6, cold=0.5),
    phon=_b("t k b q kh z ts y j g",
            "a u o ai uu ya", "n r l gh q sh", "-ai -un -agh -ur -kai -ol"),
    trad=['nomad', 'clan', 'honn', 'hier', 'oral']),
 'desert': dict(label="désertique", aff=dict(warm=1.6, interior=1.6),
    phon=_b("q s z h kh r m n sh dh",
            "a i u aa ai", "r n m d z l", "-ir -an -ad -ur -im -saf"),
    trad=['hier', 'march', 'purte', 'patri', 'hosp']),
 'equator': dict(label="équatorial", aff=dict(equator=2.4, warm=1.0, coastal=0.6),
    phon=_b("m b k ng nz mb w t nd bw",
            "a o u e i", "", "-a -o -we -ando -umbe -eza"),
    trad=['clan', 'oral', 'ancet', 'matri', 'terre']),
 'highland': dict(label="montagnard", aff=dict(highland=2.6, interior=0.8),
    phon=_b("k t p ch tz q w x kh chr",
            "a i u ay au", "k l n tz q", "-aq -uk -in -aya -oc -itl"),
    trad=['monum', 'ancet', 'hier', 'terre', 'purte']),
 'maritime': dict(label="maritime", aff=dict(coastal=2.4, warm=0.4),
    phon=_b("v fl br tr st l m d kl sp",
            "e i a o ae au", "l r n s st rt", "-ia -es -ard -ent -oor -mar"),
    trad=['mer', 'march', 'cite', 'ecrit', 'syncr']),
 'latin': dict(label="méridional", aff=dict(warm=1.4, coastal=1.2),
    phon=_b("v l r s c f br gr pr t",
            "a e i o au", "l r n s", "-ia -eno -oro -ella -ano -etra"),
    trad=['cite', 'ecrit', 'march', 'monum', 'hier']),
 'sinitic': dict(label="grand-fleuve", aff=dict(warm=0.8, large=1.8, coastal=0.7, interior=0.6),
    phon=_b("zh x q sh l h j ch t g",
            "a i e ao u ia", "ng n", "-ang -ong -ei -an -uo -ai"),
    trad=['hier', 'ecrit', 'ancet', 'terre', 'monum']),
 'nipponic': dict(label="insulaire d'orient", aff=dict(island=2.2, coastal=1.0),
    phon=_b("k s t sh m r h y n ts",
            "a i u e o", "n", "-o -a -shi -ku -ra -no"),
    trad=['honn', 'hier', 'purte', 'ancet', 'mer']),
 'indic': dict(label="des moussons", aff=dict(warm=1.6, coastal=0.8, large=0.8),
    phon=_b("bh dh r v s k pr sh j n",
            "a i u aa ia", "r n sh t", "-ara -ita -vann -esh - apur -oda"),
    trad=['hier', 'purte', 'syncr', 'monum', 'ancet']),
 'savanna': dict(label="des savanes", aff=dict(warm=1.6, interior=1.2),
    phon=_b("m k s w b nd ng t g z",
            "a o e u i", "", "-ana -oro -ele -adi -umi -asa"),
    trad=['clan', 'oral', 'matri', 'nomad', 'ancet']),
 'gaelic': dict(label="des brumes", aff=dict(cold=1.4, coastal=1.6, island=0.8),
    phon=_b("c br dr ll m gl f sh cr t",
            "ai ei o u ao ia", "gh nn ll rn dh", "-agh -mor -nach -veil -loe -dun"),
    trad=['clan', 'oral', 'honn', 'ancet', 'terre']),
 'tundra': dict(label="polaire", aff=dict(cold=3.0),
    phon=_b("n t k q s y ch p ng",
            "a u i aa", "q k t n", "-uk -aq -tuk -naq -lik -vut"),
    trad=['nomad', 'oral', 'egal', 'terre', 'hosp']),
 'persic': dict(label="des plateaux", aff=dict(highland=1.4, warm=1.0, interior=1.2),
    phon=_b("sh z r kh p f b g d n",
            "a i e u aa", "r n z sh", "-ar -uz -esh -ad -yar -dun"),
    trad=['hier', 'ecrit', 'march', 'monum', 'purte']),
}
ARCH_KEYS = list(ARCH.keys())
FEATURES = ['cold', 'warm', 'equator', 'interior', 'coastal', 'highland', 'island', 'large']


def _clean(s):
    out = []
    for ch in s:
        if len(out) >= 2 and out[-1] == ch and out[-2] == ch:
            continue
        out.append(ch)
    r = ''.join(out).strip('-')
    return r


def make_name(arch, rng, nsyl=None):
    b = ARCH[arch]['phon']
    if nsyl is None:
        nsyl = int(rng.choice([2, 2, 3]))
    s = ''
    for _ in range(nsyl):
        s += rng.choice(b['onset']) + rng.choice(b['vowel'])
    if b['coda'] and rng.random() < 0.45:
        s += rng.choice(b['coda'])
    if rng.random() < 0.78:
        s += rng.choice(b['end'])
    s = _clean(s)
    return s[:1].upper() + s[1:]


def traditions_for(arch, rng, n=None):
    """Choisit n traditions coherentes (jamais deux poles opposes du meme axe)."""
    if n is None:
        n = int(rng.choice([3, 3, 4]))
    pool = list(ARCH[arch]['trad'])
    extra = [t for t in TRADITIONS if t not in pool]
    rng.shuffle(extra)
    cand = pool + extra
    chosen = []
    used_axis = {}
    for t in cand:
        name, axis, pole = TRADITIONS[t]
        if pole != 0 and used_axis.get(axis, None) == -pole:
            continue                       # eviter la contradiction interne
        chosen.append(t)
        if pole != 0:
            used_axis[axis] = pole
        if len(chosen) >= n:
            break
    return chosen


def conflict_score(tradsA, tradsB):
    """Nb de paires de traditions en OPPOSITION (meme axe, poles contraires)."""
    c = 0
    for a in tradsA:
        na, axa, pa = TRADITIONS[a]
        if pa == 0:
            continue
        for b in tradsB:
            nb, axb, pb = TRADITIONS[b]
            if axa == axb and pa == -pb:
                c += 1
    return c
