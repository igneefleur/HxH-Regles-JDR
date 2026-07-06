# Refonte du Nen : un système de capacités modulaire

> Document de travail. Il pose l'architecture de la création de capacités, sans
> aucune valeur : pas de DI, pas de DR/DE/DT/DM/DC, pas d'UA, pas de maintien,
> pas de caractéristique, pas de pourcentage. On ne fixe ici que la grammaire :
> ce qu'est une capacité, comment elle s'assemble, comment plusieurs capacités
> forment un pouvoir. Les pourcentages et valeurs cités plus bas (+10 %, +20 %, ou
> un bonus qui passe de +30 à +36) ne sont que des exemples d'illustration du
> fonctionnement, jamais un barème. Les chiffres viendront
> ensuite et se brancheront sur la grille déjà éprouvée en renforcement, émission
> et conjuration. Seul le banc d'essai, tout en bas, porte des valeurs concrètes,
> pour vérifier que le modèle tient bout à bout.

<div class="cols" markdown>

### Intention

Le Nen se construit comme une baguette de *Noita* : on part d'un socle, on
empile des modules par-dessus, et la combinaison décide de ce que le pouvoir
fait réellement. Les modules sont les sorts. Une bonne capacité n'est pas une
ligne de catalogue figée, mais un assemblage que le joueur compose brique par
brique.

L'objectif est qu'avec ce seul jeu de briques on puisse reconstruire environ
90 % des pouvoirs de l'œuvre, la spécialisation mise à part (elle reste, par
nature, l'exception qui échappe aux règles communes).

On garde l'acquis (les modules déjà écrits en renforcement, émission et
conjuration), mais on le réorganise autour de quatre idées :

- la séparation nette entre le type d'une capacité et la catégorie de chaque
  module ;
- un modificateur d'affinité d'emploi porté à la fois par la capacité et par
  chaque module ;
- des conditions qui s'attachent à une capacité ou à un module et décalent ce
  modificateur ;
- le raccord explicite des capacités entre elles.

---

### 1. Vocabulaire

Trois mots, du plus large au plus fin.

- Pouvoir : le Hatsu d'un personnage, son nom propre (Janjanken, Bungee Gum,
  Crazy Slot). C'est ce que le monde voit et nomme. Un pouvoir se compose d'une
  ou plusieurs capacités.
- Capacité : l'unité que l'on assemble, un effet de Nen atomique, une baguette
  complète. « Pierre », « Feuille », « Ciseaux » et « Pierre Feuille Ciseaux »
  sont quatre capacités distinctes du même pouvoir.
- Module : la brique, le sort. Le plus petit élément. On empile des modules sur
  une capacité pour la façonner.

Un pouvoir est donc un ensemble de capacités raccordées entre elles ; une capacité
est un socle plus une pile de modules, dotée d'une durée, d'un modificateur
d'affinité d'emploi et, parfois, de conditions.

---

### 2. Les deux axes : type et catégorie

C'est le pivot de la refonte : on cesse de confondre deux choses qui n'en sont
pas une.

#### Le type : le rôle mécanique de la capacité

Le type dit ce que la capacité fait, mécaniquement. Il y en a trois, et toute
capacité en porte exactement un.

| Type | Ce qu'il fait |
|---|---|
| Attaque | elle frappe, elle blesse |
| Défense | elle protège, elle pare, elle entrave |
| Effet | tout le reste : amplification, déplacement, perception, altération, utilitaire |

Le type appelle ses modules naturels sans interdire les autres : une attaque
attire les modules offensifs, une défense les défensifs, mais rien n'empêche de
greffer un module d'une autre famille si l'assemblage le demande, à condition
que le module accepte ce type.

> Types spéciaux reportés. La conjuration de réceptacle (créature, objet) et
> l'effet conjuré sont des types spéciaux, mis de côté pour cette passe et
> traités plus tard. Ils ne figurent pas dans la liste des types tant qu'ils ne
> sont pas réintroduits. Attention : seul le type conjuration est retiré ; la
> catégorie conjuration reste l'une des six écoles de module, et la persistance
> d'immobilisation de l'aura propre à la conjuration n'est pas abrogée, elle
> attend simplement la réintroduction du type.

#### La catégorie : l'école de chaque module

Les six catégories de Nen (renforcement, émission, transmutation, manipulation,
conjuration, spécialisation) ne sont pas des types. Ce sont les écoles auxquelles
appartiennent les modules. Chaque module relève d'une seule catégorie, qui dit
de quelle nature de Nen il procède (un module purement structurel n'en a aucune) :

- amplifier une aptitude existante relève du renforcement ;
- projeter l'aura loin du corps relève de l'émission ;
- prêter à l'aura une propriété de matière relève de la transmutation ;
- soumettre un être ou un objet relève de la manipulation ;
- donner à l'aura une existence matérielle relève de la conjuration ;
- ce qui n'entre nulle part ailleurs relève de la spécialisation.

Ces deux axes sont orthogonaux. Une seule capacité de type attaque peut empiler
un module de dégâts (renforcement), un module tranchant (transmutation) et un
module de portée (émission) : un coup tranchant porté à distance. C'est exactement
la logique de *Noita*, où le rôle d'un sort est une chose, et son élément une
autre.

La catégorie portée par chaque module est le crochet qui rebranche l'[affinité](archetypes-nen.md)
du personnage : c'est elle qui dira plus tard le coût de conception et la
puissance d'un module, selon que le porteur est ou non dans son école. Un
renforceur convertira son [développement intérieur](di.md) en modules de
renforcement à plein rendement, et en modules de conjuration à perte.

---

### 3. Anatomie d'une capacité

On assemble une capacité en posant, dans l'ordre :

1. le type (le socle) ;
2. les modules (les sorts empilés), chacun avec ses attributs ;
3. la durée (instantané ou à maintien) ;
4. le modificateur d'affinité d'emploi global de la capacité ;
5. les conditions (facultatives), au niveau de la capacité ou d'un module.

On notera une capacité ainsi, sans aucun chiffre à ce stade :

```
Capacité : <nom>
Type        : <attaque | défense | effet>
Durée       : <instantané | à maintien>
Modificateur d'emploi (global) : <neutre par défaut>
Modules     :
  - <module> (<catégorie(s)>)        [modificateur local éventuel]
  - <module> (<catégorie(s)>)
Conditions  :
  - <énoncé>  (<décalage du modificateur, ex. +10 %>)   au niveau capacité
Raccord     : <déclencheur | lien | charge utile>       (facultatif)
```

#### 3.1 Le type (le socle)

Le socle fixe la forme de la capacité avant tout module.

- Attaque : la capacité vise et frappe. Par défaut au contact ; un module de
  portée la déporte. Elle se résout par un jet d'attaque, opposé à la défense de
  la cible.
- Défense : la capacité garde, encaisse ou entrave. Elle alimente une parade, une
  esquive, une réduction de dégâts, une barrière.
- Effet : la capacité fait autre chose que frapper ou parer. Elle amplifie,
  déplace, perçoit, altère, communique. C'est le socle le plus ouvert.

#### 3.2 La fiche de module (les sorts)

Un module ajoute une propriété à la capacité. C'est la matière du jeu. On en
empile autant qu'on veut, en suivant l'orientation du type mais sans s'y
enchaîner. Chaque module se lit sur une fiche aux attributs fixes, toujours dans
le même ordre :

```
Nom du module
-------------
Catégorie         : <une seule école, ou aucune>
Types compatibles : <sous-ensemble de attaque / défense / effet>
Affinité          : <+00% / +20% / −30% ; VAR. si elle dépend d'un choix>

Description : <ce que fait le module>

Paliers (on en retient une ligne par grille) :
  | Effet | UA | Maintien | Conception (DR / DE / DT / DM / DC) | Carac |
  |  ...  | .. |   ...    |                 ...                 |  ...  |
  Grilles annexes combinables s'il y a lieu (par exemple le Catalogue).
```

Les attributs se rangent en deux registres :

- L'en-tête porte ce qui ne change pas d'un palier de puissance à l'autre : la ou
  les catégories, les types compatibles, la caractéristique requise, le
  modificateur d'affinité d'emploi du module.
- Les paliers chiffrés portent ce qui monte avec la puissance : l'effet, le coût
  de conception, l'UA, le maintien. Ils se liront, le moment venu, sur la même
  grille que les modules existants ; ici on ne nomme que les colonnes.

Un module compte presque toujours plusieurs paliers : une suite de lignes de
puissance croissante (par exemple +10, +25, +40 à l'attaque), dont on retient une
seule à la conception. Certains modules s'étendent sur plusieurs tableaux, dont
les choix se combinent : le Catalogue de la conjuration, par exemple, fixe à part
sa contenance, son extraction simultanée et sa qualité. Une fiche peut donc porter
plusieurs grilles, et l'on en retient une ligne par grille, sauf mention de cumul.

Les types compatibles sont une vraie contrainte : un module de bonus à l'attaque
n'accepte que le type attaque, et n'a aucun sens sur un effet. Chaque module dit
donc à quels types il peut se greffer.

Une catégorie peut aussi manquer. Un module purement structurel, comme un module
de raccord, n'appartient à aucune école : il ne se convertit pas en points de
catégorie mais se paie directement en DI, et aucune affinité ne le concerne.

#### 3.3 Un module, une catégorie

Chaque module relève d'une seule catégorie, ou d'aucune s'il est purement
structurel (un module de raccord). C'est plus simple, et cela permet de ranger et
de trier les modules par école.

Un même concept peut toutefois exister dans plusieurs catégories : il y figure
alors comme autant d'entrées distinctes, une par école, chacune avec ses propres
coûts. Une attaque qui poursuit sa cible, par exemple, peut se décliner en une
version d'émission et une version de manipulation, rangées chacune sous sa
catégorie. L'affinité se lit toujours sur l'unique catégorie de l'entrée employée.

#### 3.4 La durée

La durée règle l'existence de la capacité dans le temps. Deux régimes
fondamentaux.

- Instantané : la capacité se déclenche, se résout, disparaît. Un coup, un trait,
  un déplacement (les trois finisseurs du Janken).
- À maintien : la capacité persiste tant que le personnage la soutient, en payant
  son maintien chaque round (la posture « Pierre Feuille Ciseaux »).

Un troisième régime existe pour la conjuration, qui ne se paie pas round par
round : une chose conjurée demeure tant qu'elle n'est pas congédiée ou détruite,
en immobilisant son UA sur l'aura maximale (UAM) plutôt qu'en réclamant un
maintien. On la dira persistante, et l'attribut maintien d'un tel module est sans
objet. Ce régime attend la réintroduction du type conjuration.

#### 3.5 Le modificateur d'affinité d'emploi

C'est la nouveauté centrale, et il faut la distinguer de l'affinité existante
pour éviter toute confusion.

L'[affinité d'emploi](archetypes-nen.md) (AE) est déjà définie : un pourcentage
propre au personnage, par catégorie, fixé par son archétype (sa catégorie au plus
haut, les voisines en dessous, l'opposée au plus bas). Elle gouverne la puissance
du Nen quand il emploie cette catégorie. C'est l'assise.

Le modificateur d'affinité d'emploi ne crée pas une affinité nouvelle : il
décale l'affinité d'emploi que l'archétype donne déjà à la catégorie
concernée, vers le haut ou vers le bas. Il existe à deux rangs :

- global, porté par la capacité, il vaut pour tous ses modules ;
- local, porté par chaque module, il ne vaut que pour lui.

Deux bornes de périmètre, pour ne pas déborder sur le reste du système :

- le modificateur touche la seule affinité d'emploi (la puissance), jamais
  l'affinité d'apprentissage, ou AA (la vitesse de progression) ;
- il porte sur la puissance de l'effet, dont il multiplie la valeur, et non sur les
  coûts d'UA ou de conception, qui restent gouvernés par la grille de chiffrage.

L'affinité ne multiplie que les effets chiffrés (un bonus, des dégâts, un seuil).
Un effet descriptif, comme un déclencheur, une faculté ou un nombre de capacités,
n'en est pas multiplié, même si le module porte tout de même une valeur d'affinité ;
chaque fiche dit lequel des deux effets elle produit.

#### 3.6 Les conditions

Une condition est un attribut facultatif qui s'attache soit à une capacité, soit à
un module précis. Cet ancrage est sa donnée structurante. Elle porte deux choses,
tenues séparées :

- son énoncé : la restriction, le serment, le déclencheur (« seulement contre tel
  ennemi », « seulement après l'avoir annoncé à voix haute », « au prix d'une
  sanction en cas de triche ») ;
- son effet de règle : un décalage du modificateur d'affinité d'emploi,
  exprimé en pourcentage signé.

Plus la condition est lourde, plus le décalage lui est favorable : dans l'œuvre,
une capacité que son porteur s'interdit d'employer sauf cas précis frappe d'autant
plus fort. C'est un levier de puissance, pas un coût.

L'effet est strictement localisé au niveau d'attache :

- une condition posée sur la capacité décale le modificateur global, donc se
  répercute sur tous ses modules ;
- une condition posée sur un module ne décale que le modificateur de ce module.

On peut cumuler plusieurs conditions au même niveau ; leurs décalages s'ajoutent
en points de pourcentage sur le modificateur de ce niveau, comme l'expose la
composition plus bas.

Les conditions recouvrent deux familles, souvent combinées :

- le raccord (déclencheur, lien, charge utile), qui connecte les capacités entre
  elles, détaillé en partie 4 ;
- le serment et la restriction, qui bornent l'emploi.

Toutes deux sont des conditions au sens de cette règle ; reste à trancher si une
condition de pur raccord décale elle aussi le modificateur, ou si seul le serment
le fait.

#### 3.7 La composition, module par module

L'affinité d'emploi effective se lit module par module, jamais pour la
capacité en bloc : chaque module peut relever d'une autre catégorie et porter son
propre modificateur. Pour un module donné, on empile, du plus large au plus fin :

1. la base : l'affinité d'emploi d'archétype du personnage dans la catégorie
   de ce module ;
2. le modificateur global de la capacité (partagé par tous les modules) ;
3. le modificateur local du module (propre à lui) ;
4. les décalages des conditions, chacune à son niveau (les conditions de capacité
   valent pour tous les modules, celles du module ne valent que pour lui).

Les décalages des niveaux 2 à 4 s'ajoutent en points de pourcentage à la base du
niveau 1 : leur somme donne l'affinité d'emploi effective du module, exprimée
en pourcentage (100 % pour une catégorie tenue à son sommet). Cette affinité
multiplie alors la valeur de l'effet du module. Ainsi un module de +30 à l'attaque,
employé par un renforceur dont l'affinité effective atteint 120 % (100 % d'archétype,
plus 20 % de modificateur), donne +36 au lieu de +30 ; une affinité sous 100 %
réduit d'autant, et un modificateur négatif peut faire descendre l'effet plus bas
encore. Deux invariants de structure : ce qui est posé au niveau capacité se
répercute identiquement sur tous ses modules ; ce qui est posé au niveau module ne
touche que lui. Le total des décalages (les niveaux 2 à 4 : modificateur global de
la capacité, modificateur du module et conditions) ne dépasse jamais +100 % : des
bonus peuvent le porter au-delà, mais on n'en applique jamais plus de +100 %, et
cela vaut pour n'importe quel module.

---

### 4. Composer un pouvoir : le raccord

Un pouvoir est un graphe de capacités reliées par leur raccord. On le lit comme un
petit circuit : des capacités « source » qui s'activent d'elles-mêmes, des
capacités « finisseur » qui n'existent que déclenchées.

#### Les déclencheurs

Le raccord se décline en quelques formes, qu'on combine librement.

- Immédiat : la capacité part dès qu'on y consacre l'action. Régime par défaut
  d'un instantané.
- À l'impact : la capacité ne se libère qu'au contact de ce qu'elle touche.
- À retardement : la capacité part après un délai (une minuterie, un compte à
  rebours).
- Conditionnel : la capacité part quand une condition énoncée devient vraie (la
  cible prononce un mot, une créature meurt, un seuil de points de vie est
  franchi).
- Lié : la capacité ne peut partir que pendant qu'une autre capacité du même
  pouvoir est active. C'est le lien du Janken : les trois finisseurs exigent la
  posture.
- Charge utile : une capacité en transporte une autre et la délivre là où elle
  aboutit (un trait émis qui, au point d'arrivée, conjure une bête ; une flèche
  conjurée qui, à l'impact, pose une emprise de manipulation).

#### Modules à capacité imbriquée

Certains modules ne portent pas un effet chiffré, mais une ou plusieurs autres
capacités, bâties à part avec leur propre type, leurs modules, leur durée et leurs
conditions. Le module dit seulement quand et comment cette capacité interne entre
en jeu. Le système devient ainsi récursif : une capacité peut en contenir d'autres,
et de là viennent les pouvoirs les plus riches.

- Add Trigger : sur un déclencheur donné (impact, minuterie, condition, mot-clé),
  le module active la capacité interne qu'il porte. C'est le branchement de base
  d'un sort à déclencheur.
- Charge utile : variante où la capacité interne est délivrée à l'aboutissement
  d'une attaque ou d'une émission, au point d'impact ou d'arrivée du trait.
- Catalogue : le module tient un répertoire de plusieurs capacités internes, dont
  il tire l'une ou l'autre au moment voulu, et règle combien existent à la fois.
  Ces capacités cataloguées se bâtissent à part et sans elles le Catalogue n'a rien
  à invoquer.

Une capacité imbriquée garde ses propres coûts et sa propre affinité : elle se
résout comme n'importe quelle capacité, le module conteneur n'ajoutant que de quoi
la tenir prête ou la déclencher.

Le raccord peut s'emboîter : une capacité déclenchée par un Ajouter un Déclencheur
peut elle-même en porter un, de sorte que les déclencheurs s'enchaînent. Le
Catalogue, lui, ne s'emboîte pas : une capacité cataloguée ne renferme pas de
Catalogue.

#### Exemple de circuit : le Janken

Le pouvoir de Gon se lit en quatre capacités : une source à maintien, trois
finisseurs liés. On y montre, sans chiffre, un modificateur global et une
condition (le décalage indiqué n'est qu'un exemple d'illustration).

```
Pouvoir : Janjanken

Capacité : Pierre Feuille Ciseaux       (la posture, source)
Type        : effet
Durée       : à maintien
Modificateur d'emploi (global) : neutre
Modules     :
  - bonus de caractéristique (renforcement)
Conditions  :
  - n'arme les finisseurs qu'une fois la posture annoncée  (ex. +10 %)

Capacité : Pierre                       (finisseur)
Type        : attaque
Durée       : instantané
Modules     :
  - bonus de dégâts (renforcement)
Raccord     : lié, exige la posture Pierre Feuille Ciseaux

Capacité : Feuille                      (finisseur)
Type        : attaque
Durée       : instantané
Modules     :
  - portée / attaque à distance (émission)
Raccord     : lié, exige la posture Pierre Feuille Ciseaux

Capacité : Ciseaux                      (finisseur)
Type        : attaque
Durée       : instantané
Modules     :
  - bonus d'attaque (renforcement)
Raccord     : lié, exige la posture Pierre Feuille Ciseaux
```

On voit le circuit : la posture ne frappe pas, elle prépare. Les finisseurs ne
sont rien sans elle. Trois écoles cohabitent dans un même pouvoir (renforcement
pour Pierre et Ciseaux, émission pour Feuille), ce que les deux axes rendent
naturel : chaque finisseur se résout sur l'affinité de la catégorie de ses
modules.

---

### 5. La bibliothèque de modules

Une seule bibliothèque, rangée par catégorie (l'école), où chaque module est un
sort que l'on greffe sur les types compatibles. Aucun chiffre ici : seulement le
nom, l'effet en une ligne, et les types acceptés (parmi attaque, défense, effet).
Les six attributs chiffrables de chaque fiche (UA, maintien, conception,
caractéristique, modificateur) se brancheront ensuite.

> Les catégories marquées *(esquisse)* n'avaient pas encore de modules ; ce qui
> suit en pose le squelette, à développer.

#### 5.1 Renforcement : amplifier l'existant

| Module | Effet | Types |
|---|---|---|
| Attaque | bonus à une attaque | attaque |
| Attaque complète | bonus à toutes les attaques du round | attaque |
| Dégâts | bonus aux dégâts infligés | attaque |
| Attaques supplémentaires | attaques en plus dans le tour | attaque |
| Parade | bonus aux parades | défense |
| Esquive | bonus aux esquives | défense |
| Parade complète / Esquive complète | bonus à toutes les parades / esquives | défense |
| Réduction de dégâts | encaisse une part des dégâts subis | défense |
| Caractéristique | bonus à une caractéristique | effet |
| Compétence | bonus à une compétence | effet |
| Initiative | bonus à l'initiative | effet |
| Critique | bonus à la marge de critique | attaque |
| Actions supplémentaires | actions en plus dans le tour | effet |
| Guérison de soi | regagne des points de vie dans la durée | effet |

#### 5.2 Émission : projeter et porter au loin

| Module | Effet | Types |
|---|---|---|
| Distance | la capacité agit jusqu'à une portée donnée | attaque, défense, effet |
| Zone | la capacité touche un rayon entier | attaque, défense |
| Guidage / Poursuite | l'aura corrige sa course vers la cible | attaque |
| Téléportation | déplace le porteur d'un point à un autre | effet |
| Lien / antenne | l'aura déportée reste reliée au porteur | effet |
| Retour | l'aura émise revient à son point de départ | attaque, effet |
| Persistance déportée | l'aura tient loin du corps sans se dissiper | attaque, défense, effet |

#### 5.3 Transmutation : prêter une propriété de matière *(esquisse)*

L'aura prend les qualités d'une substance sans en devenir la matière réelle : une
aura électrique garde la nature de l'aura et n'agit pas tout à fait comme une
vraie décharge. Chaque propriété ajoute un effet annexe.

| Module | Effet | Types |
|---|---|---|
| Tranchant | l'aura coupe ; dégâts de type tranchant | attaque, défense |
| Contondant | l'aura durcit ; dégâts contondants, brise les gardes | attaque, défense |
| Perforant | l'aura transperce ; ignore une part de la réduction de dégâts | attaque |
| Élastique | l'aura rebondit et s'étire ; renvoi, traction, élan | attaque, défense, effet |
| Adhésif | l'aura colle ; fixe, retient, accroche une cible | attaque, défense, effet |
| Électrique | l'aura imite la décharge ; secoue, paralyse, se propage | attaque |
| Thermique | l'aura imite le feu ou le froid ; brûle, gèle | attaque |
| Corrosif | l'aura ronge ou empoisonne dans la durée | attaque |
| Fluide | l'aura coule comme un liquide ; s'infiltre, enveloppe | défense, effet |
| Volatil | l'aura se répand comme un gaz ; nappe, voile | défense, effet |
| Texture | l'aura imite l'aspect et le toucher d'une autre matière | effet |

#### 5.4 Manipulation : soumettre êtres et objets *(esquisse)*

La prise se paie presque toujours d'une condition fixée d'avance : plus elle est
contraignante, plus l'emprise est forte. Elle se résout par un jet opposé.

| Module | Effet | Types |
|---|---|---|
| Emprise | prend le contrôle d'un être ou d'un objet | effet |
| Ordre | impose un ordre que la cible exécute | effet |
| Marquage | appose une marque qui suit la cible et sert d'ancre | attaque, effet |
| Marionnette | dirige une cible comme un pantin | effet |
| Antenne / vecteur | la prise passe par un contact ou un objet posé | attaque, effet |
| Altération | modifie perception, mémoire ou émotion de la cible | effet |
| Asservissement par condition | l'emprise se scelle par une règle, un contact, un rituel | effet |
| Portée du contrôle | nombre de cibles, distance et durée de l'emprise | effet |

#### 5.5 Conjuration : donner corps à l'aura

Les modules de conjuration (forme, taille, autonomie, armes naturelles, vol,
régénération, barrière de dégâts, stockage, catalogue, capacité innée, etc.)
existent déjà et restent valides comme catégorie. Mais ils ne valent que sur un
réceptacle conjuré, et le type conjuration est reporté, comme l'énonce la note de
la partie 2. Cette catégorie attend donc la réintroduction de son type ; on la
laisse en l'état, sans la rebrancher pour l'instant sur les trois types
ordinaires.

#### 5.6 Spécialisation : hors catégorie

Par définition, la spécialisation n'a pas de modules communs : ses effets sont
uniques et propres à chacun. Elle reste hors de la bibliothèque et hors du
périmètre des 90 %. On la mentionne pour mémoire, pas pour la cataloguer.

#### 5.7 Modules de raccord : la glu

Ces modules ne décrivent pas un effet mais un branchement. Ils s'appliquent à
n'importe quel type et sont l'ossature des pouvoirs à plusieurs capacités.

| Module | Effet | Types |
|---|---|---|
| Déclencheur | la capacité part à l'impact, à retardement ou sur condition | tous |
| Lien | la capacité dépend d'une autre capacité du pouvoir | tous |
| Charge utile | la capacité en transporte une autre et la délivre | tous |
| Add Trigger | sur un déclencheur donné, active une capacité imbriquée | tous |
| Charges | nombre d'emplois avant rechargement | tous |
| Piège posé | la capacité est posée d'avance et attend (se marie à l'In) | tous |
| Déclenchement multiple | plusieurs capacités partent d'un même geste | tous |

---

### 6. Couverture : reconstruire l'œuvre

Quelques familles de pouvoirs canoniques, et l'assemblage qui les rend, sans
chiffre. Les réceptacles conjurés sont signalés comme reportés, le temps que leur
type revienne.

| Pouvoir | Assemblage |
|---|---|
| Coup renforcé brut | attaque + dégâts (renforcement) |
| Trait d'énergie | attaque + portée (émission) |
| Trait à tête chercheuse | attaque + portée + guidage (émission) |
| Posture d'amplification | effet + caractéristiques (renforcement), à maintien |
| Foudre / corps électrique | effet + électrique (transmutation) + actions et initiative (renforcement) |
| Aura collante et élastique fixée à une cible | effet + adhésif + élastique (transmutation) + lien (émission), à maintien |
| Illusion de texture | effet + texture (transmutation) |
| Emprise scellée par un contact | effet + emprise + asservissement par condition (manipulation) |
| Sort à déclencheur (frappe puis libère un second effet) | attaque + Add Trigger (raccord), capacité imbriquée |
| Bête de garde autonome | catégorie conjuration, type reporté |
| Réserve de pouvoirs prêts à l'emploi | catégorie conjuration, type reporté |

Les cas qui résistent (vol de pouvoir, prédiction, invisibilité parfaite, copie
d'aptitude) relèvent tous de la spécialisation : c'est précisément le dixième
qu'on laisse de côté, par cohérence avec l'œuvre.

---

### 7. Ce qui change, ce qu'on garde, ce qui reste à faire

*Ce qui change.*

- Le type se réduit à trois valeurs (attaque, défense, effet), communes à toutes
  les catégories. Les types spéciaux (conjuration de réceptacle, effet conjuré)
  sont reportés.
- La fiche de module s'élargit à des attributs fixes : catégorie(s), types
  compatibles, UA, maintien, conception, caractéristique requise, modificateur
  d'affinité d'emploi.
- Une fiche se lit en plusieurs paliers de puissance croissante, un retenu à la
  conception, et peut comporter plusieurs grilles combinables (par exemple le
  Catalogue).
- Chaque module relève d'une seule catégorie ; un concept présent dans plusieurs
  écoles y figure comme autant d'entrées distinctes, triables par catégorie.
- Chaque capacité et chaque module portent un modificateur d'affinité
  d'emploi ; les conditions le décalent au niveau où elles sont posées.
- Le raccord entre capacités devient un jeu de modules à part entière.
- Certains modules portent une ou plusieurs capacités imbriquées (Add Trigger,
  charge utile, Catalogue), ce qui rend le système récursif.
- Un module peut n'avoir aucune catégorie : il se paie alors directement en DI, et
  aucune affinité ne le concerne.
- L'affinité (notée +XX% / -XX%) ne multiplie que les effets chiffrés ; les effets
  descriptifs (déclencheurs, nombres, facultés) ne sont pas multipliés, même si le
  module porte une valeur d'affinité.

*Ce qu'on garde.*

- Tous les modules déjà écrits (renforcement, émission, conjuration) et leur
  intention.
- Le modèle d'archétype et d'affinité : il rebranche sur la catégorie portée par
  chaque module, et le modificateur ne fait que le décaler.
- Les régimes de durée et la persistance propre à la conjuration.

*Ce qui reste à chiffrer.*

- Les valeurs des attributs de chaque fiche, sur la grille déjà éprouvée.
- Un éventuel plancher des décalages d'affinité (le plafond est fixé : +100 % au total).
- Le levier des serments et restrictions (ampleur du décalage selon la gêne).
- Les paliers chiffrés de transmutation et de manipulation, une fois leurs effets
  stabilisés.

*Ce qui reste à trancher (arbitrages).*

- Si une condition de pur raccord décale le modificateur, ou si seul le serment le
  fait.
- Quand et sous quelle forme réintroduire les types spéciaux reportés.

---

### 8. Banc d'essai : onze modules complets

> Contrairement au reste du document, cette section porte des valeurs concrètes :
> c'est un banc d'essai pour vérifier que le modèle tient bout à bout. Les coûts se
> calquent sur le système de Ki d'*Anima*, effet par effet : chaque module, et
> chaque grille, suit l'effet d'Anima dont la nature lui correspond et en reprend les
> vraies valeurs (UA = Primario × 20, DI = MK, MA = Maintien × 20). Le module
> d'attaque n'est pas un plafond : chaque effet a son propre maximum, plus haut ou
> plus bas. On lisse en progression régulière (DI multiples de 5, UA et MA multiples
> de 10) et la caractéristique requise monte de 5 à 30 selon le niveau de technique.
> Attaque suit « Habilidad de ataque » ; Attaque complète suit « Attack Ability
> (Multiple) », le bonus à toutes les attaques du round ; Dégâts et Dégâts complets reprennent « Damage Augmentation » (Single et Multiple) ; Esquive et Parade, avec leurs versions complètes, suivent « Dodge Ability » et « Block Ability » ; Ajouter un Déclencheur
> emprunte sa visée à « Combat Maneuvers / Precisión » ; le Catalogue, qui fabrique des
> capacités, porte une conception délibérément très lourde, l'un des effets les plus
> forts du jeu ; le Stockage, simple utilitaire, reste bien moins cher.

<div class="cj-modules anima" markdown>

<div class="keep" markdown>

#### Attaque

<p class="mod-type">Catégorie : renforcement<br>
Types : attaque</p>

Tant que la capacité est active, le personnage ajoute le bonus indiqué à l'une de ses attaques. Cet effet est chiffré : le bonus est multiplié par l'affinité d'emploi effective (un +30 porté à 120 % vaut +36).

<table>
<thead><tr><th>Bonus</th><th>DI</th><th>CAR</th><th>UA</th><th>MA</th><th>AE</th></tr></thead>
<tbody>
<tr><td>+10</td><td>5</td><td>5</td><td>40</td><td>20</td><td>—</td></tr>
<tr><td>+20</td><td>5</td><td>6</td><td>50</td><td>30</td><td>—</td></tr>
<tr><td>+30</td><td>10</td><td>7</td><td>60</td><td>40</td><td>—</td></tr>
<tr><td>+40</td><td>10</td><td>8</td><td>80</td><td>50</td><td>—</td></tr>
<tr><td>+50</td><td>15</td><td>9</td><td>100</td><td>60</td><td>—</td></tr>
<tr><td>+60</td><td>15</td><td>10</td><td>120</td><td>70</td><td>—</td></tr>
<tr><td>+70</td><td>20</td><td>11</td><td>140</td><td>80</td><td>—</td></tr>
<tr><td>+80</td><td>20</td><td>12</td><td>170</td><td>90</td><td>—</td></tr>
<tr><td>+90</td><td>25</td><td>13</td><td>200</td><td>100</td><td>—</td></tr>
<tr><td>+100</td><td>25</td><td>14</td><td>230</td><td>120</td><td>—</td></tr>
<tr><td>+110</td><td>30</td><td>15</td><td>260</td><td>140</td><td>—</td></tr>
<tr><td>+120</td><td>30</td><td>16</td><td>290</td><td>160</td><td>—</td></tr>
<tr><td>+130</td><td>35</td><td>17</td><td>320</td><td>180</td><td>—</td></tr>
<tr><td>+140</td><td>35</td><td>18</td><td>360</td><td>200</td><td>—</td></tr>
<tr><td>+150</td><td>40</td><td>20</td><td>400</td><td>220</td><td>—</td></tr>
<tr><td>+160</td><td>40</td><td>22</td><td>440</td><td>240</td><td>—</td></tr>
<tr><td>+170</td><td>45</td><td>24</td><td>480</td><td>270</td><td>—</td></tr>
<tr><td>+180</td><td>45</td><td>26</td><td>520</td><td>300</td><td>—</td></tr>
<tr><td>+190</td><td>50</td><td>28</td><td>560</td><td>330</td><td>—</td></tr>
<tr><td>+200</td><td>50</td><td>30</td><td>600</td><td>360</td><td>—</td></tr>
</tbody>
</table>

</div>

<div class="keep" markdown>

#### Attaque complète

<p class="mod-type">Catégorie : renforcement<br>
Types : attaque</p>

Tant que la capacité est active, le personnage ajoute le bonus indiqué à toutes ses attaques du round, et non à une seule comme Attaque ; c'est l'attaque complète d'Anima. Cet effet est chiffré : le bonus est multiplié par l'affinité d'emploi effective. Couvrir toutes les attaques coûte bien plus cher que d'en renforcer une, et le bonus plafonne à +100.

<table>
<thead><tr><th>Bonus</th><th>DI</th><th>CAR</th><th>UA</th><th>MA</th><th>AE</th></tr></thead>
<tbody>
<tr><td>+10</td><td>10</td><td>8</td><td>80</td><td>40</td><td>—</td></tr>
<tr><td>+20</td><td>10</td><td>10</td><td>120</td><td>80</td><td>—</td></tr>
<tr><td>+30</td><td>15</td><td>12</td><td>160</td><td>120</td><td>—</td></tr>
<tr><td>+40</td><td>20</td><td>14</td><td>200</td><td>160</td><td>—</td></tr>
<tr><td>+50</td><td>25</td><td>16</td><td>240</td><td>200</td><td>—</td></tr>
<tr><td>+60</td><td>30</td><td>18</td><td>290</td><td>240</td><td>—</td></tr>
<tr><td>+70</td><td>40</td><td>21</td><td>340</td><td>280</td><td>—</td></tr>
<tr><td>+80</td><td>50</td><td>24</td><td>400</td><td>320</td><td>—</td></tr>
<tr><td>+90</td><td>60</td><td>27</td><td>480</td><td>360</td><td>—</td></tr>
<tr><td>+100</td><td>70</td><td>30</td><td>560</td><td>400</td><td>—</td></tr>
</tbody>
</table>

</div>

<div class="keep" markdown>

#### Dégâts

<p class="mod-type">Catégorie : renforcement<br>
Types : attaque</p>

Tant que la capacité est active, le personnage ajoute le bonus indiqué aux dégâts de l'une de ses attaques. Cet effet est chiffré : le bonus est multiplié par l'affinité d'emploi effective. C'est le pendant, côté dégâts, de l'Attaque : sa conception coûte autant, mais son aura et son maintien sont plus légers.

<table>
<thead><tr><th>Bonus</th><th>DI</th><th>CAR</th><th>UA</th><th>MA</th><th>AE</th></tr></thead>
<tbody>
<tr><td>+10</td><td>5</td><td>5</td><td>20</td><td>20</td><td>—</td></tr>
<tr><td>+20</td><td>5</td><td>6</td><td>30</td><td>20</td><td>—</td></tr>
<tr><td>+30</td><td>10</td><td>7</td><td>40</td><td>20</td><td>—</td></tr>
<tr><td>+40</td><td>10</td><td>8</td><td>50</td><td>20</td><td>—</td></tr>
<tr><td>+50</td><td>15</td><td>9</td><td>60</td><td>30</td><td>—</td></tr>
<tr><td>+60</td><td>15</td><td>10</td><td>70</td><td>40</td><td>—</td></tr>
<tr><td>+70</td><td>20</td><td>11</td><td>90</td><td>50</td><td>—</td></tr>
<tr><td>+80</td><td>20</td><td>12</td><td>110</td><td>60</td><td>—</td></tr>
<tr><td>+90</td><td>25</td><td>13</td><td>130</td><td>70</td><td>—</td></tr>
<tr><td>+100</td><td>25</td><td>14</td><td>150</td><td>80</td><td>—</td></tr>
<tr><td>+110</td><td>30</td><td>15</td><td>170</td><td>90</td><td>—</td></tr>
<tr><td>+120</td><td>30</td><td>16</td><td>190</td><td>100</td><td>—</td></tr>
<tr><td>+130</td><td>35</td><td>17</td><td>210</td><td>110</td><td>—</td></tr>
<tr><td>+140</td><td>35</td><td>18</td><td>230</td><td>120</td><td>—</td></tr>
<tr><td>+150</td><td>40</td><td>20</td><td>250</td><td>140</td><td>—</td></tr>
<tr><td>+160</td><td>40</td><td>22</td><td>280</td><td>160</td><td>—</td></tr>
<tr><td>+170</td><td>45</td><td>24</td><td>310</td><td>180</td><td>—</td></tr>
<tr><td>+180</td><td>45</td><td>26</td><td>340</td><td>200</td><td>—</td></tr>
<tr><td>+190</td><td>50</td><td>28</td><td>370</td><td>220</td><td>—</td></tr>
<tr><td>+200</td><td>50</td><td>30</td><td>400</td><td>240</td><td>—</td></tr>
</tbody>
</table>

</div>

<div class="keep" markdown>

#### Dégâts complets

<p class="mod-type">Catégorie : renforcement<br>
Types : attaque</p>

Tant que la capacité est active, le personnage ajoute le bonus indiqué aux dégâts de toutes ses attaques du round, et non à une seule comme Dégâts ; c'est l'augmentation de dégâts complète d'Anima. Couvrir chaque attaque coûte bien plus cher, et le bonus plafonne à +100.

<table>
<thead><tr><th>Bonus</th><th>DI</th><th>CAR</th><th>UA</th><th>MA</th><th>AE</th></tr></thead>
<tbody>
<tr><td>+10</td><td>10</td><td>8</td><td>40</td><td>20</td><td>—</td></tr>
<tr><td>+20</td><td>10</td><td>10</td><td>60</td><td>40</td><td>—</td></tr>
<tr><td>+30</td><td>15</td><td>12</td><td>80</td><td>60</td><td>—</td></tr>
<tr><td>+40</td><td>20</td><td>14</td><td>100</td><td>80</td><td>—</td></tr>
<tr><td>+50</td><td>25</td><td>16</td><td>120</td><td>100</td><td>—</td></tr>
<tr><td>+60</td><td>30</td><td>18</td><td>150</td><td>120</td><td>—</td></tr>
<tr><td>+70</td><td>35</td><td>21</td><td>180</td><td>140</td><td>—</td></tr>
<tr><td>+80</td><td>40</td><td>24</td><td>210</td><td>160</td><td>—</td></tr>
<tr><td>+90</td><td>45</td><td>27</td><td>240</td><td>180</td><td>—</td></tr>
<tr><td>+100</td><td>50</td><td>30</td><td>280</td><td>200</td><td>—</td></tr>
</tbody>
</table>

</div>

<div class="keep" markdown>

#### Esquive

<p class="mod-type">Catégorie : renforcement<br>
Types : défense</p>

Tant que la capacité est active, le personnage ajoute le bonus indiqué à l'une de ses esquives. Cet effet est chiffré : le bonus est multiplié par l'affinité d'emploi effective. C'est le pendant, côté esquive, de l'Attaque : sa conception coûte autant, mais son maintien est plus léger.

<table>
<thead><tr><th>Bonus</th><th>DI</th><th>CAR</th><th>UA</th><th>MA</th><th>AE</th></tr></thead>
<tbody>
<tr><td>+10</td><td>5</td><td>5</td><td>40</td><td>20</td><td>—</td></tr>
<tr><td>+20</td><td>5</td><td>6</td><td>50</td><td>20</td><td>—</td></tr>
<tr><td>+30</td><td>10</td><td>7</td><td>60</td><td>30</td><td>—</td></tr>
<tr><td>+40</td><td>10</td><td>8</td><td>80</td><td>40</td><td>—</td></tr>
<tr><td>+50</td><td>15</td><td>9</td><td>100</td><td>50</td><td>—</td></tr>
<tr><td>+60</td><td>15</td><td>10</td><td>120</td><td>60</td><td>—</td></tr>
<tr><td>+70</td><td>20</td><td>11</td><td>140</td><td>70</td><td>—</td></tr>
<tr><td>+80</td><td>20</td><td>12</td><td>170</td><td>80</td><td>—</td></tr>
<tr><td>+90</td><td>25</td><td>13</td><td>200</td><td>90</td><td>—</td></tr>
<tr><td>+100</td><td>25</td><td>14</td><td>230</td><td>100</td><td>—</td></tr>
<tr><td>+110</td><td>30</td><td>15</td><td>260</td><td>120</td><td>—</td></tr>
<tr><td>+120</td><td>30</td><td>16</td><td>290</td><td>140</td><td>—</td></tr>
<tr><td>+130</td><td>35</td><td>17</td><td>320</td><td>160</td><td>—</td></tr>
<tr><td>+140</td><td>35</td><td>18</td><td>360</td><td>180</td><td>—</td></tr>
<tr><td>+150</td><td>40</td><td>20</td><td>400</td><td>200</td><td>—</td></tr>
<tr><td>+160</td><td>40</td><td>22</td><td>440</td><td>220</td><td>—</td></tr>
<tr><td>+170</td><td>45</td><td>24</td><td>480</td><td>240</td><td>—</td></tr>
<tr><td>+180</td><td>45</td><td>26</td><td>520</td><td>260</td><td>—</td></tr>
<tr><td>+190</td><td>50</td><td>28</td><td>560</td><td>290</td><td>—</td></tr>
<tr><td>+200</td><td>50</td><td>30</td><td>600</td><td>320</td><td>—</td></tr>
</tbody>
</table>

</div>

<div class="keep" markdown>

#### Esquive complète

<p class="mod-type">Catégorie : renforcement<br>
Types : défense</p>

Tant que la capacité est active, le personnage ajoute le bonus indiqué à toutes ses esquives du round, et non à une seule comme Esquive ; c'est l'esquive complète d'Anima. Couvrir toutes ses esquives coûte bien plus cher, et le bonus plafonne à +100.

<table>
<thead><tr><th>Bonus</th><th>DI</th><th>CAR</th><th>UA</th><th>MA</th><th>AE</th></tr></thead>
<tbody>
<tr><td>+10</td><td>10</td><td>8</td><td>80</td><td>40</td><td>—</td></tr>
<tr><td>+20</td><td>10</td><td>10</td><td>120</td><td>60</td><td>—</td></tr>
<tr><td>+30</td><td>15</td><td>12</td><td>160</td><td>80</td><td>—</td></tr>
<tr><td>+40</td><td>20</td><td>14</td><td>200</td><td>100</td><td>—</td></tr>
<tr><td>+50</td><td>25</td><td>16</td><td>240</td><td>120</td><td>—</td></tr>
<tr><td>+60</td><td>35</td><td>18</td><td>300</td><td>160</td><td>—</td></tr>
<tr><td>+70</td><td>45</td><td>21</td><td>360</td><td>200</td><td>—</td></tr>
<tr><td>+80</td><td>55</td><td>24</td><td>440</td><td>250</td><td>—</td></tr>
<tr><td>+90</td><td>65</td><td>27</td><td>520</td><td>300</td><td>—</td></tr>
<tr><td>+100</td><td>75</td><td>30</td><td>600</td><td>360</td><td>—</td></tr>
</tbody>
</table>

</div>

<div class="keep" markdown>

#### Parade

<p class="mod-type">Catégorie : renforcement<br>
Types : défense</p>

Tant que la capacité est active, le personnage ajoute le bonus indiqué à l'une de ses parades. Cet effet est chiffré : le bonus est multiplié par l'affinité d'emploi effective. C'est le pendant, côté parade, de l'Attaque : sa conception coûte autant, mais son maintien est plus léger.

<table>
<thead><tr><th>Bonus</th><th>DI</th><th>CAR</th><th>UA</th><th>MA</th><th>AE</th></tr></thead>
<tbody>
<tr><td>+10</td><td>5</td><td>5</td><td>40</td><td>20</td><td>—</td></tr>
<tr><td>+20</td><td>5</td><td>6</td><td>50</td><td>20</td><td>—</td></tr>
<tr><td>+30</td><td>10</td><td>7</td><td>60</td><td>30</td><td>—</td></tr>
<tr><td>+40</td><td>10</td><td>8</td><td>80</td><td>40</td><td>—</td></tr>
<tr><td>+50</td><td>15</td><td>9</td><td>100</td><td>50</td><td>—</td></tr>
<tr><td>+60</td><td>15</td><td>10</td><td>120</td><td>60</td><td>—</td></tr>
<tr><td>+70</td><td>20</td><td>11</td><td>140</td><td>70</td><td>—</td></tr>
<tr><td>+80</td><td>20</td><td>12</td><td>170</td><td>80</td><td>—</td></tr>
<tr><td>+90</td><td>25</td><td>13</td><td>200</td><td>90</td><td>—</td></tr>
<tr><td>+100</td><td>25</td><td>14</td><td>230</td><td>100</td><td>—</td></tr>
<tr><td>+110</td><td>30</td><td>15</td><td>260</td><td>120</td><td>—</td></tr>
<tr><td>+120</td><td>30</td><td>16</td><td>290</td><td>140</td><td>—</td></tr>
<tr><td>+130</td><td>35</td><td>17</td><td>320</td><td>160</td><td>—</td></tr>
<tr><td>+140</td><td>35</td><td>18</td><td>360</td><td>180</td><td>—</td></tr>
<tr><td>+150</td><td>40</td><td>20</td><td>400</td><td>200</td><td>—</td></tr>
<tr><td>+160</td><td>40</td><td>22</td><td>440</td><td>220</td><td>—</td></tr>
<tr><td>+170</td><td>45</td><td>24</td><td>480</td><td>240</td><td>—</td></tr>
<tr><td>+180</td><td>45</td><td>26</td><td>520</td><td>260</td><td>—</td></tr>
<tr><td>+190</td><td>50</td><td>28</td><td>560</td><td>290</td><td>—</td></tr>
<tr><td>+200</td><td>50</td><td>30</td><td>600</td><td>320</td><td>—</td></tr>
</tbody>
</table>

</div>

<div class="keep" markdown>

#### Parade complète

<p class="mod-type">Catégorie : renforcement<br>
Types : défense</p>

Tant que la capacité est active, le personnage ajoute le bonus indiqué à toutes ses parades du round, et non à une seule comme Parade ; c'est la parade complète d'Anima. Couvrir toutes ses parades coûte bien plus cher, et le bonus plafonne à +100.

<table>
<thead><tr><th>Bonus</th><th>DI</th><th>CAR</th><th>UA</th><th>MA</th><th>AE</th></tr></thead>
<tbody>
<tr><td>+10</td><td>10</td><td>8</td><td>80</td><td>40</td><td>—</td></tr>
<tr><td>+20</td><td>10</td><td>10</td><td>120</td><td>60</td><td>—</td></tr>
<tr><td>+30</td><td>15</td><td>12</td><td>160</td><td>80</td><td>—</td></tr>
<tr><td>+40</td><td>20</td><td>14</td><td>200</td><td>100</td><td>—</td></tr>
<tr><td>+50</td><td>25</td><td>16</td><td>240</td><td>120</td><td>—</td></tr>
<tr><td>+60</td><td>35</td><td>18</td><td>300</td><td>160</td><td>—</td></tr>
<tr><td>+70</td><td>45</td><td>21</td><td>360</td><td>200</td><td>—</td></tr>
<tr><td>+80</td><td>55</td><td>24</td><td>440</td><td>250</td><td>—</td></tr>
<tr><td>+90</td><td>65</td><td>27</td><td>520</td><td>300</td><td>—</td></tr>
<tr><td>+100</td><td>75</td><td>30</td><td>600</td><td>360</td><td>—</td></tr>
</tbody>
</table>

</div>

<div class="keep" markdown>

#### Ajouter un Déclencheur à l'Attaque

<p class="mod-type">Catégorie : aucune<br>
Types : attaque</p>

Greffé sur une attaque, ce module y attache une capacité liée, une seule, qu'il déclenche quand l'attaque aboutit selon les conditions choisies. Plus ces conditions sont dures, plus l'affinité qu'il accorde monte ; cette affinité s'ajoute à l'affinité globale de la capacité liée. Le personnage retient obligatoirement un degré de touche et une visée, et peut y joindre une cible. Se restreindre librement pour gagner de l'affinité n'est pas propre à ce module : c'est un levier commun à toute capacité, qui se pose à son niveau, pas ici. La capacité liée paie ses propres coûts ; le module, lui, n'a pas de catégorie : il se paie en DI, et guetter puis tenir le déclencheur lui coûte une aura et un maintien propres, calés sur la finesse de sa visée. La capacité liée peut elle-même porter un déclencheur, les déclenchements s'enchaînant.

<table>
<thead><tr><th>Effet</th><th>DI</th><th>CAR</th><th>UA</th><th>MA</th><th>AE</th></tr></thead>
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
<tr><td>Pas de point précis</td><td>0</td><td>—</td><td>20</td><td>10</td><td>−20%</td></tr>
<tr><td>Torse, mollet (−10)</td><td>0</td><td>—</td><td>20</td><td>10</td><td>−10%</td></tr>
<tr><td>Abdomen, bras, avant-bras, cuisse (−20)</td><td>0</td><td>—</td><td>40</td><td>20</td><td>—</td></tr>
<tr><td>Épaule, hanche (−30)</td><td>5</td><td>—</td><td>40</td><td>20</td><td>+10%</td></tr>
<tr><td>Estomac, main, poignet, genou (−40)</td><td>5</td><td>—</td><td>60</td><td>30</td><td>+20%</td></tr>
<tr><td>Poumon, foie, cheville, pied (−50)</td><td>10</td><td>—</td><td>60</td><td>30</td><td>+30%</td></tr>
<tr><td>Tête, bouche, cœur, coude, aine (−60)</td><td>10</td><td>—</td><td>80</td><td>40</td><td>+40%</td></tr>
<tr><td>Oreille, nez, testicules (−70)</td><td>15</td><td>—</td><td>100</td><td>50</td><td>+50%</td></tr>
<tr><td>Cou, vulve (−80)</td><td>15</td><td>—</td><td>120</td><td>60</td><td>+60%</td></tr>
<tr><td>Doigt (−90)</td><td>20</td><td>—</td><td>140</td><td>70</td><td>+70%</td></tr>
<tr><td>Œil (−100)</td><td>20</td><td>—</td><td>160</td><td>80</td><td>+80%</td></tr>
</tbody>
</table>

<div class="defs" markdown>

**Cible :** qui doit être touché pour armer le déclencheur. Se déclencher sur l'attaquant (soi-même) est aisé ; toucher le défenseur applique le Nen sur autrui, plus difficile, d'où son malus d'affinité.

**Degré de touche :** marge de réussite exigée de l'attaque, de la simple touche (0 %) au coup largement réussi (200 %) ; plus la marge demandée est haute, plus l'affinité accordée monte.

**Visée :** la partie du corps visée, reprise de la manœuvre [Viser](../combat/manoeuvres.md) ; plus le point est petit et son malus de visée fort, plus l'affinité accordée monte.

**Affinité accordée :** la somme des affinités des options retenues s'ajoute à l'affinité globale de la capacité liée. Les choix les plus faciles imposent un malus d'affinité, les plus durs un bonus ; le plafond commun de +100 % d'affinité s'y applique comme à tout module. Le personnage en retient au moins le degré de touche et la visée.

**Coût :** l'aura et le maintien du déclencheur sont repris de l'effet de visée d'Anima ([Combat Maneuvers / Precisión](../combat/manoeuvres.md)) et portés par la visée, toujours retenue, donc tout déclencheur en a ; plus le point visé est fin, plus ils montent. Le DI grandit avec l'affinité accordée : une option neutre ou à malus ne coûte rien, sinon 5 DI par tranche de 20 % accordée. La capacité liée paie ses propres coûts quand elle se libère.

</div>

</div>

<div class="keep" markdown>

#### Catalogue

<p class="mod-type">Catégorie : conjuration<br>
Types : à décider (réceptacle reporté)</p>

Le Catalogue renferme un répertoire d'autres capacités du personnage, prêtes à l'emploi : il en tire l'une ou l'autre au moment voulu, comme on pioche dans une réserve. C'est l'un des modules les plus puissants, et l'un des plus coûteux. On définit combien de capacités il garde, combien peuvent exister à la fois, ce qu'il a le droit de cataloguer, et leur qualité commune. Comme partout, on ne retient qu'une ligne par catégorie, sauf celles marquées *cumulable*. Son effet est descriptif, un nombre de capacités, donc l'affinité n'en multiplie pas la valeur ; il porte tout de même un malus d'affinité, ici −60 %, comme frein à un module aussi fort. Le Catalogue ne s'emboîte pas : une capacité cataloguée ne renferme pas de Catalogue.

**Capacité** : combien de capacités le Catalogue garde, et combien peuvent exister
en même temps.

<table>
<thead><tr><th>Effet</th><th>DI</th><th>CAR</th><th>UA</th><th>MA</th><th>AE</th></tr></thead>
<tbody>
<tr class="cat"><td>Capacités cataloguées</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>1</td><td>30</td><td>10</td><td>20</td><td>20</td><td>—</td></tr>
<tr><td>2</td><td>60</td><td>12</td><td>30</td><td>30</td><td>—</td></tr>
<tr><td>3</td><td>100</td><td>14</td><td>40</td><td>40</td><td>—</td></tr>
<tr><td>4</td><td>150</td><td>16</td><td>50</td><td>50</td><td>—</td></tr>
<tr><td>5</td><td>210</td><td>18</td><td>60</td><td>60</td><td>—</td></tr>
<tr><td>6</td><td>280</td><td>20</td><td>70</td><td>70</td><td>—</td></tr>
<tr><td>7</td><td>360</td><td>22</td><td>90</td><td>80</td><td>—</td></tr>
<tr><td>8</td><td>450</td><td>24</td><td>110</td><td>90</td><td>—</td></tr>
<tr><td>9</td><td>550</td><td>27</td><td>130</td><td>100</td><td>—</td></tr>
<tr><td>10</td><td>660</td><td>30</td><td>160</td><td>120</td><td>—</td></tr>
<tr class="cat"><td>Extraction simultanée</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>1</td><td>0</td><td>5</td><td>0</td><td>0</td><td>−60%</td></tr>
<tr><td>2</td><td>60</td><td>11</td><td>40</td><td>20</td><td>−60%</td></tr>
<tr><td>3</td><td>130</td><td>17</td><td>80</td><td>40</td><td>−60%</td></tr>
<tr><td>4</td><td>210</td><td>23</td><td>120</td><td>60</td><td>−60%</td></tr>
<tr><td>5</td><td>300</td><td>30</td><td>160</td><td>80</td><td>−60%</td></tr>
</tbody>
</table>

<div class="defs" markdown>

**Capacités cataloguées :** nombre de capacités différentes que le Catalogue renferme, de une à dix. Sa conception est très lourde : fabriquer un répertoire de capacités est l'un des effets les plus forts du jeu, et c'est le DI, non l'aura, qui en marque le prix.

**Extraction simultanée :** nombre de ces capacités qui peuvent exister en même temps, de une à cinq ; les autres restent rangées. En tenir une seule ne coûte rien de plus ; chaque sortie de plus est une capacité vivante supplémentaire.

</div>

**Contenu et qualité** : ce que le Catalogue a le droit de renfermer, et la puissance commune de ses capacités.

<table>
<thead><tr><th>Effet</th><th>DI</th><th>CAR</th><th>UA</th><th>MA</th><th>AE</th></tr></thead>
<tbody>
<tr class="cat"><td>Contenu (cumulable)</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Capacités d'attaque</td><td>5</td><td>10</td><td>20</td><td>0</td><td>—</td></tr>
<tr><td>Capacités de défense</td><td>5</td><td>10</td><td>20</td><td>0</td><td>—</td></tr>
<tr><td>Capacités d'effet</td><td>5</td><td>10</td><td>20</td><td>0</td><td>—</td></tr>
<tr class="flush"><td>Qualité</td><td>VAR.</td><td>0</td><td>0</td><td>0</td><td>—</td></tr>
</tbody>
</table>

<div class="defs" markdown>

**Contenu (cumulable) :** les types de capacités que le Catalogue peut renfermer ; à cumuler pour en autoriser plusieurs. Chaque type ouvert coûte le même petit forfait, calé sur le plus petit effet d'Anima : DC 5, UA 20, IMA 5.

**Qualité (VAR.) :** le personnage investit librement un nombre de points de conception, X. Chaque capacité du Catalogue se bâtit avec un budget de X (base et modules compris) ; toutes partagent cette qualité. X ne se paie qu'une fois, quel que soit le nombre de capacités cataloguées. Le coût en Aura est variable lui aussi : tirer une capacité coûte l'UA de ses propres modules.

</div>

</div>

<div class="keep" markdown>

#### Stockage

<p class="mod-type">Catégorie : conjuration<br>
Types : à décider (réceptacle reporté)</p>

La capacité renferme objets ou matière dans un espace interne ; y ranger ou en sortir un élément coûte une action. On choisit d'abord ce qu'elle accueille et ses propriétés, puis on borne sa contenance d'une seule des deux façons : par nombre d'objets, ou par espace. Dans une grille, on ne retient qu'une ligne, sauf celles marquées *cumulable* ; les coûts de toutes les lignes retenues s'additionnent. Son effet est descriptif, une contenance, que l'affinité ne multiplie pas ; comme rien ne le justifie, le module n'impose aucun malus d'affinité. C'est un utilitaire : son coût reste modéré, sans commune mesure avec le Catalogue.

**Contenu et propriétés** : ce que le contenant accueille et ses options, quelle que soit la façon dont sa contenance est bornée.

<table>
<thead><tr><th>Effet</th><th>DI</th><th>CAR</th><th>UA</th><th>MA</th><th>AE</th></tr></thead>
<tbody>
<tr class="cat"><td>Contenu (cumulable)</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Objets</td><td>5</td><td>5</td><td>20</td><td>20</td><td>—</td></tr>
<tr><td>Créatures</td><td>25</td><td>13</td><td>60</td><td>40</td><td>—</td></tr>
<tr class="cat"><td>Propriétés (cumulable)</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Lumière</td><td>5</td><td>5</td><td>20</td><td>20</td><td>—</td></tr>
<tr><td>Eau</td><td>5</td><td>5</td><td>20</td><td>20</td><td>—</td></tr>
<tr><td>Nourriture</td><td>5</td><td>5</td><td>20</td><td>20</td><td>—</td></tr>
<tr><td>Air</td><td>15</td><td>9</td><td>40</td><td>20</td><td>—</td></tr>
<tr><td>Vivable</td><td>25</td><td>15</td><td>60</td><td>40</td><td>—</td></tr>
<tr><td>Temps arrêté</td><td>30</td><td>20</td><td>60</td><td>40</td><td>—</td></tr>
</tbody>
</table>

<div class="defs" markdown>

**Objets :** le contenant accueille objets et matière inerte.

**Créatures :** il peut renfermer des êtres vivants, qui y suffoquent faute d'air, à moins que l'intérieur ne dispose d'Air, ne soit Vivable, ou que le Temps y soit arrêté.

**Air, Eau, Nourriture, Lumière :** l'intérieur est respirable, ou une eau potable, de quoi se nourrir, ou la lumière y sont disponibles en continu.

**Vivable :** regroupe l'Air, l'Eau, la Nourriture et la Lumière pour moins cher que séparément ; l'intérieur est pleinement habitable.

**Temps arrêté :** le temps est comme figé à l'intérieur ; ni objet ni créature stockés n'y vieillissent.

</div>

**Par nombre d'objets** : un nombre fixe d'objets, chacun ne dépassant pas une taille maximale.

<table>
<thead><tr><th>Effet</th><th>DI</th><th>CAR</th><th>UA</th><th>MA</th><th>AE</th></tr></thead>
<tbody>
<tr class="cat"><td>Quantité</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>1 objet</td><td>5</td><td>5</td><td>20</td><td>20</td><td>—</td></tr>
<tr><td>2 objets</td><td>5</td><td>7</td><td>20</td><td>20</td><td>—</td></tr>
<tr><td>3 objets</td><td>10</td><td>10</td><td>40</td><td>20</td><td>—</td></tr>
<tr><td>5 objets</td><td>15</td><td>13</td><td>60</td><td>40</td><td>—</td></tr>
<tr><td>10 objets</td><td>20</td><td>16</td><td>80</td><td>40</td><td>—</td></tr>
<tr><td>20 objets</td><td>30</td><td>19</td><td>100</td><td>60</td><td>—</td></tr>
<tr><td>30 objets</td><td>40</td><td>22</td><td>130</td><td>60</td><td>—</td></tr>
<tr><td>50 objets</td><td>50</td><td>26</td><td>160</td><td>80</td><td>—</td></tr>
<tr><td>100 objets</td><td>70</td><td>30</td><td>220</td><td>100</td><td>—</td></tr>
<tr class="cat"><td>Taille maximale par objet</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Minuscule</td><td>5</td><td>5</td><td>20</td><td>20</td><td>—</td></tr>
<tr><td>Très petite</td><td>10</td><td>8</td><td>40</td><td>20</td><td>—</td></tr>
<tr><td>Petite</td><td>15</td><td>11</td><td>60</td><td>40</td><td>—</td></tr>
<tr><td>Moyenne</td><td>20</td><td>14</td><td>80</td><td>40</td><td>—</td></tr>
<tr><td>Grande</td><td>30</td><td>17</td><td>120</td><td>60</td><td>—</td></tr>
<tr><td>Très grande</td><td>45</td><td>20</td><td>160</td><td>80</td><td>—</td></tr>
<tr><td>Gigantesque</td><td>60</td><td>23</td><td>220</td><td>100</td><td>—</td></tr>
<tr><td>Colossale</td><td>80</td><td>26</td><td>300</td><td>120</td><td>—</td></tr>
<tr><td>Titanesque</td><td>105</td><td>30</td><td>400</td><td>160</td><td>—</td></tr>
</tbody>
</table>

**Par espace** : tout ce qui tient dans un volume fixe, jusqu'à une charge maximale.

<table>
<thead><tr><th>Effet</th><th>DI</th><th>CAR</th><th>UA</th><th>MA</th><th>AE</th></tr></thead>
<tbody>
<tr class="cat"><td>Volume</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Cube de 1 m d'arête</td><td>5</td><td>5</td><td>20</td><td>20</td><td>—</td></tr>
<tr><td>Cube de 3 m d'arête</td><td>15</td><td>9</td><td>40</td><td>20</td><td>—</td></tr>
<tr><td>Cube de 10 m d'arête</td><td>30</td><td>13</td><td>80</td><td>40</td><td>—</td></tr>
<tr><td>Cube de 30 m d'arête</td><td>50</td><td>17</td><td>120</td><td>60</td><td>—</td></tr>
<tr><td>Cube de 100 m d'arête</td><td>75</td><td>21</td><td>180</td><td>80</td><td>—</td></tr>
<tr><td>Cube de 300 m d'arête</td><td>105</td><td>25</td><td>260</td><td>120</td><td>—</td></tr>
<tr><td>Cube de 1 km d'arête</td><td>140</td><td>30</td><td>360</td><td>160</td><td>—</td></tr>
<tr class="cat"><td>Charge maximale</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>100 kg</td><td>5</td><td>5</td><td>20</td><td>20</td><td>—</td></tr>
<tr><td>1 t</td><td>15</td><td>7</td><td>40</td><td>20</td><td>—</td></tr>
<tr><td>10 t</td><td>25</td><td>9</td><td>80</td><td>40</td><td>—</td></tr>
<tr><td>100 t</td><td>40</td><td>11</td><td>120</td><td>60</td><td>—</td></tr>
<tr><td>1 000 t</td><td>55</td><td>13</td><td>180</td><td>80</td><td>—</td></tr>
<tr><td>10 000 t</td><td>75</td><td>15</td><td>250</td><td>120</td><td>—</td></tr>
<tr><td>100 000 t</td><td>95</td><td>18</td><td>330</td><td>160</td><td>—</td></tr>
<tr><td>1 000 000 t</td><td>120</td><td>21</td><td>420</td><td>200</td><td>—</td></tr>
<tr><td>10 000 000 t</td><td>150</td><td>24</td><td>520</td><td>260</td><td>—</td></tr>
<tr><td>100 000 000 t</td><td>180</td><td>27</td><td>630</td><td>320</td><td>—</td></tr>
<tr><td>1 000 000 000 t</td><td>210</td><td>30</td><td>750</td><td>380</td><td>—</td></tr>
</tbody>
</table>

</div>

</div>

#### À décider ensemble

- Affiner Ajouter un Déclencheur à l'Attaque et le Catalogue : valeurs posées en
  première passe (déclencheur avec aura et maintien portés par les conditions
  obligatoires, DI à 5 par 10 % d'affinité ; Catalogue rechiffré à neuf sur l'échelle
  Ki, de modeste à N=1 au sommet du module d'attaque à N=50), à valider.
- Le plafond de +100 % d'affinité du déclencheur n'écrête pas encore le DI cumulé :
  empiler les conditions au-delà du plafond paie une affinité jamais reçue.
- Le Catalogue siège d'ordinaire sur un objet conjuré, dont le type est reporté.
  Reste à choisir : on le rattache à ce réceptacle, ou on en fait un module d'effet
  autonome qui se suffit à lui-même.
- Stockage : valeurs posées à un niveau utilitaire (bien sous le Catalogue), à
  valider.
- Jusqu'où vont les déclencheurs en chaîne d'Ajouter un Déclencheur (profondeur de
  la récursion).

</div>
