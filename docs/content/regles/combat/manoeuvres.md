# Attaque et Défense

<div class="cols" markdown>

### Attaque

Une attaque est l'action par laquelle un personnage cherche à atteindre un adversaire. Attaquer prend une action et un personnage ne peut normalement utiliser cette action qu'une fois par round.

Avant de lancer les dés, le personnage compose son attaque. Il choisit d'abord l'arme avec laquelle il attaque, puis le type d'attaque qu'il en fait, parmi ceux que l'arme permet : arme de mêlée, arme de jet, arme de trait ou arme à feu. Ce type fixe la compétence employée pour le jet d'attaque.

Il choisit ensuite les options d'attaque qu'il emploie, comme Viser ou Attaquer en retard, puis sélectionne la manœuvre que suit son attaque. Les options restent facultatives ; la manœuvre, elle, est toujours choisie.

Après avoir annoncé ses options et sa manœuvre, le personnage fait un jet d'attaque opposé au jet de défense de l'adversaire. Il lance d'abord son jet de compétence, calcule son résultat final et l'annonce au défenseur ; celui-ci résout ensuite sa défense. Si le résultat final de l'attaque est supérieur ou égal au résultat final de la défense, on dit que l'attaque touche et on calcule alors le degré de touche ; sinon, elle manque.

Le degré de touche mesure la marge de la réussite : c'est le résultat final de l'attaque moins le résultat final de la défense, lu en pourcentage et toujours arrondi à la dizaine inférieure (une marge de 32 donne 30 %). Le degré de touche ne peut pas dépasser 200 %, c'est le maximum possible. Si le degré de touche atteint 200 %, on considère alors qu'il s'agit d'un critique (voir Critique et Blessures).

Le degré de touche commande ce que l'attaque produit ; chaque manœuvre précise l'usage qu'elle en fait.

### Postures de combat

Durant son tour, le personnage peut prendre une posture de combat. Prendre une posture de combat coûte 1 action et dure jusqu'au début du prochain tour du personnage. Il est impossible de prendre plus d'une posture dans le même round et un personnage ne peut en tenir qu'une à la fois, gardant toujours la dernière posture prise.

Les postures sont :

<div class="defs" markdown>

**Défensive partielle :** Le personnage privilégie sa garde. Tant qu'il maintient cette posture, il obtient un +10 à ses jets de défense et un −30 à ses jets d'attaques.

**Défensive totale :** Le personnage se consacre tout entier à sa protection. Tant qu'il maintient cette posture, il obtient un +30 à ses jets de défense et ne peut effectuer que des attaques avec la manœuvre Toucher.

**Offensive partielle :** Le personnage appuie son attaque. Tant qu'il maintient cette posture, il obtient un +10 à ses jets d'attaques et un −30 à ses jets de défense.

**Offensive totale :** Le personnage attaque à corps perdu. Tant qu'il maintient cette posture, il obtient un +30 à ses jets d'attaques et ne peut effectuer que des défenses avec la manœuvre Se laisser toucher.

</div>

| Posture | Attaque | Défense |
|---|:---:|:---:|
| Défensive partielle | −30 | +10 |
| Défensive totale | Spécial | +30 |
| Offensive partielle | +10 | −30 |
| Offensive totale | +30 | Spécial |

### Employer une manœuvre

Une manœuvre est une façon particulière de porter une attaque ou d'opposer une défense. Une action de combat ordinaire se règle par son seul jet ; une manœuvre y ajoute un tour de main et échange l'effet habituel contre un autre : projeter la cible, la désarmer, l'agripper, riposter ou se protéger autrement. Le personnage annonce la manœuvre employée avant de lancer les dés.

Les manœuvres se rangent en deux familles, selon qu'elles servent à frapper ou à se défendre : les manœuvres d'attaque et les manœuvres de défense.

### Manœuvres d'attaque

Lorsqu'il effectue une attaque, le personnage doit choisir une manœuvre. Il ne peut choisir qu'une seule manœuvre par attaque et doit faire le choix avant de lancer les dés.

Si d'une manière ou d'une autre, le personnage est capable d'utiliser plusieurs manœuvres dans une même attaque, il n'effectue qu'un seul jet d'attaque pour toutes les manœuvres qui nécessitent un jet d'attaque. À cette attaque, il applique évidemment tous les malus des manœuvres utilisées.

<div class="mcard" markdown>
**Blesser** <span class="prereq">Prérequis : aucun</span> Sur une touche, la cible subit les dégâts de l'arme en fonction du degré de touche.

<p class="formula">Dégâts = dégâts de l'arme × degré de touche ÷ 100</p>

Par exemple, à 0 %, le personnage touche mais ne fait (généralement) pas de dégâts, à 50 % il effectue la moitié des dégâts de l'arme, à 100 % il effectue les dégâts normaux de l'arme et à 200 % le personnage fait le double de dégâts de l'arme.

Si le personnage Vise dans son attaque, la blessure éventuelle se localise sur la zone visée (voir Blessures) au lieu d'être tirée au hasard.

Blesser est la manœuvre par défaut : si un personnage effectue une attaque sans préciser la manœuvre qu'il utilise, alors on considère qu'il utilise Blesser.
</div>

<div class="mcard" markdown>
**Assommer** <span class="prereq">Prérequis : aucun</span> Le personnage fait le jet d'attaque opposé au jet de défense de l'adversaire avec un malus de −40 ; sur une touche, l'attaque n'inflige aucun dégât. Mais en échange, son seuil de critique s'abaisse : l'attaque devient un critique à partir d'un degré de touche de 100 %, au lieu des 200 % ordinaires.

Sur un critique, on calcule la gravité du coup et on en tire le degré de blessure, comme pour une blessure grave (voir Critique et Blessures) ; les dégâts que l'attaque aurait infligés avec la manœuvre Blesser tiennent lieu de dégâts subis. La cible ne reçoit pas cette blessure : le degré de blessure fixe seulement la difficulté d'un jet de Résistance à la Douleur, donnée par la table ci-dessous. Si la cible rate ce jet, elle sombre dans l'Inconscience (voir États) pendant 1 heure ; si elle le réussit, elle reste consciente.

| Degré de blessure | Résistance à la Douleur |
|:---:|:---:|
| 1 | Difficile (120) |
| 2 | Très difficile (180) |
| 3 | Absurde (240) |
| 4 | Quasi impossible (320) |
| 5 | Impossible (400) |

Si le personnage Vise dans son attaque, un coup au bon endroit étourdit bien plus sûrement : la zone visée ajoute un bonus à la gravité du coup. Les zones absentes de la liste n'ajoutent rien.

<div class="zones">
<div class="zone">
<p class="zone-chips"><span class="zlbl">Zone visée</span><span class="zchip">Tête</span></p>
<p class="zone-effet"><span class="zlbl">Effet</span>+100 à la gravité.</p>
</div>
<div class="zone">
<p class="zone-chips"><span class="zlbl">Zone visée</span><span class="zchip">Cou</span><span class="zchip">Bouche</span></p>
<p class="zone-effet"><span class="zlbl">Effet</span>+80 à la gravité.</p>
</div>
<div class="zone">
<p class="zone-chips"><span class="zlbl">Zone visée</span><span class="zchip">Foie</span><span class="zchip">Testicules</span><span class="zchip">Estomac</span></p>
<p class="zone-effet"><span class="zlbl">Effet</span>+60 à la gravité.</p>
</div>
<div class="zone">
<p class="zone-chips"><span class="zlbl">Zone visée</span><span class="zchip">Oreille</span><span class="zchip">Aine</span><span class="zchip">Vulve</span></p>
<p class="zone-effet"><span class="zlbl">Effet</span>+40 à la gravité.</p>
</div>
</div>

Si un même coup porte à la fois Assommer et une autre manœuvre, leurs critiques se règlent séparément : celui d'Assommer se déclenche à partir de 100 % de degré de touche et n'ouvre que le jet de Résistance à la Douleur ; celui de l'autre manœuvre attend le seuil ordinaire de 200 % et produit son effet habituel, comme la blessure grave de Blesser. Chacun se résout avec ses propres jets, et l'un peut survenir sans l'autre.
</div>

<div class="mcard" markdown>
**Agripper** <span class="prereq">Prérequis : Arme possédant la propriété Saisie</span> Le personnage fait le jet d'attaque opposé au jet de défense de l'adversaire avec un malus de −40 ; sur une touche, le personnage fait un jet de lutte opposé au jet de lutte ou de contorsion de l'adversaire, avec un bonus égal à la moitié du degré de touche, jusqu'à un maximum de +100 (un degré de touche de 30 % donne +15). En cas de réussite, la cible devient Agrippée (voir États).

Tant qu'il maintient la prise, le personnage subit lui aussi une Paralysie légère et ne peut pas utiliser pour une attaque l'arme qui tient la prise ni le membre qui la porte, sauf quand il utilise la manœuvre Maîtriser. Il peut lâcher la prise à tout moment (aucune action requise).

Le personnage peut tenir plusieurs prises en même temps, sur plusieurs adversaires ou sur plusieurs zones d'un même adversaire. Un adversaire tenu à plusieurs zones subit les effets de chaque zone.

L'adversaire peut se libérer en prenant une action : le personnage fait un nouveau jet de lutte opposé au jet de lutte ou de contorsion de l'adversaire. Si l'adversaire l'emporte, il se dégage et ne subit plus l'état Agrippé.

Si le personnage Vise dans son attaque, la prise produit un effet supplémentaire, donné ci-dessous par la zone saisie. Tant que l'adversaire est agrippé, il ne peut accomplir aucune action physique employant la partie bloquée, hormis tenter de se libérer de la prise, et il subit les états indiqués. Les zones absentes de la liste n'ajoutent rien.

<div class="zones">
<div class="zone">
<p class="zone-chips"><span class="zlbl">Zone saisie</span><span class="zchip">Cou</span><span class="zchip">Tête</span><span class="zchip">Bouche</span><span class="zchip">Nez</span><span class="zchip">Oreille</span></p>
<p class="zone-effet"><span class="zlbl">Effet</span>Bloque la tête et inflige l'état Mutisme léger (voir États).</p>
</div>
<div class="zone">
<p class="zone-chips"><span class="zlbl">Zone saisie</span><span class="zchip">Épaule</span><span class="zchip">Coude</span><span class="zchip">Bras</span><span class="zchip">Avant-bras</span></p>
<p class="zone-effet"><span class="zlbl">Effet</span>Bloque le bras saisi.</p>
</div>
<div class="zone">
<p class="zone-chips"><span class="zlbl">Zone saisie</span><span class="zchip">Poignet</span><span class="zchip">Main</span><span class="zchip">Doigt</span></p>
<p class="zone-effet"><span class="zlbl">Effet</span>Bloque la main saisie.</p>
</div>
<div class="zone">
<p class="zone-chips"><span class="zlbl">Zone saisie</span><span class="zchip">Hanche</span><span class="zchip">Cuisse</span><span class="zchip">Genou</span></p>
<p class="zone-effet"><span class="zlbl">Effet</span>Bloque la jambe saisie.</p>
</div>
<div class="zone">
<p class="zone-chips"><span class="zlbl">Zone saisie</span><span class="zchip">Mollet</span><span class="zchip">Cheville</span><span class="zchip">Pied</span></p>
<p class="zone-effet"><span class="zlbl">Effet</span>Bloque le pied saisi.</p>
</div>
</div>

Si le personnage est capable d'utiliser plusieurs manœuvres dans une même attaque, dont Agripper, Maîtriser et Soumettre, il peut les employer en même temps : les prises se font d'un même geste, et il n'a donc pas besoin d'avoir la cible Agrippée pour utiliser Maîtriser, ni d'avoir la cible Maîtrisée pour utiliser Soumettre. Il n'effectue alors qu'un seul jet de lutte, valable pour toutes ces manœuvres : en cas de réussite, leurs effets s'appliquent tous et la cible atteint directement le cran le plus élevé employé.
</div>

<div class="mcard" markdown>
**Maîtriser** <span class="prereq">Prérequis : cible Agrippée par le personnage</span> Le personnage fait le jet d'attaque opposé au jet de défense de l'adversaire avec un malus de −40 ; sur une touche, le personnage fait un jet de lutte opposé au jet de lutte ou de contorsion de la cible qu'il tient, avec un bonus égal à la moitié du degré de touche, jusqu'à un maximum de +100. En cas de réussite, la cible passe d'Agrippée à Maîtrisée (voir États).

Tant qu'il maintient la prise, le personnage subit lui aussi une Paralysie partielle et ne peut pas utiliser pour une attaque l'arme qui tient la prise ni le membre qui la porte, sauf quand il utilise la manœuvre Soumettre. Il peut lâcher la prise à tout moment (aucune action requise).

Le personnage peut tenir plusieurs prises en même temps, sur plusieurs adversaires ou sur plusieurs zones d'un même adversaire. Un adversaire tenu à plusieurs zones subit les effets de chaque zone.

Le personnage peut décider de ne pas faire de jet d'attaque, car il tient déjà son adversaire : on considère que le degré de touche vaut 0 % (donc sans aucun bonus) et qu'il ne peut être augmenté d'aucune manière (ce qui inclut Éraflure). Il fait alors directement son jet d'opposition de lutte sans le bonus.

L'adversaire peut se libérer en prenant une action : le personnage fait un nouveau jet de lutte opposé au jet de lutte ou de contorsion de l'adversaire. Si l'adversaire l'emporte, il redevient seulement Agrippé.

Si la prise visait une partie précise du corps (Agripper avec l'option Viser), ses effets persistent : le personnage tient déjà la cible et n'a pas besoin de Viser à nouveau. Il peut en revanche Viser une autre zone : son jet d'attaque subit alors le malus de cette zone et, si la manœuvre réussit, la prise se déplace sur la nouvelle zone, dont les effets remplacent les précédents. Certaines parties donnent en plus un effet supplémentaire :

<div class="zones">
<div class="zone">
<p class="zone-chips"><span class="zlbl">Zone saisie</span><span class="zchip">Cou</span></p>
<p class="zone-effet"><span class="zlbl">Effet</span>Tant que la prise est maintenue, l'adversaire subit l'état Mutisme partiel (voir États).</p>
</div>
<div class="zone">
<p class="zone-chips"><span class="zlbl">Zone saisie</span><span class="zchip">Poignet</span><span class="zchip">Main</span><span class="zchip">Doigt</span></p>
<p class="zone-effet"><span class="zlbl">Effet</span>L'adversaire lâche ce qu'il tenait.</p>
</div>
</div>

Si le personnage est capable d'utiliser plusieurs manœuvres dans une même attaque, dont Maîtriser et Soumettre, il peut les employer en même temps : il n'a donc pas besoin d'avoir la cible Maîtrisée pour utiliser Soumettre. Il n'effectue alors qu'un seul jet de lutte, valable pour toutes ces manœuvres : en cas de réussite, leurs effets s'appliquent tous et la cible atteint directement le cran le plus élevé employé.
</div>

<div class="mcard" markdown>
**Soumettre** <span class="prereq">Prérequis : cible Maîtrisée par le personnage</span> Le personnage fait le jet d'attaque opposé au jet de défense de l'adversaire avec un malus de −40 ; sur une touche, le personnage fait un jet de lutte opposé au jet de lutte ou de contorsion de la cible qu'il tient, avec un bonus égal à la moitié du degré de touche, jusqu'à un maximum de +100. En cas de réussite, la cible passe de Maîtrisée à Soumise (voir États).

Tant qu'il maintient la prise, le personnage subit lui aussi une Paralysie totale et ne peut pas utiliser pour une attaque l'arme qui tient la prise ni le membre qui la porte. Il peut lâcher la prise à tout moment (aucune action requise).

Le personnage peut tenir plusieurs prises en même temps, sur plusieurs adversaires ou sur plusieurs zones d'un même adversaire. Un adversaire tenu à plusieurs zones subit les effets de chaque zone.

Le personnage peut décider de ne pas faire de jet d'attaque, car il tient déjà son adversaire : on considère que le degré de touche vaut 0 % (donc sans aucun bonus) et qu'il ne peut être augmenté d'aucune manière (ce qui inclut Éraflure). Il fait alors directement son jet d'opposition de lutte sans le bonus.

L'adversaire peut se libérer en prenant une action : le personnage fait un nouveau jet de lutte opposé au jet de lutte ou de contorsion de l'adversaire. Si l'adversaire l'emporte, il redevient seulement Maîtrisé.

Si la prise visait une partie précise du corps (Agripper avec l'option Viser), ses effets persistent : le personnage tient déjà la cible et n'a pas besoin de Viser à nouveau. Il peut en revanche Viser une autre zone : son jet d'attaque subit alors le malus de cette zone et, si la manœuvre réussit, la prise se déplace sur la nouvelle zone, dont les effets remplacent les précédents. Certaines parties donnent en plus un effet supplémentaire :

<div class="zones">
<div class="zone">
<p class="zone-chips"><span class="zlbl">Zone saisie</span><span class="zchip">Cou</span></p>
<p class="zone-effet"><span class="zlbl">Effet</span>Tant que la prise est maintenue, l'adversaire subit l'état Mutisme total (voir États) et commence à suffoquer.</p>
</div>
</div>
</div>

<div class="mcard" markdown>
**Désarmer** <span class="prereq">Prérequis : Viser une partie du corps qui tient un objet</span> Le personnage fait le jet d'attaque opposé au jet de défense de l'adversaire avec un malus de −20, augmenté par le malus de Viser d'une des parties du corps qui tiennent l'objet : soit −60 en tout pour un objet tenu en main (Main, −40) ; sur une touche, le personnage fait un jet de lutte opposé au jet de lutte de l'adversaire ou de la compétence de l'arme tenue (si l'objet est une arme), avec un bonus égal à la moitié du degré de touche, jusqu'à un maximum de +100. Un objet tenu à plusieurs mains donne +20 au jet de l'adversaire. En cas de réussite, la cible lâche l'objet, qui tombe par terre.

Le personnage peut décider de prendre l'objet au lieu de le laisser tomber : dans ce cas, il subit un malus de −40 à son jet de lutte. Il doit l'annoncer avant de lancer le jet de lutte.
</div>

<div class="mcard" markdown>
**Mettre à terre** <span class="prereq">Prérequis : aucun</span> Le personnage fait le jet d'attaque opposé au jet de défense de l'adversaire avec un malus de −40 ; sur une touche, le personnage fait un jet de lutte opposé au jet de lutte ou d'équilibre de l'adversaire, avec un bonus égal à la moitié du degré de touche, jusqu'à un maximum de +100. En cas de réussite, la cible tombe À terre (voir États).
</div>

<div class="mcard" markdown>
**Pousser** <span class="prereq">Prérequis : aucun</span> Le personnage fait le jet d'attaque opposé au jet de défense de l'adversaire avec un malus de −40 ; sur une touche, le personnage fait un jet de lutte opposé au jet de lutte ou d'équilibre de l'adversaire, avec un bonus égal à la moitié du degré de touche, jusqu'à un maximum de +100. En cas de réussite, la cible est repoussée en ligne droite, sur une distance donnée par la Force du personnage (table ci-dessous). Pour pousser son adversaire, le personnage doit avoir assez de Force pour le porter (voir Port) ; à 0 de Force, l'adversaire n'est pas poussé.

Si l'adversaire est arrêté par un obstacle au cours de sa poussée, il subit les dégâts d'impact indiqués dans la table, à la Force du personnage. Il peut les amortir par un jet de Chute (voir Capacités physiques), dont le résultat se retranche des dégâts.

| Force | Distance | Dégâts |
|:---:|:---:|:---:|
| 1 | 0.1 m | 0 |
| 2 | 0.2 m | 0 |
| 3 | 0.3 m | 0 |
| 4 | 0.5 m | 0 |
| 5 | 1 m | 0 |
| 6 | 2 m | 0 |
| 7 | 3 m | 10 |
| 8 | 5 m | 20 |
| 9 | 7 m | 30 |
| 10 | 10 m | 40 |
| 11 | 20 m | 70 |
| 12 | 30 m | 100 |
| 13 | 50 m | 160 |
| 14 | 70 m | 210 |
| 15 | 100 m | 280 |
| 16 | 200 m | 400 |
| 17 | 300 m | 450 |
| 18 | 500 m | 500 |
| 19 | 700 m | 580 |
| 20 | 1 km | 650 |
| 21 | 2 km | 710 |
| 22 | 3 km | 760 |
| 23 | 5 km | 810 |
| 24 | 7 km | 850 |
| 25 | 10 km | 890 |
| 26 | 20 km | 920 |
| 27 | 30 km | 950 |
| 28 | 50 km | 970 |
| 29 | 70 km | 990 |
| 30 | 100 km | 1000 |

Un personnage ne peut pas utiliser la manœuvre Pousser en s'attaquant lui-même.
</div>

<div class="mcard" markdown>
**Toucher** <span class="prereq">Prérequis : aucun</span> Le personnage cherche à poser la main sur sa cible sans le moindre geste hostile. Il ne lance pas les dés : il fixe lui-même son résultat final, de 0 à sa valeur d'attaque, modificateurs de l'action compris. Ce résultat s'oppose au résultat final de la défense de la cible ; s'il lui est supérieur ou égal, le contact est établi, sans infliger aucun dégât. Sur une touche, on considère que le degré de touche vaut 0 % (donc sans aucun bonus) et qu'il ne peut être augmenté d'aucune manière (ce qui inclut Éraflure). Toucher coûte une action, mais ne compte pas dans la limite d'une attaque par round : le personnage peut Toucher sans renoncer à son attaque du round.
</div>

### Viser

Viser est une option d'attaque : le personnage la choisit en composant son attaque, en plus de sa manœuvre (voir Attaque). Il vise une zone du corps de l'adversaire, listée dans le tableau ci-dessous, et son jet d'attaque subit le malus de la zone visée. L'effet exact d'un coup visé figure dans chaque manœuvre.

<table>
<thead><tr><th>Partie du corps</th><th>Malus à l'attaque</th></tr></thead>
<tbody>
<tr><td>Œil</td><td>−100</td></tr>
<tr><td>Tête</td><td>−60</td></tr>
<tr><td>Oreille</td><td>−70</td></tr>
<tr><td>Nez</td><td>−70</td></tr>
<tr><td>Bouche</td><td>−60</td></tr>
<tr><td>Cou</td><td>−80</td></tr>
<tr><td>Épaule</td><td>−30</td></tr>
<tr><td>Cœur</td><td>−60</td></tr>
<tr><td>Poumon</td><td>−50</td></tr>
<tr><td>Bras</td><td>−20</td></tr>
<tr><td>Torse</td><td>−10</td></tr>
<tr><td>Coude</td><td>−60</td></tr>
<tr><td>Foie</td><td>−50</td></tr>
<tr><td>Estomac</td><td>−40</td></tr>
<tr><td>Avant-bras</td><td>−20</td></tr>
<tr><td>Abdomen</td><td>−20</td></tr>
<tr><td>Poignet</td><td>−40</td></tr>
<tr><td>Hanche</td><td>−30</td></tr>
<tr><td>Aine</td><td>−60</td></tr>
<tr><td>Vulve</td><td>−80</td></tr>
<tr><td>Testicules</td><td>−70</td></tr>
<tr><td>Main</td><td>−40</td></tr>
<tr><td>Doigt</td><td>−90</td></tr>
<tr><td>Cuisse</td><td>−20</td></tr>
<tr><td>Genou</td><td>−40</td></tr>
<tr><td>Mollet</td><td>−10</td></tr>
<tr><td>Cheville</td><td>−50</td></tr>
<tr><td>Pied</td><td>−50</td></tr>
</tbody>
</table>

### Attaquer en retard

Attaquer en retard est une option d'attaque : le personnage la choisit en composant son attaque, en plus de sa manœuvre (voir Attaque). Au lieu de frapper l'adversaire là où il se tient, il vise une des positions que l'adversaire a occupées depuis la fin du tour précédent du personnage. Son jet d'attaque subit un malus de −80, et l'attaque se résout comme si la cible se trouvait encore à la position choisie : distance, couvert et ligne de vue se lisent à ce moment passé, et non à l'instant présent.

Attaquer en retard n'altère pas ce qui s'est déjà passé : l'attaque s'ajoute aux événements, elle ne les réécrit pas. Si son emploi crée une incohérence, le MJ détermine exactement comment la situation se déroule.

Elle sert à cueillir qui se dérobe sitôt après avoir frappé, l'adversaire qui surgit, porte son coup et se replie hors de portée, ou qui se montre puis se terre derrière un couvert. Le personnage le rattrape à la position exposée qu'il vient de quitter, au prix d'un coup bien plus incertain.

### Défense

Une défense est la réaction (voir Déroulement du combat) par laquelle un personnage cherche à éviter ou à détourner une attaque qui le vise. Évidemment, il ne peut se défendre qu'une seule fois par attaque.

Avant de lancer les dés, le personnage compose sa défense, en connaissant le résultat final du jet d'attaque ainsi que les options et la manœuvre de l'attaque. Il choisit d'abord la compétence avec laquelle il se défend : l'Esquive, ou la Parade s'il porte une arme dotée de la propriété Parade sur un membre disponible. Cette compétence fixe le jet de défense.

Il sélectionne ensuite la manœuvre que suit sa défense ; elle est toujours choisie.

Après avoir annoncé sa manœuvre, le personnage fait son jet de défense et calcule son résultat final ; on le compare au résultat final de l'attaque pour savoir si elle touche (voir Attaque).

Certaines attaques ne peuvent pas être esquivées, d'autres ne peuvent pas être parées. Le MJ, ou le joueur qui porte l'attaque, doit l'annoncer avant que le défenseur ne compose sa défense.

### Manœuvres de défense

<div class="mcard" markdown>
**Se protéger** <span class="prereq">Prérequis : aucun</span> Le personnage fait son jet de défense, sans modificateur ni effet particulier.

Se protéger est la manœuvre par défaut : si un personnage se défend sans préciser la manœuvre qu'il utilise, alors on considère qu'il utilise Se protéger.
</div>

<div class="mcard" markdown>
**Se laisser toucher** <span class="prereq">Prérequis : aucun</span> Le personnage renonce à se défendre et laisse le coup l'atteindre. Il ne lance pas les dés : son résultat final de défense vaut 0, si bien que toute attaque dont le résultat final atteint 0 ou plus le touche d'office.
</div>

<div class="mcard" markdown>
**Encaisser** <span class="prereq">Prérequis : aucun</span> Le personnage renonce à se dérober et se ramasse pour absorber le coup. Il fait son jet de défense avec un malus de −80 ; en échange, le degré de touche de l'attaque est plafonné à 100 %, aussi large que soit l'écart entre les résultats finaux.
</div>

<div class="mcard" markdown>
**Contre-attaquer** <span class="prereq">Prérequis : avoir une contre-attaque préparée</span> Le personnage oppose à l'assaillant le coup qu'il retenait. Il fait son jet de défense avec un malus de −40. Si son résultat final est supérieur à celui de l'attaque, il riposte aussitôt : il porte une attaque ordinaire contre l'assaillant, en réaction. La riposte gagne au jet d'attaque un bonus égal à la moitié de l'écart entre les résultats finaux de la défense et de l'attaque parée, jusqu'à un maximum de +100.

La riposte est une attaque à part entière et en suit toutes les règles : l'assaillant s'en défend normalement, et peut donc la contre-attaquer s'il a lui-même une contre-attaque préparée.

Prendre cette manœuvre consomme une contre-attaque préparée, que la défense réussisse ou non.
</div>

### Contre-attaque

À son tour, le personnage peut préparer une contre-attaque. Pour ce faire, il consomme une action qui compte comme une action d'attaque, ce qui lui permet d'effectuer la manœuvre de défense Contre-attaquer une fois. La contre-attaque reste préparée jusqu'au début de son prochain tour.

S'il est capable d'effectuer plusieurs actions d'attaque, il peut alors préparer plusieurs contre-attaques (en prenant une action pour chaque contre-attaque), ce qui lui permet d'effectuer un nombre de manœuvres de défense Contre-attaquer égal au nombre de contre-attaques préparées.

### Défense d'autrui

Défendre autrui est une réaction : le personnage peut la prendre quand une attaque vise non pas lui, mais un de ses alliés.

S'il défend avec la Parade, le personnage s'interpose : il faut que son mouvement lui permette de se déplacer jusqu'à la trajectoire de l'attaque.

S'il défend avec l'Esquive, le personnage pousse son allié hors de la trajectoire : il faut que son mouvement lui permette de se déplacer jusqu'à son allié et de le déplacer hors de l'attaque, et qu'il ait assez de Force pour porter son allié (voir Port).

Dans les deux cas, le personnage se défend contre cette attaque comme s'il en était la cible (voir Défense), avec un malus de −40 à son jet de défense. Si son résultat final est supérieur au résultat final de l'attaque, l'attaque manque : l'allié n'est pas touché. S'il rate sa défense, le personnage la rate sans conséquence pour lui, l'attaque se poursuit alors contre l'allié.

Cette réaction se déclare après le jet d'attaque de l'adversaire, mais avant la défense de l'allié. Si plusieurs personnages défendent un allié contre une même attaque, leurs défenses se résolvent dans l'ordre d'intervention ; dès que l'une l'emporte, l'attaque manque et la résolution s'arrête.

</div>