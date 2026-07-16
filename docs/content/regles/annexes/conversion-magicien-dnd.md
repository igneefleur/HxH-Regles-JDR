# Conversion Magicien D&D

<div class="cols annexe-dnd" markdown>

La magie du [mage noir](../art/arts-sociaux.md) se joue avec la classe Magicien du Manuel des joueurs 2024 de Donjons et Dragons. La classe se lit dans son livre d'origine ; cette annexe convertit ses règles vers celles du livre.

### La classe

On ne garde du magicien que sa magie : les emplacements de sorts, les sorts préparés, le grimoire, les tours de magie, les rituels et la Restauration arcanique. Le reste ne s'applique pas : points de vie, dés de vie, classe d'armure, maîtrises, dons, historique et sous-classe. Le magicien ne bénéficie pas non plus des Améliorations de caractéristiques des niveaux 4, 8, 12 et 16, ni du Don épique du niveau 19.

### Le grimoire

Le magicien ne reçoit aucun sort gratuit, ni avec la classe ni en gagnant des niveaux : chaque sort de son grimoire doit être trouvé, puis retranscrit. Pour trouver un sort sur les forums de mages noirs, il fait un jet d'[Enquête](../personnage/competences.md) contre la difficulté donnée par le niveau du sort, dans la table ci-dessous. S'il le trouve, il peut le retranscrire : la retranscription lui demande 2 heures et 50 000 Ɉ par niveau du sort.

| Niveau du sort | Difficulté de recherche |
|:---:|---|
| 1 | Difficile (120) |
| 2 | Très difficile (180) |
| 3 | Absurde (240) |
| 4 | Quasi impossible (320) |
| 5 | Impossible (400) |
| 6 | Surhumaine (520) |
| 7 | Prodigieuse (640) |
| 8 | Insurmontable (780) |
| 9 | Inimaginable (920) |

### Les sorts bannis

Deux familles de sorts n'existent pas dans le monde ; leurs sorts ne peuvent être ni trouvés ni lancés :

- les sorts qui créent ou convoquent des créatures, ou qui emploient le profil d'une créature de D&D : Animation des morts, Animation des objets, Changement de forme, Coursier fantôme, Création de mort-vivant, Métamorphose, Métamorphose suprême, Simulacre, et les Convocations d'aberration, de construction, de dragon, d'élémentaire, de fée, de fiélon et de mort-vivant ;
- les sorts qui passent par d'autres plans d'existence : Bannissement, Changement de plan, Contact avec les plans, Entrave planaire, Forme éthérée, Portail et Projection astrale.

Les sorts qui créent leur propre espace restent permis, comme Corde enchantée, Demi-plan, Labyrinthe ou le Manoir somptueux de Mordenkainen.

Appel de familier fait exception à la première famille : le sort ne peut être utilisé qu'en nouant un lien avec un animal réel, que le personnage doit d'abord trouver. L'animal garde son profil et devient le familier du personnage ; le reste du sort s'applique à lui tel quel. Le MJ définit quel animal peut être un familier.

### Les sorts

Dans un même round, le personnage ne peut lancer qu'un seul sort qui coûte une action ou une action bonus, même s'il lui reste des actions. Il ne peut lancer qu'un seul sort qui coûte une réaction jusqu'au début de son prochain tour. Un sort qui effectue une attaque compte comme une [attaque](../combat/manoeuvres.md) : il en suit toutes les règles, à commencer par la limite d'une attaque par round.

### Les jets

Tous les jets se lancent avec les dés du livre : le d20 de D&D ne sert jamais.

Un jet d'attaque de sort est un jet d'attaque ordinaire, opposé à la défense de la cible ; la classe d'armure ne sert pas. La compétence dépend de l'attaque du sort, et le personnage y remplace la Dextérité par sa Logique : [Armes de trait](../personnage/competences.md) pour une attaque de sort à distance, [Armes de mêlée](../personnage/competences.md) pour une attaque de sort au corps à corps, et [Armes de jet](../personnage/competences.md) pour lancer une arme créée par un sort et dotée de la propriété Lancer de D&D.

Un jet de caractéristique de D&D se fait avec la caractéristique correspondante du livre et la compétence la plus proche de la tâche ; le MJ la choisit.

### Les bonus et les malus

Les bonus, les malus et les seuils chiffrés de D&D se multiplient par 10. L'avantage donne +40 au jet ; le désavantage donne −40.

<p class="formula">Valeur du livre = valeur de D&D × 10</p>

La classe d'armure n'existe pas dans le livre. Un bonus de CA devient un bonus d'[Esquive et de Parade](../personnage/competences.md), de +10 par point de CA. Une CA de base fixée par un sort ne donne rien ; le reste du sort s'applique normalement.

Un sort qui change la vitesse change le [Mouvement](../personnage/capacites-physiques.md#mouvement) : un bonus en mètres s'ajoute à la distance que le personnage franchit par round, un doublement la double, une réduction de moitié la divise par deux. Un sort qui accorde une vitesse de vol, d'escalade ou de nage donne ce mode de déplacement, à la valeur convertie de la même façon.

### Les sauvegardes

La cible d'un jet de sauvegarde fait un jet contre le DD du sort, qui vaut vingt fois le niveau du personnage qui le lance. La compétence du jet suit la caractéristique de la sauvegarde et la nature de l'effet.

<p class="formula">DD d'un sort = niveau du personnage × 20</p>

| Sauvegarde de D&D | Jet du livre |
|---|---|
| Force | [Prouesse de Force](../personnage/competences.md) |
| Dextérité | [Esquive](../personnage/competences.md) |
| Constitution, contre des dégâts de poison, l'état Empoisonné ou une maladie | [Résistance à la Maladie et au Poison](../personnage/competences.md) |
| Constitution, contre des dégâts de froid ou de chaleur | [Résistance à l'Environnement](../personnage/competences.md) |
| Constitution, contre l'état Épuisement | [Résistance à l'Épuisement](../personnage/competences.md) |
| Constitution, tout le reste, dont la concentration | [Résistance à la Douleur](../personnage/competences.md) |
| Sagesse, contre un effet qui inflige l'état Effrayé | [Résistance à la Peur](../personnage/competences.md) |
| Sagesse, Intelligence et Charisme, tout le reste | [Résistance à l'Influence](../personnage/competences.md) |

### Le modificateur de caractéristique

Quand un sort emploie un modificateur de caractéristique de D&D, il se calcule sur la caractéristique du livre la plus proche, avec la formule de D&D : la valeur moins 10, divisée par 2, arrondie à l'inférieur. Le modificateur d'incantation du magicien se calcule ainsi sur la [Logique](../personnage/caracteristiques.md).

<p class="formula">Modificateur de D&D = (caractéristique du livre − 10) ÷ 2, arrondi à l'inférieur</p>

### Les dégâts et les soins

Les dés du sort se lancent tels quels et leur total se multiplie par 10 : dégâts, soins et points de vie temporaires. La résistance à un type de dégâts divise par deux les dégâts de ce type ; l'immunité les annule ; la vulnérabilité les double. Le [type de dégâts](../monde/degats.md) se lit dans la table ci-dessous.

| Type de D&D | Type du livre |
|---|---|
| Contondant, force, tonnerre | CON |
| Perforant, psychique | PER |
| Tranchant | TRA |
| Feu | FEU |
| Froid | FRO |
| Foudre, radiant | ÉLE |
| Acide, poison, nécrotique | DÉC |

### Le reste

<div class="defs" markdown>

**Monnaie :** 1 po vaut 1 000 Ɉ, composantes matérielles comprises.

**Temps :** le round de D&D dure 6 secondes, comme celui du livre : les rounds, les minutes et les heures se gardent tels quels.

**Actions :** l'action et l'action bonus coûtent chacune une [action](../combat/deroulement-combat.md) ; la réaction est une [réaction](../combat/deroulement-combat.md) ; la concentration se garde telle quelle.

**Repos :** un repos long de D&D correspond à un [sommeil correct](../personnage/capacites-physiques.md#sommeil-et-repos) ; un repos court, à une heure d'[activité](../personnage/capacites-physiques.md#activite) légère.

**Sens :** un sort qui accorde un sens, comme la vision dans le noir, donne le [sens](../personnage/sens.md) du livre le plus proche ; le MJ tranche.

**Lumière :** sur la table d'[obscurité](../personnage/sens.md) de la Vue, la lumière vive de D&D est le plein jour et la lumière faible la pénombre ; les ténèbres magiques sont un noir absolu, où rien ne se perçoit.

**Tailles :** une catégorie de taille de D&D se lit dans la [taille](../monde/tailles.md) du livre du même nom.

**Types de créature :** un sort qui ne vise qu'un type de créature de D&D vise l'équivalent du monde : humanoïde couvre les [bipèdes à bras](../monde/formes.md), et le MJ tranche le reste.

**Magie et Nen :** la magie et le Nen n'ont rien à voir : un sort qui détecte, identifie, dissipe ou contre la magie est sans effet sur le Nen.

**États :** un état de D&D se lit dans l'[état](../personnage/etats.md) du livre le plus proche ; le MJ tranche.

</div>

### Ce qui n'est pas écrit

Cette annexe ne peut pas tout prévoir. Tout ce qu'elle ne tranche pas revient au MJ : il convertit au plus proche des règles du livre.

</div>
