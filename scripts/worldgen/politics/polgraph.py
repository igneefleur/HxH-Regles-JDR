"""Graphe politique partage : charge les pays (countries.npz/json) et construit
l'adjacence terrestre (longueur + barriere de montagne), les liens MARITIMES (detroits),
et les stats geo par pays. Utilise par cultures / religions / noms / puissance.
"""
import os, json, numpy as np
from scipy import ndimage
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__))

SEA_LINK_PX = 0.055        # portee d'un lien maritime (fraction de largeur) ~ detroit franchissable


class Pol:
    pass


def load():
    g = np.load(os.path.join(HERE, 'geo.npz'))
    c = np.load(os.path.join(HERE, 'countries.npz'))
    with open(os.path.join(HERE, 'countries.json'), encoding='utf-8') as f:
        cj = json.load(f)
    P = Pol()
    P.land = g['land'].astype(bool); P.elev = g['elev'].astype(np.float32)
    P.labels = c['labels'].astype(np.int32); P.cont = c['cont'].astype(np.int32)
    P.cont_of = c['cont_of'].astype(np.int32); P.K = int(c['K']); P.ncont = int(c['ncont'])
    P.H, P.W = P.labels.shape
    st = {s['id']: s for s in cj['stats']}
    K = P.K
    P.area = np.array([st[i]['area'] for i in range(1, K + 1)], np.float64)
    P.fx = np.array([st[i]['fx'] for i in range(1, K + 1)], np.float64)
    P.fy = np.array([st[i]['fy'] for i in range(1, K + 1)], np.float64)
    P.cy = np.array([st[i]['cy'] for i in range(1, K + 1)], np.float64)
    P.cx = np.array([st[i]['cx'] for i in range(1, K + 1)], np.float64)
    P.mean_elev = np.array([st[i]['mean_elev'] for i in range(1, K + 1)], np.float64)
    P.max_elev = np.array([st[i]['max_elev'] for i in range(1, K + 1)], np.float64)
    P.coast_px = np.array([st[i]['coast_px'] for i in range(1, K + 1)], np.float64)
    P.coastal = np.array([st[i]['coastal'] for i in range(1, K + 1)], bool)
    P.continent = np.array([st[i]['continent'] for i in range(1, K + 1)], np.int32)  # 1..ncont
    # index 0-based par pays : idx i (0..K-1) == label i+1
    P.st = st

    # ---- adjacence terrestre + barriere de montagne le long de la frontiere ----
    labels = P.labels; elev = P.elev
    adj = {}          # (i,j)->border length (i<j, labels 1..K)
    bmtn = {}         # (i,j)->max elev le long de la frontiere
    for dy, dx in ((1, 0), (0, 1)):
        a = labels[:-1, :] if dy else labels[:, :-1]
        b = labels[1:, :] if dy else labels[:, 1:]
        ea = elev[:-1, :] if dy else elev[:, :-1]
        eb = elev[1:, :] if dy else elev[:, 1:]
        m = (a != b) & (a > 0) & (b > 0)
        pa = a[m]; pb = b[m]; pe = np.maximum(ea[m], eb[m])
        for i, j, e in zip(pa.tolist(), pb.tolist(), pe.tolist()):
            k = (i, j) if i < j else (j, i)
            adj[k] = adj.get(k, 0) + 1
            if e > bmtn.get(k, -1e9):
                bmtn[k] = e
    P.adj = {}
    for (i, j), n in adj.items():
        P.adj.setdefault(i, {})[j] = n
        P.adj.setdefault(j, {})[i] = n
    P.border_mtn = bmtn

    # ---- liens MARITIMES : cotes de pays differents proches a travers la mer ----
    coast = P.land ^ ndimage.binary_erosion(P.land, structure=np.ones((3, 3)))
    ys, xs = np.where(coast)
    lab_c = labels[ys, xs]
    keep = lab_c > 0
    ys, xs, lab_c = ys[keep], xs[keep], lab_c[keep]
    sub = slice(None, None, 2)                       # sous-echantillonne
    pts = np.column_stack([ys[sub], xs[sub]]).astype(np.float64)
    labp = lab_c[sub]
    tree = cKDTree(pts)
    D = SEA_LINK_PX * P.W
    sea = {}                                          # (i,j)->min gap px
    pairs = tree.query_pairs(r=D, output_type='ndarray')
    if len(pairs):
        li = labp[pairs[:, 0]]; lj = labp[pairs[:, 1]]
        dd = np.sqrt(((pts[pairs[:, 0]] - pts[pairs[:, 1]]) ** 2).sum(1))
        diff = li != lj
        for i, j, d in zip(li[diff].tolist(), lj[diff].tolist(), dd[diff].tolist()):
            if d < 6:            # trop proche = deja adjacence terrestre
                continue
            k = (i, j) if i < j else (j, i)
            if d < sea.get(k, 1e18):
                sea[k] = d
    P.sea = {}
    for (i, j), d in sea.items():
        if j in P.adj.get(i, {}):    # deja voisins terrestres
            continue
        P.sea.setdefault(i, {})[j] = d
        P.sea.setdefault(j, {})[i] = d
    return P


def graph_edges(P, mtn_pen=2.2, sea_pen=2.6, cont_pen=3.0, sea_D=None):
    """Retourne dict i->list[(j, cost)] : cout de propagation d'un trait (culture/religion)
    d'un pays a l'autre. Montagne = barriere ; mer = barriere plus forte ; autre continent = forte."""
    if sea_D is None:
        sea_D = SEA_LINK_PX * P.W
    E = {}
    for i in P.adj:
        for j, blen in P.adj[i].items():
            k = (i, j) if i < j else (j, i)
            mt = P.border_mtn.get(k, 0.0)
            mtn = max(0.0, (mt - 0.12) / 0.6)         # 0 plaine -> ~1 haute montagne
            samecont = P.continent[i - 1] == P.continent[j - 1]
            cost = 1.0 + mtn_pen * min(mtn, 1.2) + (0.0 if samecont else cont_pen)
            E.setdefault(i, []).append((j, cost))
    for i in P.sea:
        for j, d in P.sea[i].items():
            samecont = P.continent[i - 1] == P.continent[j - 1]
            frac = d / sea_D
            cost = 1.0 + sea_pen * (0.5 + frac) + (0.0 if samecont else 0.6 * cont_pen)
            E.setdefault(i, []).append((j, cost))
    return E


if __name__ == '__main__':
    P = load()
    ncoast = int(P.coastal.sum())
    nse = sum(len(v) for v in P.sea.values()) // 2
    print(f'K={P.K} continents={P.ncont} cotiers={ncoast} liens_maritimes={nse}')
    deg = [len(P.adj.get(i, {})) for i in range(1, P.K + 1)]
    print('degre terrestre moy', round(np.mean(deg), 2), 'max', max(deg))
    print('aires: min', int(P.area.min()), 'med', int(np.median(P.area)), 'max', int(P.area.max()))
