# Capacités de Nen

<div class="cols" markdown>

Une capacité de Nen s'assemble à partir d'un socle, sur lequel on empile des modules. Le socle fixe ce que la capacité cherche à faire ; chaque module lui ajoute une propriété chiffrée. Un pouvoir de Nen est un ensemble de capacités reliées entre elles.

Ce chapitre pose le langage commun aux six catégories : de quoi une capacité se compose, ce que coûtent ses modules, comment ils se raccordent. Les modules propres à chaque école figurent dans les chapitres qui suivent ; ceux qui n'appartiennent à aucune école restent ici.

Employer une capacité de Nen demande une arme [Compatible Nen](../combat/armes.md), par laquelle l'aura circule. Les armes de corps portent toutes cette propriété ; un objet fabriqué ne la gagne que par le [Shu](techniques-nen.md).

### Vocabulaire

<div class="defs" markdown>

**Pouvoir :** le Hatsu d'un personnage, désigné par un nom propre ; un pouvoir se compose d'une ou plusieurs capacités.

**Capacité :** un effet de Nen complet et autonome ; un même pouvoir peut en réunir plusieurs.

**Module :** la plus petite pièce ; on empile des modules sur une capacité pour lui ajouter des propriétés.

**Lanceur :** celui dont la réserve paie l'UAA d'une capacité à son déclenchement ; l'aura qu'elle dérobe ou gagne lui revient.

**Mainteneur :** celui dont la réserve paie la MA d'une capacité à chaque round où elle se maintient.

</div>

Un pouvoir est donc un ensemble de capacités raccordées entre elles ; une capacité est un socle, plus une pile de modules, dotée d'une cible, d'une durée, d'un modificateur d'affinité d'emploi et, parfois, de conditions.

Le plus souvent, le porteur d'une capacité en est à la fois le lanceur et le mainteneur. Ces rôles ne se détachent du porteur que par une entité qu'il a dressée : une entité qui s'entretient seule devient le mainteneur de son propre socle, dont le porteur reste le lanceur ; une capacité embarquée dans une entité qui manie le Nen peut, selon le réglage choisi, lui passer le rôle de mainteneur, de lanceur, ou les deux. [Maintenir à Distance](emission.md) n'y change rien : le porteur reste lanceur et mainteneur.

### Les deux axes : type et catégorie

Toute capacité se lit sur deux axes indépendants. Le premier dit ce qu'elle fait ; le second, de quelle nature de Nen procède chacun de ses modules.

#### Le type : le rôle de la capacité

Le type dit ce que la capacité fait, mécaniquement. Il y en a trois, et toute capacité en porte exactement un.

| Type | Ce qu'il fait |
|---|---|
| Attaque | elle frappe, elle blesse |
| Défense | elle protège, elle pare, elle entrave |
| Effet | tout le reste : amplification, déplacement, perception, altération, utilité |

Le type oriente le choix des modules sans le restreindre : un module de n'importe quelle famille peut se greffer sur la capacité, pourvu que sa fiche accepte ce type.

#### La catégorie : l'école du module

Les six catégories de Nen (renforcement, émission, transmutation, manipulation, conjuration, spécialisation) ne sont pas des types : ce sont les écoles auxquelles appartiennent les modules. Chaque module relève d'une seule catégorie, qui dit de quelle nature de Nen il procède. Un module purement structurel n'en a aucune.

<div class="defs" markdown>

**Renforcement :** amplifier une aptitude qui existe déjà.

**Émission :** projeter l'aura loin du corps.

**Transmutation :** prêter à l'aura une propriété de matière.

**Manipulation :** soumettre un être ou un objet.

**Conjuration :** donner à l'aura une existence matérielle.

**Spécialisation :** ce qui n'entre nulle part ailleurs.

</div>

Les deux axes sont indépendants : une capacité de type attaque peut empiler un module de dégâts (renforcement), un module tranchant (transmutation) et un module de portée (émission), pour un coup tranchant porté à distance.

La catégorie de chaque module détermine l'[affinité](archetypes-nen.md) qui s'y applique : elle fixe le coût de conception et la puissance du module, selon que le porteur emploie ou non son école. Un renforceur convertit ainsi son [développement intérieur](di.md) en modules de renforcement à plein rendement, et en modules de conjuration à perte.

### Anatomie d'une capacité

On assemble une capacité en posant, dans l'ordre : son type, le socle ; sa cible ; ses modules, chacun avec ses attributs ; sa durée ; son modificateur d'affinité d'emploi global ; ses conditions, s'il y en a.

#### Le socle : le type

Le socle fixe la forme de la capacité avant tout module. Trois socles de base servent à toutes les catégories ; ils ne coûtent rien en soi et tiennent tous leurs effets de leurs modules. Les autres socles, propres à une école, sont décrits dans son chapitre.

<div class="cj-modules anima" markdown>

<div class="keep" markdown>

#### Attaque

<p class="mod-type">Socle : attaque</p>

La capacité sert à frapper : elle porte les dégâts et les effets d'une attaque, et se résout par un jet opposé à la défense de la cible. Elle s'emploie au contact par défaut ; un module de portée l'étend à distance. Sans module, elle ne coûte rien : ses modules lui donnent sa portée, ses dégâts et ses effets.

</div>

<div class="keep" markdown>

#### Défense

<p class="mod-type">Socle : défense</p>

La capacité protège, pare ou entrave : elle alimente une parade, une esquive, une réduction de dégâts ou une barrière. Sans module, elle ne coûte rien : ses modules lui donnent ses effets.

</div>

<div class="keep" markdown>

#### Effet

<p class="mod-type">Socle : effet</p>

La capacité fait autre chose que frapper ou parer : elle amplifie, déplace, perçoit, altère ou communique. Son effet porte sur le porteur lui-même. Sans module, elle ne coûte rien : ses modules portent tout ce qu'elle fait.

</div>

</div>

#### La cible

Toute capacité vise une cible : l'être ou l'objet sur lequel son effet porte. Par défaut, une capacité d'attaque, de défense ou d'effet a pour cible Soi-même, c'est-à-dire le porteur, sur qui son effet se pose.

Un module de raccord peut déplacer cette cible : le module Ajouter un Déclencheur à l'Attaque, réglé sur le défenseur, fait porter la capacité liée sur l'adversaire touché plutôt que sur le porteur ; le module Ajouter un Déclencheur à la Défense, réglé sur l'attaquant, la fait porter sur l'adversaire contré.

#### La fiche de module

Un module ajoute une propriété à la capacité. On en empile autant qu'on veut, même plusieurs fois le même : deux modules identiques ne cumulent jamais leurs bonus sur un même jet, chacun s'applique à un jet différent.

Chaque module se lit sur une fiche aux attributs fixes. L'en-tête porte ce qui ne change pas d'un palier à l'autre : la catégorie du module, les types auxquels il se greffe, son modificateur d'affinité d'emploi. Les paliers chiffrés portent ce qui monte avec la puissance, dans des colonnes toujours identiques.

<div class="defs" markdown>

**Conception (DR, DE, DT, DM, DC, DS) :** le coût pour concevoir le palier, payé une fois dans le développement de la catégorie du module, lui-même acheté sur le [développement intérieur](di.md) au taux de l'affinité d'apprentissage, par tranches de 10. Un module sans catégorie se paie directement en DI.

**CAR (VOL, LOG, INS, ERU, IMA, CHA selon l'école du module) :** la caractéristique mentale minimale exigée pour concevoir le palier ; chaque école a la sienne.

**UAA :** l'aura accumulée : l'aura que le lanceur rassemble sur sa réserve pour déclencher la capacité, dans la limite de son [UAR](aura.md) par round ; une capacité plus chère que l'UAR s'accumule sur plusieurs rounds.

**MA :** le maintien, l'aura payée chaque round par son mainteneur pour la garder active. À zéro pour une capacité instantanée.

**AEG / AEL :** le modificateur d'affinité d'emploi que porte le palier, un décalage en points de pourcentage ; « — » quand il est neutre. L'en-tête en dit le rang : AEG pour un décalage global, valant pour tous les modules de la capacité, qu'il soit porté par le socle, par un raccord ou par un module qui change la nature de la capacité entière ; AEL pour un décalage local, porté par le module et ne valant que pour lui.

</div>

Un module compte presque toujours plusieurs paliers, une suite de lignes de puissance croissante, dont on retient une seule à la conception. Certains s'étendent sur plusieurs grilles combinables : on en retient une ligne par grille, sauf mention de cumul.

Chaque fiche dit à quels types son module se greffe, et cette liste est contraignante : un module de bonus à l'attaque n'accepte que le type attaque.

#### Une catégorie par module

Chaque module relève d'une seule catégorie, ou d'aucune s'il est purement structurel. Les modules se rangent ainsi par école, chacune dans son chapitre.

Un même concept peut exister dans plusieurs catégories : il y figure alors comme autant d'entrées distinctes, une par école, chacune avec ses propres coûts. Une attaque qui poursuit sa cible, par exemple, se décline en une version d'émission et une version de manipulation. L'affinité se lit toujours sur l'unique catégorie de l'entrée employée.

Un module sans catégorie ne se convertit pas en points d'école : il se paie directement en DI, et aucune affinité ne le concerne. Les modules de raccord n'ont pas de catégorie ; ils figurent à la fin de ce chapitre.

#### La durée

La durée règle l'existence de la capacité dans le temps.

<div class="defs" markdown>

**Instantané :** la capacité se déclenche, se résout et disparaît ; son maintien est nul.

**À maintien :** la capacité persiste tant que le personnage la soutient, en payant son maintien chaque round.

</div>

Le porteur garde une capacité à maintien active tant qu'il touche sa cible, ce sur quoi son aura se pose. Avec la cible Soi-même, la capacité est posée sur son corps, en contact permanent : il la maintient sans autre condition et en paie la MA chaque round.

Avec toute autre cible, un adversaire, un allié, un objet ou une créature, le porteur la maintient de la même façon, sans relais, tant qu'il garde la cible au contact ou à ses côtés. Dès que la cible s'éloigne, le contact rompt : le maintien ne passe plus que par l'un des deux relais, prévu dès la conception de la capacité. Sans relais, l'éloignement met fin à la capacité.

Le premier relais, [Maintenir à Distance](emission.md), relie le porteur à la capacité par son aura ; son maintien augmente avec l'éloignement. Il vaut pour toute cible détachée : un adversaire, un allié, un objet ou une créature.

Le second relais est l'[Éveil au Nen](conjuration.md) réglé pour que l'entité s'entretienne seule, réservé à une créature ou un objet que le porteur a lui-même dressés. Ce réglage cède à l'entité une part de la réserve : l'entité devient le mainteneur de son propre socle, au contact comme au loin, et le porteur cesse d'en payer le maintien. Seul le maintien du socle passe ainsi à l'entité : son lanceur reste le porteur qui l'a dressée, et les rôles réglés en embarquant une capacité dans l'entité relèvent de cette capacité, non du socle.

L'autre réglage de l'Éveil au Nen, où le conjurateur garde le maintien, n'est pas un relais : le porteur maintient l'entité au contact ou par Maintenir à Distance. Le choix entre les deux réglages ne dépend pas de la distance : le porteur peut régler l'entité pour qu'elle s'entretienne seule même s'il la garde près de lui.

Une capacité instantanée n'a pas de maintien : elle se résout et disparaît.

À la conception, une capacité à maintien peut être réglée pour se soutenir à la minute plutôt qu'au round : elle ne réclame alors son maintien qu'une fois par minute, mais celui-ci coûte cinq fois sa valeur. C'est le régime des capacités que l'on garde longtemps, hors du combat, là où payer à chaque round n'aurait pas de sens ; en plein combat, où le round est l'unité, le maintien au round reste la règle.

#### L'affinité d'emploi et son modificateur

L'[affinité d'emploi](archetypes-nen.md) est un pourcentage propre au personnage, par catégorie, fixé par son archétype : sa catégorie au plus haut, les voisines en dessous, l'opposée au plus bas. Elle gouverne la puissance de son Nen dans cette catégorie.

Le modificateur d'affinité d'emploi ne crée pas une affinité nouvelle : il décale, vers le haut ou vers le bas, celle que l'archétype donne déjà à la catégorie concernée. Il existe à deux rangs : global, porté par la capacité, il vaut pour tous ses modules ; local, porté par un module, il ne vaut que pour lui.

Le modificateur ne touche que l'affinité d'emploi, la puissance, jamais l'affinité d'apprentissage, la vitesse de progression. Il porte sur la valeur de l'effet, non sur les coûts d'aura ou de conception.

L'affinité ne multiplie que les effets chiffrés : un bonus, des dégâts, un seuil. Un effet descriptif, un déclencheur, une faculté ou un nombre de capacités n'est pas multiplié, même si le module porte une valeur ; chaque fiche dit lequel des deux effets elle produit.

#### Les conditions

Une condition est un attribut facultatif qui s'attache soit à une capacité, soit à un module précis. Elle porte deux choses : son énoncé, la restriction ou le serment (« seulement contre tel adversaire », « seulement après l'avoir annoncé à voix haute ») ; et son effet de règle, un décalage du modificateur d'affinité d'emploi, en pourcentage signé.

Plus la condition est lourde, plus le décalage est favorable. Une condition ne coûte rien : son seul effet de règle est ce décalage.

L'effet reste strictement localisé au niveau d'attache : une condition posée sur la capacité décale le modificateur global, donc tous ses modules ; une condition posée sur un module ne décale que le sien. On peut cumuler plusieurs conditions au même niveau ; leurs décalages s'ajoutent en points de pourcentage.

#### La composition, module par module

L'affinité d'emploi effective se lit module par module, jamais pour la capacité en bloc : chaque module peut relever d'une autre catégorie et porter son propre modificateur. Pour un module donné, on empile, du plus large au plus fin :

1. la base : l'affinité d'emploi d'archétype du personnage dans la catégorie de ce module ;
2. le modificateur global de la capacité, partagé par tous les modules ;
3. le modificateur local du module, propre à lui ;
4. les décalages des conditions, chacune à son niveau.

Les décalages des niveaux 2 à 4 s'ajoutent en points de pourcentage à la base : leur somme donne l'affinité d'emploi effective du module, 100 % pour une catégorie tenue à son sommet. Cette affinité multiplie la valeur de l'effet : un module de +30 à l'attaque, employé à 120 % d'affinité effective, donne +36 ; une affinité sous 100 % réduit l'effet d'autant, et un modificateur négatif peut le réduire davantage. Le total des décalages des niveaux 2 à 4 ne dépasse jamais +100 % : des bonus peuvent le porter au-delà, mais on n'en applique jamais plus.

### Créer une capacité, pas à pas

On crée une capacité en six étapes, du socle jusqu'aux coûts. Un même exemple, une capacité offensive, suit ces étapes d'un bout à l'autre.

#### 1. Poser le socle

On choisit d'abord le type de la capacité, son socle : attaque, défense ou effet. Ce choix oriente les modules à venir et fixe la façon dont la capacité se résout.

> Exemple. Le personnage veut une capacité qui frappe fort. Il pose un socle d'attaque.

#### 2. Choisir le module principal

On retient ensuite le module principal, celui qui porte l'effet central de la capacité. On lit sa fiche : sa catégorie, les types qu'elle accepte, son modificateur d'affinité, puis le palier retenu et les quatre valeurs de ce palier : la conception, la CAR, l'UAA et la MA.

> Exemple. Le module central est Attaque, de la catégorie renforcement, décliné en Armes de mêlée. Le personnage en retient le palier +60 : 15 DR, CAR 10, UAA 120, MA 70.

#### 3. Empiler les modules secondaires

On ajoute autant de modules qu'on veut, un palier par module, dans la limite du développement intérieur disponible. Ils affinent ou étendent la capacité ; chacun apporte sa propre ligne de coûts et peut relever d'une autre catégorie que le module principal.

> Exemple. Le personnage greffe un second module de renforcement, Dégâts, au palier +40 : 10 DR, CAR 8, UAA 50, MA 20.

#### 4. Régler la durée, le modificateur et les conditions

On fixe la durée, instantanée ou à maintien, au round ou à la minute ; on pose le modificateur d'affinité d'emploi global de la capacité ; et l'on ajoute les conditions éventuelles, chacune décalant l'affinité à son niveau.

> Exemple. La capacité sera à maintien. Le personnage y attache une condition : elle ne frappe que contre un adversaire qu'il a nommé à voix haute. Cette restriction lui vaut un décalage de +20 % sur toute la capacité.

#### 5. Additionner les coûts

On somme les coûts des modules retenus. La conception est la somme de leurs coûts de développement, regroupés par catégorie (DR, DE, etc.), puis achetés sur le développement intérieur au taux de l'affinité d'apprentissage, par tranches de 10 DI. L'UAA est la somme de leurs UAA, dépensée pour employer la capacité ; la MA, la somme de leurs maintiens, payée à chaque round tant qu'elle dure. La CAR de la capacité entière est la plus haute de celles de ses paliers.

> Exemple. 15 + 10 = 25 DR ; à 100 % d'affinité de renforcement, ces 25 DR coûtent 30 DI (10 DI pour 10 DR, par tranches de 10) ; UAA 120 + 50 = 170 ; MA 70 + 20 = 90 ; CAR, la plus haute des deux, 10.

#### 6. Appliquer l'affinité aux valeurs d'effet

On lit enfin, module par module, l'affinité d'emploi effective, en empilant la base d'archétype, le modificateur global, le modificateur local et les conditions, comme l'expose la composition. Cette affinité multiplie la valeur des seuls effets chiffrés.

> Exemple. Le personnage est un renforceur : sa catégorie de renforcement est à 100 %. La condition posée y ajoute 20 %, portant l'affinité effective de ses deux modules à 120 %. Le bonus à l'attaque passe de +60 à +72, celui aux dégâts de +40 à +48. La capacité achevée : à maintien, 25 DR de conception (soit 30 DI), 170 d'aura à l'emploi, 90 de maintien par round, CAR 10 ; et, contre l'adversaire nommé, +72 à l'attaque et +48 aux dégâts.

</div>

---

## Modules sans catégorie {: style="text-align: center" }

<div class="cols" markdown>

Un module de raccord n'appartient à aucune école : il se greffe sur le type de capacité que dit sa fiche et se paie directement en DI, sans conversion par une affinité d'apprentissage.

<div class="cj-modules anima" markdown>

<div class="keep" markdown>

#### Ajouter un Déclencheur à l'Attaque

<p class="mod-type">Catégorie : aucune<br>
Types : attaque</p>

Greffé sur une attaque, ce module y attache une capacité liée, une seule, qu'il déclenche quand l'attaque aboutit selon les conditions choisies. La capacité liée peut elle-même porter un déclencheur : les déclenchements s'enchaînent.

Le personnage retient obligatoirement un degré de touche et une visée dans la table ci-dessous, et peut y joindre une cible ; sans cible retenue, la capacité liée garde sa cible par défaut, le porteur. Plus les options retenues sont dures, plus l'affinité accordée monte ; cette affinité s'ajoute à l'affinité globale de la capacité liée.

La capacité liée paie ses propres coûts. Le module, lui, se paie en DI, et le déclencheur coûte une aura et un maintien propres, lus à la ligne de la visée retenue.

<table>
<thead><tr><th>Effet</th><th>DI</th><th>CAR</th><th>UAA</th><th>MA</th><th>AEG</th></tr></thead>
<tbody>
<tr class="cat"><td>Cible</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Attaquant</td><td>0</td><td>—</td><td>0</td><td>0</td><td>—</td></tr>
<tr><td>Défenseur</td><td>0</td><td>—</td><td>0</td><td>0</td><td>−20%</td></tr>
<tr class="cat"><td>Degré de touche (obligatoire)</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Touche de 0 %</td><td>0</td><td>—</td><td>0</td><td>0</td><td>−20%</td></tr>
<tr><td>Touche de 20 %</td><td>0</td><td>—</td><td>0</td><td>0</td><td>−10%</td></tr>
<tr><td>Touche de 40 %</td><td>0</td><td>—</td><td>0</td><td>0</td><td>—</td></tr>
<tr><td>Touche de 60 %</td><td>5</td><td>—</td><td>0</td><td>0</td><td>+10%</td></tr>
<tr><td>Touche de 80 %</td><td>5</td><td>—</td><td>0</td><td>0</td><td>+20%</td></tr>
<tr><td>Touche de 100 %</td><td>10</td><td>—</td><td>0</td><td>0</td><td>+30%</td></tr>
<tr><td>Touche de 120 %</td><td>10</td><td>—</td><td>0</td><td>0</td><td>+40%</td></tr>
<tr><td>Touche de 140 %</td><td>15</td><td>—</td><td>0</td><td>0</td><td>+50%</td></tr>
<tr><td>Touche de 160 %</td><td>15</td><td>—</td><td>0</td><td>0</td><td>+60%</td></tr>
<tr><td>Touche de 180 %</td><td>20</td><td>—</td><td>0</td><td>0</td><td>+70%</td></tr>
<tr><td>Touche de 200 %</td><td>20</td><td>—</td><td>0</td><td>0</td><td>+80%</td></tr>
<tr class="cat"><td>Visée (obligatoire)</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Pas de point précis</td><td>0</td><td>—</td><td>20</td><td>20</td><td>−20%</td></tr>
<tr><td>Torse, mollet (−10)</td><td>0</td><td>—</td><td>20</td><td>20</td><td>−10%</td></tr>
<tr><td>Abdomen, bras, avant-bras, cuisse (−20)</td><td>0</td><td>—</td><td>40</td><td>20</td><td>—</td></tr>
<tr><td>Épaule, hanche (−30)</td><td>5</td><td>—</td><td>40</td><td>20</td><td>+10%</td></tr>
<tr><td>Estomac, main, poignet, genou (−40)</td><td>5</td><td>—</td><td>60</td><td>40</td><td>+20%</td></tr>
<tr><td>Poumon, foie, cheville, pied (−50)</td><td>10</td><td>—</td><td>60</td><td>40</td><td>+30%</td></tr>
<tr><td>Tête, bouche, cœur, coude, aine (−60)</td><td>10</td><td>—</td><td>80</td><td>40</td><td>+40%</td></tr>
<tr><td>Oreille, nez, testicules (−70)</td><td>15</td><td>—</td><td>100</td><td>40</td><td>+50%</td></tr>
<tr><td>Cou, vulve (−80)</td><td>15</td><td>—</td><td>120</td><td>60</td><td>+60%</td></tr>
<tr><td>Doigt (−90)</td><td>20</td><td>—</td><td>140</td><td>60</td><td>+70%</td></tr>
<tr><td>Œil (−100)</td><td>20</td><td>—</td><td>160</td><td>60</td><td>+80%</td></tr>
</tbody>
</table>

<div class="defs" markdown>

**Cible :** qui doit être touché pour armer le déclencheur. Celui qu'il faut toucher devient aussi la cible de la capacité liée : réglé sur le défenseur, le déclencheur la fait porter sur cet adversaire ; réglé sur l'attaquant, sur le porteur.

**Degré de touche :** la marge de réussite exigée de l'attaque, de 0 % à 200 % ; plus la marge exigée est haute, plus l'affinité accordée monte.

**Visée :** la partie du corps visée, reprise de la manœuvre [Viser](../combat/manoeuvres.md) ; plus le point est petit et son malus de visée fort, plus l'affinité accordée monte.

**Affinité accordée :** la somme des affinités des options retenues, ajoutée à l'affinité globale de la capacité liée ; le plafond commun de +100 % s'applique comme à tout module.

**Coût :** l'aura et le maintien du déclencheur se lisent à la ligne de la visée retenue. Le DI suit l'affinité accordée : une option neutre ou à malus ne coûte rien, une option à bonus coûte 5 DI par tranche de 20 % accordée. La capacité liée paie ses propres coûts quand elle se déclenche.

</div>

</div>

<div class="keep" markdown>

#### Ajouter un Déclencheur à la Défense

<p class="mod-type">Catégorie : aucune<br>
Types : défense</p>

Greffé sur une défense, ce module y attache une capacité liée, une seule, qu'il déclenche quand la défense aboutit selon les conditions choisies. La capacité liée peut elle-même porter un déclencheur : les déclenchements s'enchaînent.

Le personnage retient obligatoirement un degré de défense et une visée dans la table ci-dessous, et peut y joindre une cible ; sans cible retenue, la capacité liée garde sa cible par défaut, le porteur. Plus les options retenues sont dures, plus l'affinité accordée monte ; cette affinité s'ajoute à l'affinité globale de la capacité liée.

La capacité liée paie ses propres coûts. Le module, lui, se paie en DI, et le déclencheur coûte une aura et un maintien propres, lus à la ligne de la visée retenue.

<table>
<thead><tr><th>Effet</th><th>DI</th><th>CAR</th><th>UAA</th><th>MA</th><th>AEG</th></tr></thead>
<tbody>
<tr class="cat"><td>Cible</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Défenseur</td><td>0</td><td>—</td><td>0</td><td>0</td><td>—</td></tr>
<tr><td>Attaquant</td><td>0</td><td>—</td><td>0</td><td>0</td><td>−20%</td></tr>
<tr class="cat"><td>Degré de défense (obligatoire)</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Défense de 0 %</td><td>0</td><td>—</td><td>0</td><td>0</td><td>−20%</td></tr>
<tr><td>Défense de 20 %</td><td>0</td><td>—</td><td>0</td><td>0</td><td>−10%</td></tr>
<tr><td>Défense de 40 %</td><td>0</td><td>—</td><td>0</td><td>0</td><td>—</td></tr>
<tr><td>Défense de 60 %</td><td>5</td><td>—</td><td>0</td><td>0</td><td>+10%</td></tr>
<tr><td>Défense de 80 %</td><td>5</td><td>—</td><td>0</td><td>0</td><td>+20%</td></tr>
<tr><td>Défense de 100 %</td><td>10</td><td>—</td><td>0</td><td>0</td><td>+30%</td></tr>
<tr><td>Défense de 120 %</td><td>10</td><td>—</td><td>0</td><td>0</td><td>+40%</td></tr>
<tr><td>Défense de 140 %</td><td>15</td><td>—</td><td>0</td><td>0</td><td>+50%</td></tr>
<tr><td>Défense de 160 %</td><td>15</td><td>—</td><td>0</td><td>0</td><td>+60%</td></tr>
<tr><td>Défense de 180 %</td><td>20</td><td>—</td><td>0</td><td>0</td><td>+70%</td></tr>
<tr><td>Défense de 200 %</td><td>20</td><td>—</td><td>0</td><td>0</td><td>+80%</td></tr>
<tr class="cat"><td>Visée (obligatoire)</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Pas de point précis</td><td>0</td><td>—</td><td>20</td><td>20</td><td>−20%</td></tr>
<tr><td>Torse, mollet (−10)</td><td>0</td><td>—</td><td>20</td><td>20</td><td>−10%</td></tr>
<tr><td>Abdomen, bras, avant-bras, cuisse (−20)</td><td>0</td><td>—</td><td>40</td><td>20</td><td>—</td></tr>
<tr><td>Épaule, hanche (−30)</td><td>5</td><td>—</td><td>40</td><td>20</td><td>+10%</td></tr>
<tr><td>Estomac, main, poignet, genou (−40)</td><td>5</td><td>—</td><td>60</td><td>40</td><td>+20%</td></tr>
<tr><td>Poumon, foie, cheville, pied (−50)</td><td>10</td><td>—</td><td>60</td><td>40</td><td>+30%</td></tr>
<tr><td>Tête, bouche, cœur, coude, aine (−60)</td><td>10</td><td>—</td><td>80</td><td>40</td><td>+40%</td></tr>
<tr><td>Oreille, nez, testicules (−70)</td><td>15</td><td>—</td><td>100</td><td>40</td><td>+50%</td></tr>
<tr><td>Cou, vulve (−80)</td><td>15</td><td>—</td><td>120</td><td>60</td><td>+60%</td></tr>
<tr><td>Doigt (−90)</td><td>20</td><td>—</td><td>140</td><td>60</td><td>+70%</td></tr>
<tr><td>Œil (−100)</td><td>20</td><td>—</td><td>160</td><td>60</td><td>+80%</td></tr>
</tbody>
</table>

<div class="defs" markdown>

**Cible :** qui reçoit la capacité quand la défense aboutit. Celui que vise le déclencheur devient la cible de la capacité liée : réglé sur l'attaquant, le déclencheur la fait porter sur cet adversaire ; réglé sur le défenseur, sur le porteur.

**Degré de défense :** la marge de réussite exigée de la défense, de 0 % à 200 % ; plus la marge exigée est haute, plus l'affinité accordée monte.

**Visée :** le point par où la capacité liée atteint l'attaquant au contact de la défense, repris de la manœuvre [Viser](../combat/manoeuvres.md) ; plus le point est petit et son malus fort, plus l'affinité accordée monte.

**Affinité accordée :** la somme des affinités des options retenues, ajoutée à l'affinité globale de la capacité liée ; le plafond commun de +100 % s'applique comme à tout module.

**Coût :** l'aura et le maintien du déclencheur se lisent à la ligne de la visée retenue. Le DI suit l'affinité accordée : une option neutre ou à malus ne coûte rien, une option à bonus coûte 5 DI par tranche de 20 % accordée. La capacité liée paie ses propres coûts quand elle se déclenche.

</div>

</div>

<div class="keep" markdown>

#### Ajouter une Capacité à une Créature

<p class="mod-type">Catégorie : aucune<br>
Types : créature</p>

Greffé sur une créature, ce module lui embarque une capacité liée, une seule, qu'elle emploie comme sienne. On peut greffer plusieurs fois ce module pour confier plusieurs capacités à la même créature.

La capacité liée paie sa propre conception et son aura à l'emploi ; le module, lui, se paie en DI. Employée par la créature, la capacité garde l'affinité d'emploi de celui qui l'a raccordée, la créature n'ayant pas d'affinité propre.

Celui qui a raccordé la capacité règle aussi qui la lance et qui la maintient. Lanceur et mainteneur se règlent séparément, en toute combinaison ; pour une capacité instantanée, sans maintien, le réglage du mainteneur reste sans effet. Ces rôles ne dépendent pas de la façon dont la créature emploie la capacité, mais de son entretien : par défaut, ils suivent l'entité, à elle si elle s'entretient seule, au conjurateur sinon ; on peut aussi les attribuer d'office à la créature. L'aura que la capacité dérobe ou gagne revient toujours à son lanceur.

L'entretien relève de l'[Éveil au Nen](conjuration.md), qui règle deux choses distinctes : que la créature manie le Nen, ce qui lui donne l'usage d'une réserve propre et suffit à lui donner un rôle ; et qu'elle s'entretienne seule ou non, ce qui fixe les défauts : une entité qui s'entretient seule déclenche et tient ses capacités sur sa propre réserve, et les deux rôles lui reviennent donc par défaut. Une créature peut manier le Nen sans s'entretenir seule.

<table>
<thead><tr><th>Emploi</th><th>DI</th><th>CAR</th><th>UAA</th><th>MA</th><th>AEG</th></tr></thead>
<tbody>
<tr><td>Sur ordre du conjurateur</td><td>10</td><td>—</td><td>0</td><td>0</td><td>—</td></tr>
<tr><td>D'elle-même</td><td>25</td><td>—</td><td>0</td><td>0</td><td>—</td></tr>
<tr class="cat"><td>Lanceur (obligatoire)</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Le lanceur suit l'entité (défaut)</td><td>0</td><td>—</td><td>0</td><td>0</td><td>—</td></tr>
<tr><td>La créature en devient le lanceur</td><td>0</td><td>—</td><td>0</td><td>0</td><td>—</td></tr>
<tr class="cat"><td>Mainteneur (obligatoire)</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Le mainteneur suit l'entité (défaut)</td><td>0</td><td>—</td><td>0</td><td>0</td><td>—</td></tr>
<tr><td>La créature en devient le mainteneur</td><td>0</td><td>—</td><td>0</td><td>0</td><td>—</td></tr>
</tbody>
</table>

<div class="defs" markdown>

**Sur ordre du conjurateur :** la créature n'emploie la capacité que lorsque le conjurateur le lui commande.

**D'elle-même :** la créature l'emploie quand elle le juge bon, sans attendre d'ordre ; réservé à une créature indépendante.

**Le lanceur suit l'entité :** la créature la déclenche elle-même, sur sa réserve propre, si elle s'entretient seule, ce qui suppose qu'elle manie le Nen ; le conjurateur sinon, qui en paie alors l'UAA.

**La créature en devient le lanceur :** la créature déclenche elle-même la capacité, quel que soit son entretien, sur sa réserve propre, et en paie l'UAA ; l'aura que la capacité dérobe ou gagne lui revient. Ce réglage exige que la créature manie déjà le Nen, prérequis qu'il n'accorde pas : sans lui, le rôle reste au conjurateur. Il sert la créature qui manie le Nen sans s'entretenir seule ; celle qui s'entretient seule tient déjà ce rôle par défaut.

**Le mainteneur suit l'entité :** la créature la tient elle-même, sur sa réserve propre, si elle s'entretient seule, ce qui suppose qu'elle manie le Nen ; le conjurateur sinon, qui en paie alors la MA.

**La créature en devient le mainteneur :** la créature tient elle-même la capacité, quel que soit son entretien, sur sa réserve propre, et en paie la MA chaque round. Ce réglage exige que la créature manie déjà le Nen, prérequis qu'il n'accorde pas : sans lui, le rôle reste au conjurateur. Il sert la créature qui manie le Nen sans s'entretenir seule ; celle qui s'entretient seule tient déjà ce rôle par défaut.

</div>

</div>

<div class="keep" markdown>

#### Ajouter une Capacité à un Objet

<p class="mod-type">Catégorie : aucune<br>
Types : objet</p>

Greffé sur un objet, ce module lui embarque une capacité liée, une seule, qu'il libère à l'emploi. On peut greffer plusieurs fois ce module pour doter le même objet de plusieurs capacités.

La capacité liée paie sa propre conception et son aura ; le module, lui, se paie en DI. Employée par l'objet, la capacité garde l'affinité d'emploi de celui qui l'a raccordé.

Celui qui a raccordé la capacité règle aussi qui la lance et qui la maintient. Lanceur et mainteneur se règlent séparément, en toute combinaison ; pour une capacité instantanée, sans maintien, le réglage du mainteneur reste sans effet. Par défaut, ces rôles suivent l'objet : à lui s'il s'entretient seul, à celui qui l'a raccordé sinon ; on peut aussi les attribuer d'office à l'objet. L'aura que la capacité dérobe ou gagne revient toujours à son lanceur.

L'[Éveil au Nen](conjuration.md) donne à l'objet une réserve propre, le minimum pour prendre un rôle, et règle à part s'il s'entretient seul.

<table>
<thead><tr><th>Emploi</th><th>DI</th><th>CAR</th><th>UAA</th><th>MA</th><th>AEG</th></tr></thead>
<tbody>
<tr><td>À l'usage de l'objet</td><td>10</td><td>—</td><td>0</td><td>0</td><td>—</td></tr>
<tr><td>De lui-même</td><td>25</td><td>—</td><td>0</td><td>0</td><td>—</td></tr>
<tr class="cat"><td>Lanceur (obligatoire)</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Le lanceur suit l'entité (défaut)</td><td>0</td><td>—</td><td>0</td><td>0</td><td>—</td></tr>
<tr><td>L'objet en devient le lanceur</td><td>0</td><td>—</td><td>0</td><td>0</td><td>—</td></tr>
<tr class="cat"><td>Mainteneur (obligatoire)</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Le mainteneur suit l'entité (défaut)</td><td>0</td><td>—</td><td>0</td><td>0</td><td>—</td></tr>
<tr><td>L'objet en devient le mainteneur</td><td>0</td><td>—</td><td>0</td><td>0</td><td>—</td></tr>
</tbody>
</table>

<div class="defs" markdown>

**À l'usage de l'objet :** l'objet libère la capacité quand on s'en sert, au contact ou d'un geste.

**De lui-même :** l'objet emploie la capacité sans qu'on se serve de lui ; réservé à un objet doté d'une conscience.

**Le lanceur suit l'entité :** l'objet la déclenche lui-même, sur sa réserve propre, s'il s'entretient seul, ce qui suppose qu'il soit éveillé au Nen ; celui qui l'a raccordé sinon, qui en paie alors l'UAA.

**L'objet en devient le lanceur :** l'objet déclenche lui-même la capacité, quel que soit son entretien, sur sa réserve propre, et en paie l'UAA ; l'aura que la capacité dérobe ou gagne lui revient. Ce réglage exige que l'objet soit déjà éveillé au Nen, prérequis qu'il n'accorde pas : sans lui, le rôle reste à celui qui l'a raccordé. Il sert l'objet éveillé qui ne s'entretient pas seul ; celui qui s'entretient seul tient déjà ce rôle par défaut.

**Le mainteneur suit l'entité :** l'objet la tient lui-même, sur sa réserve propre, s'il s'entretient seul, ce qui suppose qu'il soit éveillé au Nen ; celui qui l'a raccordé sinon, qui en paie alors la MA.

**L'objet en devient le mainteneur :** l'objet tient lui-même la capacité, quel que soit son entretien, sur sa réserve propre, et en paie la MA chaque round. Ce réglage exige que l'objet soit déjà éveillé au Nen, prérequis qu'il n'accorde pas : sans lui, le rôle reste à celui qui l'a raccordé. Il sert l'objet éveillé qui ne s'entretient pas seul ; celui qui s'entretient seul tient déjà ce rôle par défaut.

</div>

</div>

</div>

</div>
