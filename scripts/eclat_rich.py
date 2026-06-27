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
("0", "L'humain ordinaire, l'immense majorité des gens. Aucun don à la naissance : tout ce qu'il devient, il l'arrache au travail, et lentement. La plupart mènent une vie honnête sans rien accomplir qu'on retienne."),
("5", "L'individu doué, qui se détache dans son domaine sans toujours savoir pourquoi : l'athlète naturel, l'élève qui comprend du premier coup, l'artisan dont les mains savent avant l'esprit. Son talent le porte au-dessus de ses pairs, mais il reste dans l'ordinaire humain."),
("10", "Un talent rare, de ceux qu'une génération produit à peine. L'élite par nature : les meilleurs chasseurs, les maîtres de leur art, ceux dont le don saute aux yeux. Là où le commun s'épuise, eux paraissent à peine forcer."),
("15", "Le prodige, né pour les sommets. Il apprend à une vitesse fulgurante et saisit en quelques semaines ce qu'il faut des années à d'autres pour seulement effleurer. On dit de lui qu'il était fait pour cela."),
("20", "Le génie qui dépasse les prodiges eux-mêmes et redéfinit ce que son art croyait possible. À ce degré, le talent semble déjà toucher la limite de ce qu'on imagine un homme capable de porter."),
("25", "Un talent monstrueux, si vaste qu'il inquiète autant qu'il fascine. Ce que d'autres mettent une vie à conquérir, il l'effleure presque sans effort ; son don semble défier l'ordre des choses."),
("30", "Un don aux confins de ce qu'on tient pour humain, qui paraît ne plus rien devoir à la nature. À ce point, le talent ressemble déjà à autre chose qu'un talent, et l'on peine à croire qu'un homme l'ait reçu en naissant."),
("35", "Le génie effrayant, dont l'intelligence et l'instinct ploient le monde à leur volonté. Rien ne lui résiste longtemps, et sa seule existence glace ceux qui en mesurent la portée."),
("40", "Une puissance innée sans égale. Né au sommet, doté d'un don qu'on n'imagine pas humain, il est l'apogée du vivant : ce que les autres appellent prouesse n'est pour lui qu'un point de départ."),
("45", "Au-delà des plus grands. Un talent de légende, qui surpasse les êtres les plus exceptionnels que le monde ait connus ; on n'en rencontre qu'une poignée à travers les âges."),
("50", "L'extrême sommet, à la lisière de ce qu'un être vivant peut incarner. Un don que rien d'autre, parmi tout ce qui vit, n'égale, et qui n'a plus de point de comparaison."),
("55 et au-delà", "L'Éclat dépasse alors tout ce que le vivant peut contenir : il n'a plus de commune mesure, et l'échelle n'y connaît plus de limite supérieure."),
]
tierblock = '<div class="eclat-tiers" markdown>\n\n' + "\n\n".join(f"**Éclat {n}** {d}" for n, d in tiers) + '\n\n</div>'

doc = f"""# Éclat

<div class="cols" markdown>

<div class="keep" markdown>

L'Éclat est le talent d'un personnage à sa naissance : le don qu'il a reçu avant d'avoir rien appris, et que nul effort ne lui aurait accordé. C'est la part la plus rare et la plus fondamentale d'un être ; elle ne se gagne pas, elle se possède dès le premier souffle et l'accompagne sa vie durant.

</div>

<div class="keep" markdown>

Tout le reste s'acquiert. Un personnage forge ses [caractéristiques](caracteristiques.md), apprend ses [compétences](competences.md) et suit ses [formations](formations.md), au prix d'une vie de travail. L'Éclat, lui, ne se travaille pas : aucun effort ne le fait monter d'un cran, et il trace la limite vers laquelle tout ce travail tend. On peut cultiver cette terre ; la bouleverser, presque jamais.

</div>

<div class="keep" markdown>

Il décide de deux choses, et de deux seulement. D'abord, jusqu'où un personnage peut aller : c'est l'Éclat qui fixe le plafond de ses caractéristiques et le sommet de son art. Ensuite, à quelle vitesse il y parvient : à effort égal, le plus doué progresse plus vite, et continue d'avancer là où un autre a depuis longtemps cessé. L'Éclat n'accorde par lui-même aucun pouvoir ni aucun point ; il n'est qu'une mesure, mais c'est la mesure de tout ce qui reste possible.

</div>

<div class="keep" markdown>

### Attribuer un Éclat

Les personnages-joueurs n'ont pas une vie ordinaire : les évènements les cherchent et c'est souvent à eux de dénouer ce qui doit l'être. Ceux qui font une histoire portent en eux quelque chose de plus, et l'Éclat mesure cette étoffe.

</div>

<div class="keep" markdown>

Un personnage-joueur reçoit donc d'ordinaire un Éclat supérieur au tout-venant. Le MJ fixe celui de chaque personnage à sa création, selon le ton de sa table et la place qu'il lui donne. Un Éclat de 10 convient à la plupart : assez rare pour le distinguer sans l'arracher au commun. On réserve 15 aux véritables prodiges, promis dès l'enfance aux plus hauts sommets. En deçà, le personnage se fond dans la foule ; bien au-delà, il dépasse ce qu'on conçoit d'un être humain.

</div>

<div class="keep" markdown>

### L'échelle de l'Éclat

L'Éclat se compte par paliers de cinq, de 0 (l'humain ordinaire) jusqu'à 50 et au-delà. Entre deux paliers, on retient toujours le palier inférieur : un Éclat de 4 relève du palier 0, un Éclat de 17 du palier 15. Chaque palier dit ce qu'un être porte en lui dès la naissance.

</div>

{tierblock}

<div class="keep" markdown>

### Changer d'Éclat en cours de vie

L'Éclat est donné à la naissance, et rien dans la vie ordinaire ne le déplace : ni l'entraînement, ni les années, ni la volonté. Il existe pourtant des moments rares où un être se révèle à lui-même et où son talent, jusque-là endormi, bascule d'un palier ou plus. Ce ne sont pas des progrès patients mais des éveils : ils surviennent d'un coup, ou pas du tout.

</div>

<div class="keep" markdown>

Un tel bouleversement peut naître d'un exploit qui dépasse tout ce que le personnage se croyait capable d'accomplir ; de la rencontre d'un être dont l'Éclat écrase le sien et lui ouvre les yeux sur ce qu'il pourrait devenir ; d'une situation mortelle traversée et survécue, qui arrache de lui une force ignorée ; ou de toute autre épreuve qui marque une vie. Le MJ juge seul si l'instant le mérite, et de combien l'Éclat se déplace.

</div>

</div>

---

## La vitesse d'apprentissage

L'Éclat ne dit pas seulement jusqu'où un personnage peut aller : il commande aussi l'allure à laquelle il y parvient. À effort égal, même maître, mêmes heures, le plus doué va toujours plus vite et progresse encore longtemps après que l'autre a touché son plafond. Les tableaux qui suivent traduisent cette différence en chiffres.

On les lit ainsi : à la ligne de son Éclat et dans la colonne de son palier actuel, un personnage qui s'entraîne gagne dix points par période indiquée, selon le cas tous les jours, toutes les semaines ou tous les ans. La courbe est partout la même : un départ rapide où les premiers paliers tombent en quelques jours, puis un ralentissement régulier, jusqu'à un sommet qui ne se conquiert qu'après des décennies. Le tiret marque la fin du chemin : le talent ne mène pas plus loin et nul entraînement n'y changera rien.

Deux progressions avancent en parallèle. Les [points de formation](points-formation.md) nourrissent le niveau : l'avancement ordinaire de toute discipline, ouvert à tous. Le développement intérieur nourrit le prestige, qui mesure la [maîtrise du Nen](conjuration.md) : plus exigeant et plus lent, à la portée de chacun, mais sans Éclat un personnage n'en tire qu'une compétence modeste, payée d'une vie entière. Dans les deux cas, cent points valent un palier.

{htable("Points de formation", 3, prefix="Niveau")}

{htable("Développement intérieur (Nen)", 2, prefix="Prestige")}

Au-delà du palier 16-18, la cadence continue de la même façon, perdant un cran tous les trois niveaux jusqu'à « par an » ; ensuite, le talent ne mène pas plus loin et la progression cesse.

### Au fil des années

Les tableaux précédents donnent la cadence ; ceux qui suivent en montrent le fruit, pour qui s'entraîne chaque jour sans relâche. On y lit le niveau, puis le prestige, atteints selon l'Éclat et le nombre d'années d'entraînement. La colonne n'indique pas l'âge mais la durée écoulée depuis le début de l'entraînement : on compte d'ordinaire la formation à partir de dix ans, et le Nen à partir de vingt.

{htable("Niveau", 3, dur=True)}

{htable("Prestige", 2, dur=True)}
"""
open(F, "w", encoding="utf-8", newline="\n").write(doc)
print("eclat.md réécrit avec en-têtes doubles ; tables :", doc.count("<table>"))
