# Système de points des armes

<div class="cols" markdown>

### Principe

Chaque arme vaut exactement 100 points :

Dégâts + Type + Portée(s) + Mains + Propriétés + Compatibilité AM + Modificateur − Contraintes − Illégalité = 100

Le barème est « gros » : tout est en multiples de 10, ce qui force chaque arme à porter quelques propriétés fortes plutôt qu'une longue liste de petits traits.

### Dégâts

Chaque arme part de 20 dégâts de base gratuits (le score d'une attaque à mains nues) ; le système de points n'achète que les dégâts *au-dessus* de 20. Les dégâts affichés dans les tableaux incluent déjà cette base.

| Élément | Points |
|---|---|
| Dégâts | (valeur affichée − 20), le plus souvent multiples de 10 ; affichage de 20 à 200 |

### Type de dégâts

Le ou les types de dégâts infligés (voir la page Types de Dégâts). Les types physiques (CON, TRA, PER) sont gratuits ; les types élémentaires (FEU, FRO, ÉLE, DÉC) et chaque type supplémentaire coûtent des points. Avec plusieurs types, l'attaquant choisit lequel à chaque attaque.

| Type de dégâts | Points |
|---|---|
| Un type physique (CON / TRA / PER) | 0 |
| Chaque type au-delà du premier | +10 |
| Chaque type élémentaire (FEU / FRO / ÉLE / DÉC) | +20 |

### Mains

Le nombre de mains nécessaires pour manier l'arme.

| Mains | Effet | Points |
|---|---|---|
| 1 main | L'arme se manie à une main. | 0 |
| Polyvalente | L'arme se manie à une ou deux mains. Tenue à une seule main, le personnage subit un malus de −10 à l'attaque. | −10 |
| 2 mains | L'arme se manie à deux mains. Tenue à une seule main, le personnage subit un malus de −40 à l'attaque. | −20 |

### Modificateur de dégâts

À chaque attaque, le porteur ajoute à ses dégâts N fois son modificateur de Force (le multiplicateur ×N de l'arme, de ×0 à ×3 ; voir le Tableau des Modificateurs des caractéristiques). Une arme Finesse utilise le modificateur de Dextérité à la place. Les armes à gâchette ou mécaniques (armes à feu, arbalètes, explosifs, lanceurs) sont en ×0.

| Multiplicateur | Points |
|---|---|
| ×0 | 0 |
| ×1 | +10 |
| ×2 | +20 |
| ×3 | +30 |

20 correspond au modificateur d'un bon combattant (Force 15 à 17). Plus le multiplicateur est élevé, plus les dégâts de base sont bas : à modificateur moyen, l'arme retrouve ses dégâts d'origine ; un personnage plus fort frappe plus dur, un plus faible moins.

### Portée (une arme paie chacune de ses portées)

Une arme frappe au contact, se lance à la main ou tire un projectile ; certaines cumulent (la dague se lance ET frappe au contact). Chaque portée donne une distance courte (pleine efficacité) et une distance longue, qui est la portée **maximale** : au-delà, l'arme n'atteint pas. Aucune portée n'est illimitée.

**Mêlée / contact.** L'arme frappe au contact, à portée de bras. Cette portée coûte +10 points.

**Portée de lancer** (arme projetée à la main) :

| Palier | Courte / longue max | Points |
|---|---|---|
| Lancer courte | 10 / 20 m | +10 |
| Lancer longue | 40 / 80 m | +20 |

**Portée de tir** (projectile mécanique ou arme à feu) :

| Palier | Courte / longue max | Points |
|---|---|---|
| Tir courte | 10 / 40 m | +20 |
| Tir moyenne | 30 / 90 m | +30 |
| Tir longue | 40 / 180 m | +40 |
| Tir très longue | 90 / 360 m | +50 |

L'allonge n'est pas une portée : c'est une propriété (+20). Pour les explosifs de zone, la portée est la distance de lancer/tir ; le rayon figure dans Zone. La distance longue est un plafond ferme : **80 m** pour un lancer, **360 m** pour un tir.

### Compatibilité arts martiaux (AM)

L'AM n'indique pas *combien* d'arts martiaux savent employer l'arme, mais jusqu'à quel **palier** on peut les pratiquer avec elle (les arts martiaux montent en trois paliers : Basique, Avancé, Expert). Plus l'arme prolonge le corps entraîné, plus le palier atteignable est haut.

| AM | Palier d'arts martiaux atteignable | Points |
|---|---|---|
| ✧✧✧ | Aucun | 0 |
| ✦✧✧ | Basique | +10 |
| ✦✦✧ | Avancé | +20 |
| ✦✦✦ | Expert | +30 |

- ✦✦✦ (jusqu'au palier Expert) : extensions du corps entraîné (bâton, nunchaku, kama, sai, fouet, chaîne, griffes, poing renforcé, éventail, katar)
- ✦✦✧ (jusqu'à Avancé) : armes à art de combat dédié (toutes les épées, sabre, rapière, lance, hallebarde, glaive, trident, dague)
- ✦✧✧ (Basique seul) : armes d'impact ou peu techniques (haches, masses, marteaux, fléau, pique, et le macuahuitl, qui est une massue tranchante d'impact et non une lame d'estoc) et armes à tension corporelle (arcs y compris à poulies, fronde, armes de jet)
- ✧✧✧ (aucun palier) : armes à gâchette ou purement mécaniques, sans technique du corps (arbalètes, armes à feu, explosifs, taser, lanceurs). *Aucune arme de mêlée n'est AM ✧✧✧.*

<div class="span" markdown>

### Propriétés bonus

| Points | Propriétés |
|---|---|
| +10 | Saisie · Dissimulable · Retour · Dégainage instantané · Poussée · Éraflure · Aggravation · Finesse · Parade · Précise · Déchirante · Jumelable · Désarmement |
| +20 | Renversement · Allonge ×2 · Mains libres · Assommement |
| +30 | Indésarmable · Allonge ×3 · Immobilisation à distance · Aveuglement de zone |
| +40 | Allonge ×4 · Décharge incapacitante |

Zone et Cône se paient par palier de taille (liste fermée, plafond +50) :

| Zone (rayon) | 3 m | 5 m | 10 m | 20 m |
|---|:---:|:---:|:---:|:---:|
| Points | +20 | +30 | +40 | +50 |

| Cône (longueur, 45°) | 5 m | 10 m | 15 m | 20 m |
|---|:---:|:---:|:---:|:---:|
| Points | +20 | +30 | +40 | +50 |

Un cône à 90° monte d'un palier. *Tir soutenu* (tir automatique qui arrose un cône, réservé aux armes à rafale) se paie au palier du cône arrosé.

*Perce-armure* (fusion de l'ancien Perce-blindage) se paie par palier selon la part de réduction de dégâts ignorée : ignore 20 (+10), 40 (+20), 60 (+30), 80 (+40), 100 (+50). Aux paliers hauts, elle défonce les blindages, véhicules et structures.

*Vitesse du son* (+20) : le projectile atteint ou dépasse la vitesse du son ; la cible qui tente de l'esquiver ou de le parer subit −40 à son jet de défense. Réservée aux armes à haute vélocité (canon rayé : fusils et carabines).

### Contraintes

| Points | Contraintes |
|---|---|
| −10 | Lourde · Rechargement lent · Bruyante |
| −20 | Très lourde · Surchauffe · Sensible à l'humidité |
| −30 | Extrêmement lourde · Arme lente |
| −40 | Usage unique |

*Lourdeur (prérequis de Force)* : *Lourde* (−10), *Très lourde* (−20) et *Extrêmement lourde* (−30) imposent une Force minimale pour manier l'arme (FOR 5, 7, 9). En dessous, le porteur subit −20 à l'attaque par point de Force manquant.

*Inefficace de près* : dans la bande de distance indiquée, l'arme est hors de son domaine et le porteur subit un malus de −40 à l'attaque. Le coût de la contrainte reprend la valeur de cette bande au barème des portées : au contact −10, courte −20, moyenne −30, longue −40.

</div>

### Munitions (tirs avant recharge)

La capacité s'exprime en **tirs avant recharge**, pas en balles : ce qui compte, c'est le nombre d'attaques qu'on enchaîne avant de recharger. Une arme à rafale consomme plusieurs munitions par tir, donc se vide plus vite — « Munitions (10 tirs, rafale de 3) » tient 10 attaques pour 30 balles. Recharger coûte une action, ou tout le tour avec *Rechargement lent*.

Plus une arme enchaîne de tirs, plus c'est un avantage, donc plus ça **coûte de points** (moins de dégâts) : le mono-coup, qui recharge à chaque attaque, ne coûte rien et frappe le plus fort ; le grand chargeur paie sa constance.

| Tirs avant recharge | 1 | 2 | 4 | 6 | 10 | 15 | 20 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Coût | 0 | 0 | +10 | +20 | +30 | +40 | +50 |

- Le **tir automatique** (*Tir soutenu*) est réservé aux armes à **rafale** (conso ≥ 2 munitions par tir) : impossible sur une arme coup par coup.
- Une recharge qui prend plus d'une action ajoute *Rechargement lent* (−10) : c'est là que se paie la lenteur d'un mousquet ou d'une arbalète lourde.
- Les consommables non rechargeables, comme la grenade ou la charge, portent la contrainte *Usage unique* (−40).
- Cette table remplace les anciens termes éparpillés (*Chargement*, *Petit chargeur*, *5 utilisations*) pour tout ce qui touche à la capacité.

### Illégalité (linéaire, −20 par étoile)

| Illégalité | Statut | Points |
|---|---|---|
| ☆☆☆☆☆ | Autorisée partout | 0 |
| ★☆☆☆☆ | Restrictions de port mineures | −20 |
| ★★☆☆☆ | Interdite dans plusieurs pays / permis | −40 |
| ★★★☆☆ | Interdite dans la plupart des pays | −60 |
| ★★★★☆ | Réservée militaire/police | −80 |
| ★★★★★ | Interdite partout aux civils | −100 |

Calcul mental : étoiles × 20. Cohérence : ☆☆☆☆☆ outils/sport et primitifs (arcs, fronde, boomerang) · ★☆☆☆☆ armes blanches, anciennes et à poudre noire (dague, épées, haches, fléau, arbalètes, mousquet, tromblon) · ★★☆☆☆ exotiques bridées (nunchaku, sai, griffes, poing américain, taser, fusils de chasse) · ★★★☆☆ armes de poing · ★★★★☆ fusils militaires semi-automatiques et pistolets-mitrailleurs · ★★★★★ armes à tir automatique (rafale), anti-matériel, mitrailleuse, lance-flammes et autres armes d'aire, explosifs. Critère net : le **tir automatique d'une arme d'épaule** (fusil d'assaut, mitrailleuse) fait passer à ★★★★★ ; les **automatiques compacts tenus à la main** (pistolet-mitrailleur) et les armes longues militaires semi-automatiques restent à ★★★★☆.

### Créer une nouvelle arme

1. Concept, illégalité (★), compatibilité AM
2. Dégâts affichés (20 de base + achetés, ≤ 200) et multiplicateur du modificateur (×0 à ×3, +10 par niveau)
3. Portée(s) : chacune se paie
4. Combler l'écart avec 1 à 4 propriétés fortes ; ajouter des contraintes si l'arme dépasse 100
5. Tout est en multiples de 10 : le total tombe juste

**Exemple, Dague (★☆☆☆☆, AM ✦✦✧, 30 dégâts affichés = 20 de base + 10 achetés)** : 10 (dégâts au-dessus de 20) + 10 (mêlée) + 10 (jet 10/20 m) + 20 (AM ✦✦✧) + 20 (×1 FOR) + 10 (Finesse) + 10 (Dissimulable) + 10 (Parade) + 10 (Dégainage instantané) + 10 (Jumelable) − 20 (★☆☆☆☆) = **100**

**Exemple, Fusil anti-matériel (★★★★★, AM ✧✧✧, 200 dégâts)** : 180 (dégâts au-dessus de 20) + 50 (tir très longue) − 10 (2 mains) + 50 (Perce-armure, ignore 100) + 10 (Précise) + 10 (Déchirante) + 10 (Aggravation) − 30 (Extrêmement lourde) − 30 (Arme lente) − 20 (Inefficace de près courte) − 10 (Rechargement lent) − 10 (Bruyante) − 100 (★★★★★) = **100**

### Repères de l'échelle

- 30 à 90 : corps à corps (20 de base gratuits + dégâts achetés ; le modificateur ×N s'ajoute en jeu)
- 60 à 90 : armes de jet et arcs
- 90 à 200 : armes mécaniques et à feu (à un coup = frappe forte, à chargeur = plus faible)
- 200 : le plafond de dégâts affichés, atteint par le lance-roquettes, l'anti-matériel, la mitrailleuse, le fusil de précision, la grenade et le lance-grenades. Ce plafond correspond à 180 points de dégâts achetés plus 20 de base.

### Notes d'équilibrage

- Chaque arme vaut 100 points exactement
- Modificateur de dégâts : le corps à corps ajoute ×N le modificateur de Force (Dextérité pour les Finesse), +10 points par niveau, ce qui laisse plus de place aux propriétés sur les armes de mêlée ; les armes à distance mécaniques sont en ×0
- Plafond de dégâts affiché 200 (180 en points + 20 de base gratuits) : atteint par le lance-roquettes, le fusil anti-matériel, la mitrailleuse légère, le fusil de précision et les explosifs de jet
- Propriétés et contraintes « grosses » (multiples de 10, de 10 à 50) : peu de traits par arme. Pour réduire encore le nombre de lignes d'une arme, on augmente la valeur unitaire des traits ; pour en mettre davantage, on la baisse
- Plus aucune mécanique économique (coût, rareté des munitions) ; maîtrises fondues dans les propriétés ; dégâts sans jet de dé ; armes solo
- Munitions = réservoir exprimé en **tirs avant recharge** (capacité ÷ conso par attaque) ; le coût monte avec le nombre de tirs (0 au mono-coup, jusqu'à +50), donc le petit chargeur frappe plus fort. Les arcs et frondes n'ont pas de réservoir ; grenade et charge restent en *Usage unique*.

</div>
