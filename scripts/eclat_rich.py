# -*- coding: utf-8 -*-
"""Réécrit eclat.md : texte riche (façon Gnose d'Anima) + tableaux HTML à double
en-tête (titre de groupe au-dessus des colonnes, « Éclat » à gauche sur deux rangs)."""
import math, sys
sys.stdout.reconfigure(encoding="utf-8")
F = "docs/content/livre/eclat.md"
W = 3
COLS = ["1-3", "4-6", "7-9", "10-12", "13-15", "16-18"]
NC = len(COLS)
DURS = [1, 2, 3, 5, 10, 20, 30, 50, 100]
LADDER = {1: "10/an", 2: "10/trimestre", 3: "10/mois", 4: "10/semaine",
          5: "10/jour", 6: "10/heure", 7: "10/minute"}
RATE = {1: 10.0, 2: 40.0, 3: 120.0, 4: 521.4, 5: 3652.5, 6: 87660.0, 7: 5259600.0}


def period(r):
    return "−" if r <= 0 else ("instantané" if r >= 8 else LADDER[r])


def rate(r):
    return 0.0 if r <= 0 else (float("inf") if r >= 8 else RATE[r])


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
    """Tableau HTML : 1re rangée d'en-tête = « Éclat » (rowspan) + titre de groupe
    (colspan) ; 2e rangée = libellés de colonnes. Sans classe, pour hériter du style."""
    if dur:
        col_headers = [f"{d} an" if d == 1 else f"{d} ans" for d in DURS]
        rows = [[str(e)] + [str(lvl(acc(e // 5 + off, d))) for d in DURS] for e in range(0, 51, 5)]
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


tiers = [
("0", "L'humain ordinaire, et l'immense majorité des gens. Il ne reçoit aucun don à la naissance : tout ce qu'il devient, il l'arrache à la force du travail, et lentement. La plupart de ceux qui portent cet Éclat mènent une vie honnête sans jamais rien accomplir que l'on retienne."),
("5", "L'individu doué, celui qui se détache dans son domaine sans toujours savoir pourquoi : l'athlète naturel, l'élève qui comprend du premier coup, l'artisan dont les mains semblent savoir avant l'esprit. Son talent est réel et le porte au-dessus de ses pairs, mais il reste de part en part dans l'ordinaire humain."),
("10", "Un talent rare, de ceux qu'une génération produit à peine. C'est l'élite par nature : les meilleurs chasseurs, les maîtres de leur art, ceux dont le don saute aux yeux de quiconque les regarde à l'œuvre. Là où le commun s'épuise, eux paraissent à peine forcer."),
("15", "Le prodige, né pour les sommets. Il apprend à une vitesse à couper le souffle et saisit en quelques semaines ce qu'il faut des années à d'autres pour seulement effleurer. On le reconnaît du premier regard, et l'on dit de lui qu'il était fait pour cela."),
("20", "Le génie qui dépasse les prodiges eux-mêmes et redéfinit ce que son art croyait possible. À ce degré, le talent semble déjà toucher la limite de ce qu'on imagine un homme capable de porter."),
("25", "Un talent monstrueux, si vaste qu'il inquiète autant qu'il fascine. Ce que d'autres mettent une vie à conquérir, il l'effleure presque sans effort, et son don semble défier l'ordre des choses."),
("30", "Un don aux confins de ce qu'on tient pour humain, qui paraît ne plus rien devoir à la nature. À ce point, le talent ressemble déjà à autre chose qu'un talent, et l'on peine à croire qu'un homme l'ait reçu en naissant."),
("35", "Le génie effrayant, dont l'intelligence et l'instinct ploient le monde à leur seule volonté. Rien ne lui résiste longtemps, et sa seule existence suffit à glacer ceux qui en mesurent la portée."),
("40", "Une puissance innée sans égale. Né au sommet, doté d'un don que l'on n'imagine pas humain, il est l'apogée du vivant : ce que les autres appellent prouesse n'est pour lui qu'un point de départ."),
("45", "Au-delà des plus grands. Un talent qui appartient déjà à la légende et surpasse les êtres les plus exceptionnels que le monde ait connus ; on n'en rencontre qu'une poignée à travers les âges."),
("50", "L'extrême sommet, à la lisière de ce qu'un être vivant peut incarner. Un don que rien d'autre, parmi tout ce qui vit, n'égale, et qui n'a plus de point de comparaison."),
("55 et au-delà", "L'Éclat dépasse alors tout ce que le vivant peut contenir : il n'a plus de commune mesure, et l'échelle n'y connaît plus de limite supérieure."),
]
tierblock = '<div class="eclat-tiers" markdown>\n\n' + "\n\n".join(f"**Éclat {n}** {d}" for n, d in tiers) + '\n\n</div>'

doc = f"""# Éclat

<div class="cols" markdown>

L'Éclat est le talent d'un personnage à sa naissance : le don qu'il a reçu avant d'avoir rien appris, et que nul effort ne lui aurait accordé. C'est la part la plus rare et la plus fondamentale d'un être ; elle ne se gagne pas, elle se possède dès le premier souffle et l'accompagne sa vie durant.

Tout le reste s'acquiert. Un personnage forge ses [caractéristiques](caracteristiques.md), apprend ses [compétences](competences.md) et suit ses [formations](formations.md), au prix d'une vie de travail. L'Éclat, lui, ne se travaille pas : aucun effort ne le fait monter d'un cran, et il trace la limite vers laquelle tout ce travail tend. On peut cultiver cette terre ; la bouleverser, presque jamais.

Il décide de deux choses, et de deux seulement. D'abord, jusqu'où un personnage peut aller : c'est l'Éclat qui fixe le plafond de ses caractéristiques et le sommet de son art. Ensuite, à quelle vitesse il y parvient : à effort égal, le plus doué progresse plus vite, et continue d'avancer là où un autre a depuis longtemps cessé. L'Éclat n'accorde par lui-même aucun pouvoir ni aucun point ; il n'est qu'une mesure, mais c'est la mesure de tout ce qui reste possible.

### Attribuer un Éclat

Les personnages-joueurs ne sont pas des gens comme les autres : leur vie n'a rien d'ordinaire. Les évènements les cherchent, les rencontres hors du commun se pressent sur leur route, et c'est souvent à eux seuls qu'il revient de dénouer ce qui doit l'être. Un forgeron qui passe sa vie à battre le fer dans son échoppe ne fait pas une histoire ; ceux qui en font une portent en eux quelque chose de plus, et l'Éclat mesure cette étoffe.

Aussi un personnage-joueur reçoit-il, d'ordinaire, un Éclat supérieur à celui du tout-venant. C'est au MJ, et à lui seul, de fixer celui de chaque personnage à sa création, selon le ton de sa table et la place qu'il entend lui donner dans le monde. Un Éclat de 10 conviendra à la plupart, assez rare pour le distinguer sans l'arracher au commun ; on réservera 15 aux véritables prodiges, promis dès l'enfance aux plus hauts sommets. En deçà, le personnage se fondrait dans la foule des gens sans relief ; bien au-delà, il dépasserait ce que l'on conçoit d'un être humain.

### L'échelle de l'Éclat

L'Éclat se compte par paliers de cinq, de 0, l'humain ordinaire, jusqu'à 50 et au-delà. Entre deux paliers, on retient toujours le palier inférieur : un Éclat de 4 relève du palier 0, un Éclat de 17 du palier 15. Chaque palier dit ce qu'un être porte en lui dès la naissance, sans rien lui accorder de plus.

{tierblock}

### Changer d'Éclat en cours de vie

L'Éclat est donné à la naissance, et rien dans la vie ordinaire ne le déplace : ni l'entraînement, ni les années, ni la volonté la plus farouche. Il est pourtant des moments, rares et brûlants, où un être se révèle à lui-même et où son talent, jusque-là endormi, bascule d'un palier, parfois davantage. Ce ne sont jamais des progrès patients, mais des éveils : ils surviennent d'un coup, ou pas du tout.

Un tel bouleversement peut naître d'un exploit qui dépasse tout ce que le personnage se croyait capable d'accomplir ; de la rencontre d'un être dont l'Éclat écrase le sien, et dont la seule présence lui ouvre les yeux sur ce qu'il pourrait devenir ; d'une situation mortelle traversée et survécue, qui arrache de lui une force qu'il ignorait porter ; ou de toute autre épreuve qui marque une vie à jamais. C'est au MJ, et à lui seul, de juger si l'instant le mérite, et de combien l'Éclat se déplace.

</div>

---

## La vitesse d'apprentissage

L'Éclat ne dit pas seulement jusqu'où un personnage peut aller : il commande aussi l'allure à laquelle il y parvient. Deux êtres peuvent fournir le même effort, suivre le même maître, s'entraîner les mêmes heures ; le plus doué ira toujours plus vite, et continuera de progresser longtemps après que l'autre aura touché son plafond. Les tableaux qui suivent traduisent cette différence en chiffres.

On les lit ainsi : à la ligne de son Éclat et dans la colonne de son palier actuel, un personnage qui s'entraîne gagne dix points par période indiquée, dix tous les jours, toutes les semaines ou tous les ans selon le cas. La courbe est partout la même, et c'est elle qui fait le sel de l'Éclat : un départ rapide, où les premiers paliers tombent en quelques jours, puis un ralentissement régulier, jusqu'à un sommet qui ne se conquiert qu'au terme de décennies. Le tiret marque la fin du chemin : à ce stade, le talent ne mène pas plus loin, et nul entraînement n'y changera rien.

Deux progressions avancent en parallèle. Les points de formation nourrissent le niveau (voir [Points de formation](points-formation.md)) : c'est l'avancement ordinaire, celui de toute discipline, ouvert à tous. Le développement intérieur nourrit le prestige, qui mesure la maîtrise du Nen (voir [Conjuration](conjuration.md)) : plus exigeant et plus lent, il reste à la portée de chacun, mais sans Éclat un personnage n'en tire jamais qu'une compétence modeste, payée d'une vie entière. Dans les deux cas, cent points valent un palier.

{htable("Points de formation", 3, prefix="Niveau")}

{htable("Développement intérieur (Nen)", 2, prefix="Prestige")}

Au-delà du palier 16-18, la cadence continue de la même façon, perdant un cran tous les trois niveaux jusqu'à « par an » ; ensuite, le talent ne mène pas plus loin et la progression cesse.

### Au fil des années

Les tableaux précédents donnent la cadence ; ceux qui suivent en montrent le fruit, pour qui s'entraîne chaque jour sans relâche. On y lit le niveau, puis le prestige, atteints selon l'Éclat et le nombre d'années d'entraînement. La colonne n'indique pas l'âge du personnage, mais la durée écoulée depuis qu'il s'y est mis : on compte d'ordinaire la formation à partir de dix ans, et le Nen à partir de vingt.

{htable("Niveau", 3, dur=True)}

{htable("Prestige", 2, dur=True)}
"""
open(F, "w", encoding="utf-8").write(doc)
print("eclat.md réécrit avec en-têtes doubles ; tables :", doc.count("<table>"))
