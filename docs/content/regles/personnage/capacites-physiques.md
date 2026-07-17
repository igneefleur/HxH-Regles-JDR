# Capacités physiques

<div class="cols" markdown>

Les capacités physiques mesurent ce que le corps d'un personnage accomplit sans jet de dé : la distance qu'il franchit, le bond qu'il fait, la charge qu'il soulève, la portée de son lancer, le souffle qu'il retient, la profondeur qu'il supporte. Chacune découle d'une [caractéristique](caracteristiques.md) physique et se lit dans une table. Ce chapitre en définit six : le [Mouvement](#mouvement), issu de l'Agilité ; le [Saut](#saut), le [Port](#port) et le [Lancer](#lancer), issus de la Force ; l'[Apnée](#retenir-son-souffle) et la [Pression](#pression-aquatique), issues de l'Endurance. Il définit d'abord ce qu'elles partagent : la lecture des tables, la [Fatigue](#la-fatigue), l'[activité](#activite), le sommeil et le fond.

Sur l'échelle des caractéristiques, notée de 0 à 30, 5 est la moyenne humaine et 9 le plafond humain réel.

<div class="keep" markdown>

### Lire une capacité

Chaque capacité est une valeur du personnage, qui porte son nom : son Mouvement, son Saut, son Port, son Lancer, son Apnée, sa Pression. Cette valeur est égale à la caractéristique dont la capacité découle : le Mouvement d'un personnage est égal à son Agilité, son Port à sa Force.

Chaque capacité tient dans une table de trente et une lignes, une par valeur de la capacité, de 0 à 30. Chaque ligne est désignée par sa valeur : la ligne 5 est celle du Mouvement 5. La plupart des tables portent trois colonnes, une par intensité d'[activité](#activite) : Légère, Intermédiaire et Lourde. Les autres portent leurs propres colonnes, que leur capacité explique.

Lire une capacité consiste à croiser une ligne et une colonne. Par défaut, la ligne est la valeur de la capacité du personnage ; chaque capacité précise comment se détermine la colonne. Aucun jet de dé n'intervient : la valeur lue s'applique telle quelle. Quels que soient les bonus et les malus, on ne lit jamais sous la ligne 0 ni au-delà de la ligne 30.

</div>

</div>

---

<div class="cols" markdown>

### La Fatigue {#la-fatigue}

Les points de fatigue mesurent les réserves du corps. La Fatigue découle de l'Endurance : la Fatigue d'un personnage est égale à son Endurance, et c'est son maximum de points de fatigue ; bien reposé, il les possède tous.

Quand il fait un jet, un personnage peut consommer des points de fatigue pour se dépasser : chaque point consommé donne +15 au jet, jusqu'à cinq points par jet, soit +75 au plus. Il l'annonce avant de lancer les dés, et tout jet y a droit, jets de Résistance à l'Épuisement compris.

Un personnage perd aussi des points de fatigue quand il rate un jet de [Résistance à l'Épuisement](competences.md) : il en perd un par tranche de vingt points manquants au seuil, sa marge d'échec. Rater de 20 à 39 en fait perdre un, de 40 à 59 deux, et ainsi de suite ; rater de moins de 20 n'en fait perdre aucun. Ce jet ne se fait pas n'importe quand : on le fait en forçant sur l'effort ou sur l'éveil, comme décrit plus bas ([Forcer l'effort](#forcer-leffort), [Veiller sans dormir](#veiller-sans-dormir)).

Les points de fatigue peuvent descendre sous zéro, qu'ils soient consommés ou perdus. Chaque point sous zéro donne −10 à tous les jets du personnage, jets de Résistance à l'Épuisement compris : à −1 il subit −10, à −3 il subit −30. Ce malus vaut pour les jets suivants : il ne touche pas le jet qui vient de créer ces points.

Quand ses points de fatigue tombent à son maximum en négatif, ou en dessous, le personnage s'effondre d'épuisement et sombre dans l'[Inconscience](etats.md) : avec une Fatigue de 8, il s'effondre à −8. Un personnage peut se dépenser jusqu'à s'effondrer : le jet se résout d'abord, puis il tombe. L'effondrement se poursuit en sommeil : le personnage ne peut pas être réveillé avant d'avoir dormi le temps de sommeil que demande son [Repos](#sommeil-et-repos), et ce sommeil compte comme correct.

Les points de fatigue ne remontent qu'en dormant correctement. Dormir correctement, c'est dormir au moins le temps de sommeil que demande son [Repos](#sommeil-et-repos), donné par la table du sommeil. Ce sommeil ramène les points de fatigue au maximum, remet à zéro le compte des jets d'effort ([Forcer l'effort](#forcer-leffort)) et redonne les durées d'activité de la journée. Le personnage repart frais.

### Activité {#activite}

Une activité est tout ce qu'un personnage fait de son corps, du repos au combat. On ne classe pas le geste lui-même mais l'effort fourni, en trois intensités : légère, intermédiaire ou lourde.

Un personnage est toujours dans une seule intensité à la fois : celle de son effort le plus intense du moment. S'il fait plusieurs choses en même temps, seule la plus exigeante compte.

Pour classer une activité, on la compare aux exemples ci-dessous ; en cas de doute, le MJ tranche.

<div class="defs" markdown>

**Légère :** un effort minime, soutenu toute la journée sans peine, qui n'entame jamais les réserves. C'est l'intensité ordinaire d'une journée éveillée : ni heures ni fatigue à compter. Par exemple : marcher d'un pas tranquille, flâner ; cuisiner, ranger un campement, jardiner sans forcer ; lire, étudier, dessiner une carte, converser ; monter la garde, faire le guet, voyager assis ; s'étirer, répéter des gestes lents.

**Intermédiaire :** un effort moyen, tenable de longues heures avec des pauses. Le personnage transpire et fournit un travail réel sans se mettre à bout : le rythme d'une vraie journée de labeur. Par exemple : randonner sac au dos, marcher vite, trottiner longtemps ; fendre du bois, creuser, manier la pioche, charrier des charges ; travailler à la forge, aux champs ou sur un chantier ; nager, ramer, pédaler à rythme régulier.

**Lourde :** un gros effort à pleine puissance, à l'intensité maximale du corps. Le personnage se dépense sans retenue et puise dans ses réserves : il ne tient ce rythme qu'un temps limité avant de réclamer du repos. Par exemple : combattre, en duel ou en mêlée ; sprinter, fuir, poursuivre à toutes jambes ; pousser le corps à sa limite lors d'un exploit.

</div>

#### Sommeil et repos {#sommeil-et-repos}

Le Repos découle de l'Endurance : le Repos d'un personnage est égal à son Endurance, et c'est à sa ligne que se lit sa table, en bas de section. Chaque jour, un personnage a besoin du temps de sommeil que demande son Repos. Un personnage qui a dormi correctement commence sa journée bien reposé, sans malus.

Un sommeil plus court que le temps requis ne redonne rien : ni points de fatigue, ni réserves d'effort. En revanche, un sommeil interrompu peut reprendre : on additionne tout ce que le personnage dort depuis son dernier sommeil correct, et dès que le total atteint son temps de sommeil requis, il a dormi correctement.

Un personnage ne peut pas se rendormir aussitôt après un sommeil correct : il doit d'abord rester éveillé un temps minimal, la moitié de son temps avant d'être fatigué ([Veiller sans dormir](#veiller-sans-dormir)). Un sommeil trop court pour être correct n'impose pas ce délai. La table du sommeil, ci-dessous, donne les deux durées, aux colonnes Avant de pouvoir redormir et Avant d'être fatigué.

<p class="formula">Temps avant de pouvoir redormir = temps avant d'être fatigué ÷ 2</p>

#### Le Fond {#le-fond}

Le Fond découle de l'Endurance : le Fond d'un personnage est égal à son Endurance. C'est l'endurance de son corps à l'effort soutenu, lue à sa ligne dans la table du Fond, en bas de section : la durée d'activité intermédiaire et la durée d'activité lourde qu'il peut fournir dans une journée sans rien risquer.

La colonne Activité intermédiaire donne la durée totale d'activité intermédiaire qu'un personnage peut fournir dans sa journée ; la colonne Activité lourde, la durée totale d'activité lourde. Les deux durées se dépensent séparément ; le reste de la journée se passe en activité légère, qui ne se compte pas. Un sommeil correct rend les deux durées en entier.

<div class="memo" markdown>

Exemple. Avec une Endurance de 5, la moyenne humaine, un personnage dort 8 heures ; son Fond lui donne jusqu'à 8 heures d'activité intermédiaire mais à peine une vingtaine de minutes d'activité lourde dans sa journée, tout le reste se passant en activité légère. Au pic humain réel (Endurance 9), six heures de sommeil lui suffisent, et son Fond tient 12 heures d'intermédiaire et tout juste une heure de lourde.

</div>

#### Forcer l'effort

Les durées du Fond donnent ce qu'un personnage peut faire dans sa journée sans danger : tant qu'il reste sous sa durée d'activité intermédiaire et sous sa durée d'activité lourde, il ne risque rien. Le MJ juge au cas par cas ce qui compte dans chaque intensité : le but est de limiter les journées où l'on force trop, pas de chronométrer chaque geste.

Quand un personnage a épuisé l'une de ces durées et continue quand même dans cette intensité, il force sur un corps déjà à bout. Il fait alors un jet de [Résistance à l'Épuisement](competences.md), une première fois au moment où il dépasse la durée, puis régulièrement tant qu'il continue : toutes les heures en activité intermédiaire, toutes les dix minutes en activité lourde. S'il s'arrête puis reprend plus tard, la durée toujours épuisée, il refait un jet aussitôt, puis aux mêmes intervalles : les pauses ne remettent rien à zéro avant le prochain sommeil correct. La difficulté augmente à chaque jet :

<p class="formula">Difficulté = 100 + 20 × le nombre de jets déjà faits pour forcer l'effort depuis le dernier sommeil correct</p>

Le premier jet se fait donc à 100, le deuxième à 120, et ainsi de suite ; les jets de veille ([Veiller sans dormir](#veiller-sans-dormir)) ne comptent pas dans ce total. S'il réussit, le personnage tient jusqu'au prochain jet. S'il échoue, il perd des points de [fatigue](#la-fatigue) selon sa marge d'échec ; rien ne l'empêche de continuer, sinon la fatigue elle-même.

#### Veiller sans dormir

Un personnage peut rester éveillé sans risque pendant son temps avant d'être fatigué, qui dépend de son Repos :

<p class="formula">Temps avant d'être fatigué = 24 heures − le temps de sommeil requis</p>

Au-delà, chaque heure d'éveil en plus lui demande un jet de [Résistance à l'Épuisement](competences.md), de plus en plus difficile :

<p class="formula">Difficulté = 20 pour la première heure dépassée, +20 par heure suivante</p>

La première heure dépassée demande donc un jet à 20, la deuxième un jet à 40, et ainsi de suite. Ces jets suivent leur propre compte, séparé de celui de Forcer l'effort : un personnage qui force à la fois sur l'éveil et sur ses durées d'activité fait les deux séries de jets. Les heures dormies ne comptent pas comme heures d'éveil, et le compte d'heures dépassées ne repart de zéro qu'après un sommeil correct. S'il réussit, le personnage reste debout jusqu'à l'heure suivante. S'il échoue, il perd des points de [fatigue](#la-fatigue) selon sa marge d'échec. Il peut renoncer et dormir dès qu'il le peut ; sinon, la fatigue finit par le faire tomber : arrivé à son maximum en négatif, il s'effondre d'épuisement.

<div class="gloss-source span sommeil" markdown>

| Repos | Temps de sommeil | Avant de pouvoir redormir | Avant d'être fatigué |
|:---:|:---:|:---:|:---:|
| 0 | 18 h | 3 h | 6 h |
| 1 | 16 h | 4 h | 8 h |
| 2 | 14 h | 5 h | 10 h |
| 3 | 12 h | 6 h | 12 h |
| 4 | 10 h | 7 h | 14 h |
| 5 | 8 h | 8 h | 16 h |
| 6 | 7 h 30 | 8 h 15 | 16 h 30 |
| 7 | 7 h | 8 h 30 | 17 h |
| 8 | 6 h 30 | 8 h 45 | 17 h 30 |
| 9 | 6 h | 9 h | 18 h |
| 10 | 5 h 30 | 9 h 15 | 18 h 30 |
| 11 | 5 h | 9 h 30 | 19 h |
| 12 | 4 h 30 | 9 h 45 | 19 h 30 |
| 13 | 4 h | 10 h | 20 h |
| 14 | 3 h 30 | 10 h 15 | 20 h 30 |
| 15 | 3 h | 10 h 30 | 21 h |
| 16 | 2 h 30 | 10 h 45 | 21 h 30 |
| 17 | 2 h | 11 h | 22 h |
| 18 | 1 h 30 | 11 h 15 | 22 h 30 |
| 19 | 1 h | 11 h 30 | 23 h |
| 20 | aucun | 12 h | 24 h |
| 21 | aucun | 12 h | 24 h |
| 22 | aucun | 12 h | 24 h |
| 23 | aucun | 12 h | 24 h |
| 24 | aucun | 12 h | 24 h |
| 25 | aucun | 12 h | 24 h |
| 26 | aucun | 12 h | 24 h |
| 27 | aucun | 12 h | 24 h |
| 28 | aucun | 12 h | 24 h |
| 29 | aucun | 12 h | 24 h |
| 30 | aucun | 12 h | 24 h |

</div>

<div class="defs" markdown>

**Aucun :** le personnage n'a pas besoin de dormir. On considère qu'il se repose quand il est capable de dormir (son délai Avant de pouvoir redormir écoulé), qu'il est en activité légère depuis le début de son [tour](../combat/deroulement-combat.md) précédent et qu'il l'annonce (aucune action requise) : ce repos compte comme un sommeil correct.

</div>

<div class="gloss-source span sommeil" markdown>

| Fond | Activité intermédiaire | Activité lourde |
|:---:|:---:|:---:|
| 0 | 3 h | 1 min |
| 1 | 4 h | 2 min |
| 2 | 5 h | 3 min |
| 3 | 6 h | 5 min |
| 4 | 7 h | 10 min |
| 5 | 8 h | 20 min |
| 6 | 9 h | 30 min |
| 7 | 10 h | 40 min |
| 8 | 11 h | 50 min |
| 9 | 12 h | 1 h |
| 10 | 12 h | 1 h 30 |
| 11 | 12 h | 2 h |
| 12 | 12 h | 2 h 30 |
| 13 | 12 h | 3 h |
| 14 | 12 h | 3 h 30 |
| 15 | 12 h | 4 h |
| 16 | 12 h | 4 h 30 |
| 17 | 12 h | 5 h |
| 18 | 12 h | 5 h 30 |
| 19 | 12 h | 6 h |
| 20 | 12 h | 6 h 30 |
| 21 | 12 h | 7 h |
| 22 | 12 h | 7 h 30 |
| 23 | 12 h | 8 h |
| 24 | 12 h | 8 h 30 |
| 25 | 12 h | 9 h |
| 26 | 12 h | 9 h 30 |
| 27 | 12 h | 10 h |
| 28 | 12 h | 10 h 30 |
| 29 | 12 h | 11 h |
| 30 | 12 h | 12 h |

</div>

</div>

---

<div class="cols" markdown>

### Mouvement

Le Mouvement découle de l'Agilité : le Mouvement d'un personnage est égal à son Agilité. C'est la distance qu'il franchit en un [round](../combat/deroulement-combat.md), soit 6 secondes. Cette distance constitue son [mouvement passif](../combat/deroulement-combat.md) : il la parcourt durant son tour sans dépenser d'action, en une ou plusieurs fois, autour de ses actions. Tout mouvement qu'il n'utilise pas durant son tour reste disponible pour ses [réactions](../combat/deroulement-combat.md), jusqu'au début de son prochain tour.

Dans la table ci-dessous, la colonne se choisit par l'allure que le personnage adopte, et chaque allure impose son intensité d'[activité](#activite) :

<div class="defs" markdown>

**Légère, la marche :** la distance franchie d'un pas tranquille, toute la journée sans s'essouffler. Tant qu'un personnage ne dépasse pas cette distance dans le round, il reste en activité légère.

**Intermédiaire, la course :** la distance couverte en course soutenue, pendant des heures avec des pauses. Dès qu'un personnage dépasse sa marche dans un round, il court et passe au moins en activité intermédiaire.

**Lourde, le sprint :** la distance parcourue en sprint, un effort bref à pleine vitesse. Sprinter exige l'action [Foncer](#foncer) : sans elle, un personnage ne dépasse jamais sa course dans un round. Sprinter est une activité lourde.

</div>

<div class="gloss-source" data-gloss="mouvement" markdown>

| Mouvement | Légère | Intermédiaire | Lourde |
|:---:|:---:|:---:|:---:|
| 0 | 0 m | 0 m | 0 m |
| 1 | 2 m | 4 m | 10 m |
| 2 | 3 m | 6 m | 15 m |
| 3 | 4 m | 8 m | 20 m |
| 4 | 6 m | 12 m | 30 m |
| 5 | 8 m | 16 m | 40 m |
| 6 | 10 m | 20 m | 50 m |
| 7 | 12 m | 24 m | 60 m |
| 8 | 14 m | 28 m | 70 m |
| 9 | 16 m | 32 m | 80 m |
| 10 | 20 m | 40 m | 100 m |
| 11 | 30 m | 60 m | 150 m |
| 12 | 40 m | 80 m | 200 m |
| 13 | 60 m | 120 m | 300 m |
| 14 | 80 m | 160 m | 400 m |
| 15 | 100 m | 200 m | 500 m |
| 16 | 150 m | 300 m | 750 m |
| 17 | 200 m | 400 m | 1 km |
| 18 | 300 m | 600 m | 1.5 km |
| 19 | 400 m | 800 m | 2 km |
| 20 | 600 m | 1.2 km | 3 km |
| 21 | 800 m | 1.6 km | 4 km |
| 22 | 1 km | 2 km | 5 km |
| 23 | 1.5 km | 3 km | 7.5 km |
| 24 | 2 km | 4 km | 10 km |
| 25 | 3 km | 6 km | 15 km |
| 26 | 5 km | 10 km | 25 km |
| 27 | 10 km | 20 km | 50 km |
| 28 | 20 km | 40 km | 100 km |
| 29 | 50 km | 100 km | 250 km |
| 30 | 100 km | 200 km | 500 km |

</div>

<div class="memo" markdown>

Exemple. Avec un Mouvement de 5, un personnage couvre par round 8 m en marche (activité légère), 16 m en course (activité intermédiaire), puis 40 m en sprint (activité lourde), à condition de Foncer.

</div>

#### Foncer

Foncer est une [action](../combat/deroulement-combat.md) qui permet au personnage de se déplacer en allure lourde, le sprint, jusqu'au début de son prochain tour. C'est un effort en soi : tant que son effet dure, le personnage est au moins en activité intermédiaire.

En fonçant, le personnage peut faire un jet de la compétence de déplacement qui convient à son milieu pour aller plus vite : [Course](competences.md) pour un déplacement terrestre, [Natation](competences.md) pour un déplacement aquatique, [Vol](competences.md) pour un déplacement aérien. Le jet donne un bonus au Mouvement, lu dans la table ci-dessous à la ligne du plus haut seuil atteint. Jusqu'au début de son prochain tour, le personnage lit toutes ses distances à la ligne de son Mouvement augmenté de ce bonus, quelle que soit la colonne. Avec un Mouvement de 5 et un jet à 180 (+2), il lit la ligne 7 : 12 m en marche, 24 m en course, 60 m en sprint. La distance du round en cours est relue à la nouvelle valeur, et ce qu'il a déjà parcouru ce round s'en décompte.

<div class="sepia-table" markdown>

| Jet de déplacement | Bonus au Mouvement |
|:---:|:---:|
| Difficile (120) | +1 |
| Très difficile (180) | +2 |
| Absurde (240) | +3 |
| Quasi impossible (320) | +4 |
| Impossible (400) | +5 |
| Surhumaine (520) | +6 |
| Prodigieuse (640) | +7 |
| Insurmontable (780) | +8 |
| Inimaginable (920) | +9 |

</div>

Rien n'empêche de Foncer tour après tour : c'est la durée d'activité lourde de la journée qui limite le sprint. Un personnage qui fonce à chacun de ses tours peut conserver le dernier jet de déplacement qu'il a fait, ou relancer.

#### Changer d'allure ou de terrain en chemin

Rien n'oblige à garder la même allure durant tout un round : le personnage passe de l'une à l'autre à sa guise. Quand il change d'allure, on retire tout le mouvement déjà parcouru ce round de la distance de la nouvelle allure : ce qui reste est ce qu'il peut encore parcourir.

<p class="formula">Distance restante = nouvelle distance lue − mètres déjà parcourus ce round</p>

S'il ne reste rien, le mouvement du round est épuisé. L'intensité d'[activité](#activite) du round est celle de l'allure la plus exigeante employée.

La même soustraction s'applique chaque fois que la distance lue change en plein déplacement, quand le personnage entre sur un [terrain difficile](#terrain-difficile) ou en sort, ou quand l'effet de [Foncer](#foncer) commence ou s'arrête : on retire les mètres déjà parcourus ce round de la nouvelle distance. S'il a déjà parcouru autant ou plus, son mouvement du round est épuisé.

<div class="memo" markdown>

Exemple. Avec un Mouvement de 5, un personnage court 16 m ou sprinte 40 m par round. S'il court 8 m puis se met à sprinter, en Fonçant, il retire ces 8 m des 40 m du sprint : il peut encore parcourir 32 m. À l'inverse, s'il entre dans la boue d'un terrain Difficile (−2) après 6 m de route, sa course s'y lit au Mouvement 3, soit 8 m, dont il retire les 6 m déjà parcourus : il n'avance plus que de 2 m ce round.

</div>

<div class="keep" markdown>

#### Terrain difficile

Un sol qui gêne la progression, boue, éboulis, sous-bois, neige, décombres ou foule, ralentit le mouvement sans rien coûter d'autre. Le MJ classe le terrain parmi les six types ci-dessous, en le comparant aux exemples, et le personnage applique le malus de la table à la ligne où il lit sa distance, à la colonne de l'allure qu'il adopte : l'inverse de Foncer, qui la fait lire plus haut. Les bonus et les malus au Mouvement s'additionnent : +2 en fonçant et −3 de terrain Éprouvant font −1.

</div>

On ne cumule pas plusieurs obstacles : un seul type s'applique, celui qui décrit le mieux l'ensemble du terrain.

<div class="sepia-table" markdown>

| Terrain | Mouvement |
|:---|:---:|
| Dégagé | 0 |
| Encombré | −1 |
| Difficile | −2 |
| Éprouvant | −3 |
| Ardu | −4 |
| Impraticable | −5 |

</div>

<div class="defs" markdown>

**Dégagé :** sol ferme et libre, route, plaine, plancher. Le mouvement se lit normalement.

**Encombré :** gravats épars, herbes hautes, eau aux chevilles, foule clairsemée. À peine ralenti, il garde presque toute son allure.

**Difficile :** boue, éboulis, broussailles, neige à mi-mollet. La progression tombe de moitié.

**Éprouvant :** marécage, pente d'éboulis instable, neige à mi-cuisse, ronciers. Chaque mètre demande un effort.

**Ardu :** boue profonde, congères, amas de rochers. On n'y gagne que quelques pas par round.

**Impraticable :** marécage jusqu'au torse, ronciers inextricables, éboulement. On n'y avance presque plus : pour un corps ordinaire, Mouvement 5 ou moins, c'est l'arrêt.

</div>

<div class="memo" markdown>

Exemple. Avec un Mouvement de 5, un personnage court 16 m par round en activité intermédiaire. Sur un terrain Difficile, il lit sa distance au Mouvement 3 : 8 m. Sur un terrain Éprouvant, il tombe au Mouvement 2, soit 6 m. Sur un terrain Impraticable, il descend au Mouvement 0 : il ne bouge plus.

</div>

#### Déplacement dans l'eau

Dans l'eau, le Mouvement se lit sur la même table, avec la compétence [Natation](competences.md) pour [Foncer](#foncer). Sans paire de nageoires ni de tentacules, c'est le cas du corps humain, un personnage nage avec −3 au Mouvement, comme le veulent les [formes du vivant](../monde/formes.md).

#### Chute

Un personnage qui tombe subit les dégâts de l'impact, donnés par la hauteur de la chute dans la table ci-dessous. On lit la plus grande hauteur qui ne dépasse pas celle de la chute : une chute de 10 mètres se lit à la ligne 8 m et inflige 30 dégâts. En dessous de 3 mètres, la chute n'inflige rien.

Les dégâts de chute sont des dégâts [contondants](../monde/degats.md), et ils ignorent 100 points de réduction de dégâts de la cible, quel qu'en soit le type d'armure.

Un personnage commence à chuter instantanément, dès qu'il peut tomber. Il effectue ensuite son mouvement de chute à la fin de son tour, et ce mouvement ne s'effectue qu'une seule fois par round. Il descend de 150 mètres au premier round où il commence à chuter, puis de 300 mètres par round, sa vitesse plafonnant à 50 m/s, soit 180 km/h, atteinte après 450 mètres de chute.

Les dégâts suivent l'énergie de l'impact, donc le carré de la vitesse : ils augmentent avec la hauteur, d'abord vite, puis de moins en moins à mesure que l'air freine. À la vitesse maximale, atteinte à 450 mètres, la chute cesse d'accélérer : au-delà, on ne tombe pas plus vite, donc pas plus fort, et les dégâts plafonnent à 500.

<div class="sepia-table" markdown>

| Hauteur de chute | Dégâts |
|:---:|:---:|
| 3 m | 10 |
| 5 m | 20 |
| 8 m | 30 |
| 12 m | 50 |
| 16 m | 60 |
| 20 m | 70 |
| 25 m | 90 |
| 30 m | 100 |
| 40 m | 140 |
| 50 m | 160 |
| 60 m | 190 |
| 80 m | 240 |
| 100 m | 280 |
| 130 m | 320 |
| 160 m | 360 |
| 200 m | 400 |
| 250 m | 430 |
| 300 m | 450 |
| 400 m | 480 |
| 450 m et plus | 500 |

</div>

Toucher le sol déclenche une [réaction](../combat/deroulement-combat.md) : le personnage fait un jet de la compétence [Chute](competences.md), et chaque point du jet à partir de 100 retire un point aux dégâts de la chute.

<p class="formula">Réduction des dégâts = résultat du jet de Chute − 100</p>

Un jet de 130 retire ainsi 30 points aux dégâts ; un jet sous 100 ne retire rien. En amortissant ou en roulant au sol, le personnage change une chute brutale en réception maîtrisée. Un personnage hors d'état de réagir, [Inconscient](etats.md) par exemple, ne fait pas ce jet et subit les dégâts entiers.

<div class="memo" markdown>

Exemple. Une chute de trois cents mètres inflige 450 dégâts. Le personnage obtient 400 à son jet de Chute et en retire 300 : il n'en subit plus que 150. Le même jet annulerait entièrement une chute de cent mètres, qui n'inflige que 280 dégâts.

</div>

#### Chuter dans l'eau

Tomber dans l'eau plutôt que sur une surface dure amortit la chute, à condition que l'eau soit assez profonde : 5 m suffisent toujours, quelle que soit la hauteur de chute, car l'eau freine d'autant plus fort qu'on la frappe vite. Les dégâts sont alors divisés par deux, après le jet de Chute : on applique d'abord la réduction du jet, puis on divise ce qui reste par deux. Une eau trop peu profonde compte comme un sol dur.

</div>

---

<div class="cols" markdown>

### Saut

Le Saut découle de la Force : le Saut d'un personnage est égal à sa Force. C'est la distance qu'il atteint en sautant, donnée par la table ci-dessous. La colonne Avec élan vaut pour un saut pris en pleine course ; la colonne Sans élan, pour un saut à l'arrêt, qui s'élève moitié moins haut. L'élan demande de [Foncer](#foncer) et de courir au moins 10 mètres en ligne droite juste avant de sauter, quelle que soit la hauteur du saut. À 5, la moyenne humaine s'élève de 0.5 m sans élan et de 1 m avec ; à 9, le sommet humain réel, 3.5 m et 7 m.

Sauter est une [action](../combat/deroulement-combat.md) et un effort à pleine puissance : le round où il saute, le personnage est en [activité](#activite) lourde. La course d'élan compte dans le [mouvement](#mouvement) du round ; le saut, lui, n'y compte pas. Un saut qui aboutit sur un sol se termine par un simple atterrissage, sans dégâts.

Un personnage dont le saut le laisse en l'air y reste, là où son saut l'a porté. Il peut se laisser tomber quand il le souhaite pendant son tour (aucune action requise) ; s'il ne l'a pas fait avant la fin de son tour, il tombe alors, selon les règles de la [Chute](#chute).

<div class="gloss-source" data-gloss="saut" markdown>

| Saut | Sans élan | Avec élan |
|:---:|:---:|:---:|
| 0 | 0 m | 0 m |
| 1 | 0 m | 0.1 m |
| 2 | 0.1 m | 0.2 m |
| 3 | 0.2 m | 0.3 m |
| 4 | 0.3 m | 0.5 m |
| 5 | 0.5 m | 1 m |
| 6 | 1 m | 2 m |
| 7 | 1.5 m | 3 m |
| 8 | 2.5 m | 5 m |
| 9 | 3.5 m | 7 m |
| 10 | 5 m | 10 m |
| 11 | 10 m | 20 m |
| 12 | 15 m | 30 m |
| 13 | 25 m | 50 m |
| 14 | 35 m | 70 m |
| 15 | 50 m | 100 m |
| 16 | 100 m | 200 m |
| 17 | 150 m | 300 m |
| 18 | 250 m | 500 m |
| 19 | 350 m | 700 m |
| 20 | 500 m | 1 km |
| 21 | 1 km | 2 km |
| 22 | 1.5 km | 3 km |
| 23 | 2.5 km | 5 km |
| 24 | 3.5 km | 7 km |
| 25 | 5 km | 10 km |
| 26 | 10 km | 20 km |
| 27 | 15 km | 30 km |
| 28 | 25 km | 50 km |
| 29 | 35 km | 70 km |
| 30 | 50 km | 100 km |

</div>

Au moment de sauter, le personnage peut faire un jet de [Saut](competences.md) (aucune action requise) pour aller plus loin. Le jet donne un bonus au Saut, lu dans la table ci-dessous à la ligne du plus haut seuil atteint : le personnage lit alors la table à la ligne de son Saut augmenté de ce bonus. Un jet sous Difficile (120) ne donne aucun bonus.

<div class="sepia-table" markdown>

| Jet de Saut | Bonus au Saut |
|:---:|:---:|
| Difficile (120) | +1 |
| Très difficile (180) | +2 |
| Absurde (240) | +3 |
| Quasi impossible (320) | +4 |
| Impossible (400) | +5 |
| Surhumaine (520) | +6 |
| Prodigieuse (640) | +7 |
| Insurmontable (780) | +8 |
| Inimaginable (920) | +9 |

</div>

<div class="memo" markdown>

Exemple. Avec un Saut de 5, un personnage s'élève de 1 m en sautant avec élan. Sur un jet de Saut à 180 (+2), il lit la ligne 7 : 3 m. Au sommet humain réel (Saut 9), le même saut sans jet atteint 7 m.

</div>

<div class="keep" markdown>

#### Saut en longueur

Le personnage peut augmenter son saut uniquement dans la longueur, en consommant son [mouvement](#mouvement) : chaque mètre de mouvement dépensé ajoute un mètre au saut. Il peut au mieux multiplier la distance du saut par quatre.

</div>

<div class="memo" markdown>

Exemple. Avec un Saut de 5 et son élan, un personnage saute 1 m. En dépensant 3 m de mouvement, il franchit 4 m en longueur, son maximum (quatre fois 1 m).

</div>

</div>

---

<div class="cols" markdown>

### Port

Le Port découle de la Force : le Port d'un personnage est égal à sa Force. Son indice de poids fixe la charge qu'un personnage porte, soulève ou brise. La colonne se détermine par la charge maniée, et la charge impose son intensité d'[activité](#activite) :

<div class="defs" markdown>

**Légère :** le poids porté ou déplacé sans aucune fatigue, indéfiniment. Tant qu'une charge n'excède pas cette valeur, elle ne coûte aucun effort et laisse le personnage en activité légère.

**Intermédiaire :** le poids manié au prix d'un vrai effort, des heures durant mais avec des pauses. Dès qu'une charge dépasse la colonne Légère, le personnage passe au moins en activité intermédiaire.

**Lourde :** le poids maximal soulevé ou brisé à pleine puissance, le temps d'un seul effort. Mouvoir une charge qui dépasse la colonne Intermédiaire exige l'action [Forcer](#forcer) : sans elle, elle reste hors de portée. Le personnage passe alors en activité lourde.

</div>

<div class="gloss-source" data-gloss="port" markdown>

| Port | Légère | Intermédiaire | Lourde |
|:---:|:---:|:---:|:---:|
| 0 | 0 kg | 0 kg | 0 kg |
| 1 | 1 kg | 2 kg | 5 kg |
| 2 | 2 kg | 5 kg | 10 kg |
| 3 | 3 kg | 8 kg | 20 kg |
| 4 | 5 kg | 15 kg | 50 kg |
| 5 | 10 kg | 30 kg | 100 kg |
| 6 | 20 kg | 60 kg | 200 kg |
| 7 | 30 kg | 100 kg | 300 kg |
| 8 | 50 kg | 150 kg | 500 kg |
| 9 | 100 kg | 300 kg | 1 t |
| 10 | 1 t | 3 t | 10 t |
| 11 | 2 t | 6 t | 20 t |
| 12 | 3 t | 10 t | 30 t |
| 13 | 5 t | 15 t | 50 t |
| 14 | 10 t | 30 t | 100 t |
| 15 | 100 t | 300 t | 1 000 t |
| 16 | 200 t | 600 t | 2 000 t |
| 17 | 300 t | 1 000 t | 3 000 t |
| 18 | 500 t | 1 500 t | 5 000 t |
| 19 | 1 000 t | 3 000 t | 10 000 t |
| 20 | 10 000 t | 30 000 t | 100 000 t |
| 21 | 20 000 t | 60 000 t | 200 000 t |
| 22 | 30 000 t | 100 000 t | 300 000 t |
| 23 | 50 000 t | 150 000 t | 500 000 t |
| 24 | 100 000 t | 300 000 t | 1 000 000 t |
| 25 | 1 000 000 t | 3 000 000 t | 10 000 000 t |
| 26 | 2 000 000 t | 6 000 000 t | 20 000 000 t |
| 27 | 3 000 000 t | 10 000 000 t | 30 000 000 t |
| 28 | 5 000 000 t | 15 000 000 t | 50 000 000 t |
| 29 | 10 000 000 t | 30 000 000 t | 100 000 000 t |
| 30 | 100 000 000 t | 300 000 000 t | 1 000 000 000 t |

</div>

<div class="memo" markdown>

Exemple. Avec un Port de 5, la moyenne humaine, un personnage porte sans fatigue 10 kg en activité légère, manie 30 kg en activité intermédiaire, puis soulève jusqu'à 100 kg le temps d'un effort en activité lourde.

</div>

#### Forcer

Forcer est une [action](../combat/deroulement-combat.md). Le personnage fait un jet de [Prouesse de Force](competences.md) : le jet donne un bonus au Port, lu dans la table ci-dessous à la ligne du plus haut seuil atteint. Jusqu'à la fin du prochain round, il en tire deux effets : il peut mouvoir les charges de sa colonne Lourde ; et pour soulever, briser ou résister à un écrasement, il lit la table à la ligne de son Port augmenté de ce bonus. Un jet sous Difficile (120) ne donne aucun bonus, mais permet tout de même de mouvoir les charges de la colonne Lourde.

<div class="sepia-table" markdown>

| Jet de Prouesse de Force | Bonus au Port |
|:---:|:---:|
| Difficile (120) | +1 |
| Très difficile (180) | +2 |
| Absurde (240) | +3 |
| Quasi impossible (320) | +4 |
| Impossible (400) | +5 |
| Surhumaine (520) | +6 |
| Prodigieuse (640) | +7 |
| Insurmontable (780) | +8 |
| Inimaginable (920) | +9 |

</div>

<div class="keep" markdown>

#### Tirer et pousser

Tirer ou pousser une charge suit le même indice de poids, mais toutes ses valeurs sont multipliées par dix : on tire ou pousse dix fois ce qu'on porterait. Les intensités imposées et l'action Forcer pour la colonne Lourde s'appliquent comme au soulevé. Ainsi un Port de 9, sommet humain réel, soulève une tonne à pleine puissance mais en tire ou pousse dix.

</div>

#### Écrasement

Une masse trop lourde qui s'abat sur un personnage, ou sous laquelle il est coincé, l'écrase. On compare la masse à sa colonne Lourde : tant qu'elle n'excède pas ce qu'il lève à pleine puissance, il la supporte sans dégâts, quitte à rester bloqué. Au-delà, on cherche le Port requis, le plus petit Port dont la colonne Lourde atteint la masse, et chaque point d'écart inflige 40 dégâts :

<p class="formula">Dégâts par round = 40 × (Port requis − Port du personnage)</p>

Ces dégâts tombent une première fois dès l'écrasement, puis à la fin de chacun de ses tours tant qu'il reste pris. À chaque fois, il peut faire un jet de [Prouesse de Force](competences.md) (aucune action requise) : le bonus au Port que donne son jet, lu dans la table de [Forcer](#forcer), efface autant de points d'écart, et les dégâts du round retombent de 40 par point effacé.

<div class="memo" markdown>

Exemple. Avec un Port de 5, un personnage lève 100 kg à pleine puissance (ligne 5 de la colonne Lourde). Pris sous un bloc d'une tonne, que seul un Port de 9 soulèverait, il est dépassé de quatre points, soit 160 dégâts. S'il atteint Très difficile (180) à son jet de Prouesse de Force, il en efface deux et n'en subit plus que 80 ce round-là.

</div>

### Lancer

Le Lancer découle de la Force : le Lancer d'un personnage est égal à sa Force. La table ci-dessous en tire un multiplicateur, qui multiplie les portées des [armes](../combat/armes.md) que les muscles du porteur propulsent, aussi bien les armes de jet que les arcs. Chez la moyenne humaine (Lancer 5), les portées des armes se lisent telles quelles (×1) ; au sommet humain réel (Lancer 9), elles triplent (×3) : c'est l'écart réel entre un lancer ordinaire et un record du monde.

Le multiplicateur ne s'applique qu'aux armes que le corps propulse. Une arme à [Propulsion mécanique](../combat/armes.md) garde ses portées inchangées, quel que soit le tireur.

<div class="gloss-source" data-gloss="lancer" markdown>

| Lancer | Portées de lancer et de tir |
|:---:|:---:|
| 0 | ×0 |
| 1 | ×0.2 |
| 2 | ×0.4 |
| 3 | ×0.6 |
| 4 | ×0.8 |
| 5 | ×1 |
| 6 | ×1.5 |
| 7 | ×2 |
| 8 | ×2.5 |
| 9 | ×3 |
| 10 | ×5 |
| 11 | ×7 |
| 12 | ×10 |
| 13 | ×20 |
| 14 | ×30 |
| 15 | ×50 |
| 16 | ×70 |
| 17 | ×100 |
| 18 | ×200 |
| 19 | ×300 |
| 20 | ×500 |
| 21 | ×700 |
| 22 | ×1 000 |
| 23 | ×2 000 |
| 24 | ×3 000 |
| 25 | ×5 000 |
| 26 | ×7 000 |
| 27 | ×10 000 |
| 28 | ×20 000 |
| 29 | ×30 000 |
| 30 | ×50 000 |

</div>

<div class="memo" markdown>

Exemple. Une dague se lance à 5/10 m. Avec un Lancer de 9 (×3), elle porte 15/30 m ; avec un Lancer de 12 (×10), 50/100 m. Un Lancer de 0 (×0) ne lance rien, et un fusil tire à la même distance quel que soit le tireur.

</div>

</div>

---

<div class="cols" markdown>

### Retenir son souffle

L'Apnée découle de l'Endurance : l'Apnée d'un personnage est égale à son Endurance. C'est la durée pendant laquelle il retient sa respiration. À l'inverse du Mouvement et du Port, la colonne ne se choisit pas, elle se subit : l'apnée se lit à la colonne de l'intensité d'[activité](#activite) du moment, et un effort plus intense la raccourcit, car plus le corps s'active, plus il brûle d'oxygène.

Retenir son souffle coûte une [action](../combat/deroulement-combat.md), le temps de bloquer sa respiration. Le personnage tient ensuite la durée que lui donne son Apnée, lue à la colonne de l'intensité d'activité qu'il fournit pendant ce temps.

<div class="gloss-source" data-gloss="apnee" markdown>

| Apnée | Légère | Intermédiaire | Lourde |
|:---:|:---:|:---:|:---:|
| 0 | moins de 6 s | 0 s | 0 s |
| 1 | 6 s | moins de 6 s | 0 s |
| 2 | 12 s | 6 s | moins de 6 s |
| 3 | 18 s | 12 s | 6 s |
| 4 | 30 s | 18 s | 12 s |
| 5 | 1 min | 30 s | 18 s |
| 6 | 2 min | 1 min | 30 s |
| 7 | 3 min | 2 min | 1 min |
| 8 | 5 min | 3 min | 2 min |
| 9 | 10 min | 5 min | 3 min |
| 10 | 20 min | 10 min | 5 min |
| 11 | 30 min | 20 min | 10 min |
| 12 | 1 h | 30 min | 20 min |
| 13 | 2 h | 1 h | 30 min |
| 14 | 3 h | 2 h | 1 h |
| 15 | 5 h | 3 h | 2 h |
| 16 | 10 h | 5 h | 3 h |
| 17 | 1 jour | 10 h | 5 h |
| 18 | 2 jours | 1 jour | 10 h |
| 19 | 3 jours | 2 jours | 1 jour |
| 20 | 5 jours | 3 jours | 2 jours |
| 21 | 10 jours | 5 jours | 3 jours |
| 22 | 20 jours | 10 jours | 5 jours |
| 23 | 1 mois | 20 jours | 10 jours |
| 24 | 2 mois | 1 mois | 20 jours |
| 25 | 3 mois | 2 mois | 1 mois |
| 26 | 5 mois | 3 mois | 2 mois |
| 27 | 10 mois | 5 mois | 3 mois |
| 28 | illimitée | 10 mois | 5 mois |
| 29 | illimitée | illimitée | 10 mois |
| 30 | illimitée | illimitée | illimitée |

</div>

<div class="defs" markdown>

**Légère :** au repos ou en activité légère, le souffle se garde le plus longtemps.

**Intermédiaire :** sous une activité intermédiaire, qu'il porte une charge, coure ou peine, la même apnée fond déjà de beaucoup.

**Lourde :** en activité lourde, lorsqu'il force, sprinte ou se bat, le souffle file au plus vite.

</div>

<div class="memo" markdown>

Exemple. Avec une Apnée de 5, un personnage retient son souffle 1 minute au repos en activité légère, 30 secondes sous un effort modéré en activité intermédiaire, puis 18 secondes en plein combat en activité lourde.

</div>

En bloquant sa respiration, le personnage peut faire un jet d'[Apnée](competences.md) (aucune action requise). Le jet donne un bonus à l'Apnée, lu dans la table ci-dessous à la ligne du plus haut seuil atteint : pour toute la durée de ce souffle, le personnage lit la table à la ligne de son Apnée augmentée de ce bonus. Un jet sous Difficile (120) ne donne aucun bonus.

<div class="sepia-table" markdown>

| Jet d'Apnée | Bonus à l'Apnée |
|:---:|:---:|
| Difficile (120) | +1 |
| Très difficile (180) | +2 |
| Absurde (240) | +3 |
| Quasi impossible (320) | +4 |
| Impossible (400) | +5 |
| Surhumaine (520) | +6 |
| Prodigieuse (640) | +7 |
| Insurmontable (780) | +8 |
| Inimaginable (920) | +9 |

</div>

#### Alterner entre deux activités en apnée

Rien n'oblige à garder la même intensité durant toute une apnée : le personnage passe de l'une à l'autre à sa guise. Le souffle reste une réserve unique, que chaque intensité épuise plus ou moins vite. On la suit en fractions :

<p class="formula">Part consommée = temps passé dans l'intensité ÷ durée maximale de la colonne</p>

Chaque part consommée se reporte à l'identique sur les autres colonnes, et le souffle est épuisé quand la somme des parts atteint le tout.

<div class="memo" markdown>

Exemple. Avec une Apnée de 10, un personnage tient 20 minutes en activité légère, 10 en intermédiaire et 5 en lourde. Une minute en activité lourde lui en coûte le cinquième, soit 4 minutes d'activité légère (un cinquième de 20). En se calmant, il ne lui reste plus que 16 minutes d'apnée légère.

</div>

#### Suffocation

Privé d'air, étranglé, noyé ou enfermé sans oxygène, un personnage suffoque. La suffocation est subie de force, en pleine détresse, là où l'apnée mesure le souffle retenu de plein gré : un personnage dont l'apnée s'épuise sans qu'il retrouve d'air se met aussitôt à suffoquer. Retrouver de l'air met fin à la suffocation.

La Suffocation découle de l'Endurance : la Suffocation d'un personnage est égale à son Endurance. Le personnage résiste un nombre de rounds égal à sa Suffocation : le décompte part de sa Suffocation et baisse de 1 par round. À 0, il sombre dans l'[Inconscience](etats.md) ; inconscient, le décompte poursuit sa chute au même rythme, et le personnage meurt lorsqu'il atteint l'opposé de sa Suffocation.

<div class="memo" markdown>

Exemple. Avec une Suffocation de 10, un personnage lutte 10 rounds avant de sombrer dans l'Inconscience, puis tient 10 rounds encore, jusqu'à −10, avant de mourir. Un round durant 6 secondes, c'est une minute de résistance, puis une minute de sursis.

</div>

### Pression aquatique {#pression-aquatique}

La Pression découle de l'Endurance : la Pression d'un personnage est égale à son Endurance. C'est la profondeur qu'il supporte, donnée par la table ci-dessous. La colonne se détermine par la profondeur où il se trouve, et la profondeur impose son intensité d'[activité](#activite) :

<div class="defs" markdown>

**Légère :** la profondeur supportée indéfiniment. Tant que le personnage ne descend pas plus bas, la pression le laisse en activité légère.

**Intermédiaire :** la profondeur supportée au prix d'un vrai effort, de longues heures durant. Plus bas que sa profondeur Légère, le personnage passe au moins en activité intermédiaire.

**Lourde :** la profondeur maximale que le corps supporte, à pleine puissance. Plus bas que sa profondeur Intermédiaire, le personnage passe en activité lourde.

</div>

<div class="gloss-source" data-gloss="pression" markdown>

| Pression | Légère | Intermédiaire | Lourde |
|:---:|:---:|:---:|:---:|
| 0 | 0 m | 0 m | 0 m |
| 1 | 0.2 m | 0.4 m | 1 m |
| 2 | 0.4 m | 1 m | 2 m |
| 3 | 0.6 m | 1.6 m | 4 m |
| 4 | 1 m | 3 m | 10 m |
| 5 | 2 m | 6 m | 20 m |
| 6 | 4 m | 12 m | 40 m |
| 7 | 6 m | 20 m | 60 m |
| 8 | 10 m | 30 m | 100 m |
| 9 | 20 m | 60 m | 200 m |
| 10 | 200 m | 600 m | 2 km |
| 11 | 400 m | 1.2 km | 4 km |
| 12 | 600 m | 2 km | 6 km |
| 13 | 1 km | 3 km | 10 km |
| 14 | 2 km | 6 km | 20 km |
| 15 | 20 km | 60 km | 200 km |
| 16 | 40 km | 120 km | 400 km |
| 17 | 60 km | 200 km | 600 km |
| 18 | 100 km | 300 km | 1 000 km |
| 19 | 200 km | 600 km | 2 000 km |
| 20 | 2 000 km | 6 000 km | 20 000 km |
| 21 | 4 000 km | 12 000 km | 40 000 km |
| 22 | 6 000 km | 20 000 km | 60 000 km |
| 23 | 10 000 km | 30 000 km | 100 000 km |
| 24 | 20 000 km | 60 000 km | 200 000 km |
| 25 | 200 000 km | 600 000 km | 2 000 000 km |
| 26 | 400 000 km | 1 200 000 km | 4 000 000 km |
| 27 | 600 000 km | 2 000 000 km | 6 000 000 km |
| 28 | 1 000 000 km | 3 000 000 km | 10 000 000 km |
| 29 | 2 000 000 km | 6 000 000 km | 20 000 000 km |
| 30 | 20 000 000 km | 60 000 000 km | 200 000 000 km |

</div>

La profondeur Lourde est la limite du corps : plus bas, le poids de l'eau écrase le personnage. On cherche alors sa Pression requise : la plus petite Pression dont la profondeur Lourde atteint celle où il se trouve. Chaque point d'écart lui inflige 40 dégâts, comme un [Écrasement](#ecrasement) : une première fois quand il passe sous sa limite, puis à la fin de chacun de ses tours suivants tant qu'il reste à cette profondeur. La Pression requise suit la profondeur du personnage : remonter réduit les dégâts, et remonter au-dessus de sa profondeur Lourde y met fin.

<p class="formula">Dégâts par round = 40 × (Pression requise − Pression du personnage)</p>

<div class="memo" markdown>

Exemple. Avec une Pression de 5, un personnage nage sans effort jusqu'à 2 m de fond, passe en activité intermédiaire jusqu'à 6 m, puis en activité lourde jusqu'à 20 m, sa limite. À 45 m, il faudrait une Pression de 7 (60 m) : avec deux points d'écart, il subit 80 dégâts en descendant, puis autant à la fin de chacun de ses tours tant qu'il reste à cette profondeur. Avec une Pression de 13, la fosse la plus profonde de l'océan (10 km) est à sa portée, à pleine puissance.

</div>

</div>
