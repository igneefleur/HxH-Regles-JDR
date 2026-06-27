# -*- coding: utf-8 -*-
"""Ajoute le glossaire des propriétés à la fin de armes.md.
Démote les titres d'un cran (le glossaire passe sous le H1 « # Armes ») et
remplace les tirets cadratins « — » par « : » (règle du livre).
Usage : python scripts/patch_glossaire.py"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

GLOSSAIRE = r"""# Glossaire des propriétés d'armes

Règle exacte de chaque propriété du tableau d'armes.

## Rappel du modèle de combat

- 1 tour par round. Actions actives = (MOD AGI + MOD DEX) / 10, arrondi à l'inférieur, **min 1, max 10**.
- On ne peut pas faire **deux fois le même type d'action** (sauf modules de combat, à venir).
- **Attaque** : COMP ATTAQUE + MOD DEX + d100, contre **défense** (réaction gratuite et illimitée) : esquive (COMP ESQUIVE + MOD AGI + d100) ou parade (COMP PARADE + MOD DEX + d100).
- **Marge** = total attaque − total défense, arrondie à la dizaine inférieure → c'est le **% de touche**.
    - ≥ 200 → plafonné à 200 % (×2) · 10 à 200 → ce % · 0 à 9 → touche mais 0 dégât · < 0 → raté.
- **Dégâts infligés = (Dégâts de base − Réduction de Dégât) × marge %**. La RD se retire avant le multiplicateur.

## Propriétés validées

### Légère (+10)
Une fois par tour, le porteur peut effectuer **une attaque avec une autre arme légère sans consommer d'action**. Cette attaque suit la procédure normale (jet d'attaque, défense adverse). Nécessite donc une seconde arme possédant aussi *Légère*.

### Dégainage instantané (+10)
Dégainer une arme coûte **normalement une action**. Avec *Dégainage instantané*, le dégainage est **compris dans l'action d'attaque** : on peut sortir l'arme et frapper dans le même geste, sans dépenser d'action séparée.

### Retour (+10)
Après un lancer, l'arme **revient à la main du lanceur à la fin de son tour**. Permet de relancer la même arme au tour suivant sans la récupérer manuellement.

### Éraflure (+10)
**+10 points de touche** (la marge), mais **uniquement si la touche sans le bonus est ≤ 90 %** (90 % compris). Exemples : une touche à 90 % passe à 100 % ; une touche à 0 % (marge 0–9, normalement 0 dégât) passe à 10 % : la lame mord toujours un peu. Un coup déjà à 100 % ou plus n'en profite pas.

### Aggravation (+10)
**+10 points de touche**, mais **uniquement si la touche sans le bonus est ≥ 100 %** (100 % compris). Récompense les coups déjà excellents : un 150 % devient 160 %. Reste plafonné à **200 %** (un 200 % ne gagne rien).

*Éraflure et Aggravation se complètent exactement au seuil 90 / 100 : comme les marges s'arrondissent à la dizaine, il n'existe pas de valeur intermédiaire, donc aucun recouvrement.*

### Poussée (+10)
Sur une touche infligeant des dégâts, la cible est repoussée en ligne droite d'une distance **égale aux dégâts finaux infligés**. Un coup plus fort projette plus loin.

### Renversement (+10)
**Dès que l'attaque touche** (toute touche réussie, même à 0 %), la cible est mise **à terre**. Se relever coûte 1 action ; tant qu'elle est au sol, ses défenses sont pénalisées.

### Assommement (+10)
**Dès que l'attaque touche**, la cible est étourdie et **perd 1 action active** à son prochain tour (minimum 0).

### Ralentissement (+10)
**Dès que l'attaque touche**, le **déplacement** de la cible est réduit de moitié à son prochain tour.

*Renversement, Assommement et Ralentissement se déclenchent sur n'importe quelle touche, pas au seuil de 100 %, car une marge ≥ 100 % est rarissime quand attaque et défense s'équilibrent.*

### Mains libres (+20)
L'arme s'utilise en gardant les **deux mains libres** (griffes, arme intégrée au gant). Le porteur peut grimper, manipuler un objet ou utiliser une autre arme en même temps.

### Dissimulable (+20)
Facile à cacher sur soi. Passe une **fouille sommaire** et le port discret en public ; ne se remarque pas tant qu'elle n'est pas dégainée.

### Allonge (+20)
Frappe à une **portée de mêlée supérieure** (≈ 2–3 m). Permet d'engager une cible avant le contact et de frapper par-dessus un allié.

### Polyvalente (+20)
S'utilise à une ou deux mains. On compte les **dégâts à une main** (valeur de gauche) ; à deux mains, les dégâts passent à la **valeur entre parenthèses**.

### Contourne un abri (+10)
Frappe une cible derrière une **couverture partielle** : la cible perd le bénéfice défensif d'un abri léger contre cette attaque.

### Tir en cloche (+10)
Trajectoire haute par-dessus un obstacle. Atteint une cible **hors de la ligne de vue directe** (derrière un muret, dans une tranchée).

### Indésarmable (+10)
L'arme ne peut **pas être désarmée** (fixée, intégrée, sanglée). Immunise contre *Désarmement*.

### Incendiaire (+20)
La cible et le terrain inflammable **prennent feu** : dégâts de feu récurrents chaque tour jusqu'à extinction (une action pour s'éteindre ou se rouler au sol).

### Persistant (+20)
L'effet de zone **reste actif plusieurs tours** sur la zone touchée ; quiconque y entre ou y demeure le subit.

### Harcèlement (+20)
Frappe vive et gênante : sur une touche, la cible subit **−10 à son prochain jet** (attaque ou défense), déstabilisée.

### Désarmement (+20)
Sur une touche, au choix, le porteur fait **lâcher son arme** à la cible au lieu d'infliger les dégâts. Sans effet sur une cible *Indésarmable*.

### Saisie à distance (+20)
Sur une touche, la cible est **agrippée à distance** (par une chaîne, un fouet lesté…) : tant que le porteur maintient la prise, la cible ne peut pas se déplacer et subit un malus. Elle se libère en consacrant une action (jet opposé).

### Maintient sans jet (+20)
Une cible déjà entravée ou saisie le **reste sans nouveau jet** : pas besoin de réussir un jet à chaque tour pour la maintenir (l'entrave tient d'elle-même).

### Surprise (+20)
Quand l'adversaire est **surpris** (attaque depuis une position non repérée, embuscade), le porteur gagne **+40 à son jet d'attaque** sur ce coup. Sans effet dès que la cible est consciente du danger.

### Perce-armure (+30)
L'attaque **ignore la RD des armures souples** (tissu, cuir, kevlar, rembourrage) : contre une cible en armure souple, on calcule les dégâts comme si elle n'en portait pas. Sans effet sur une armure rigide/lourde.

### Perce-blindage (+30)
L'attaque **ignore la RD des armures lourdes** (plaque, blindage rigide, véhicules, structures) et, étant la version supérieure, aussi des souples. Défonce ce qui arrête tout le reste.

### Réduit au silence (+20)
Tant que l'effet dure, la cible **ne peut plus parler ni crier** : impossible d'appeler à l'aide, de donner un ordre ou de prononcer une incantation. (Garrot qui comprime la gorge, prise étouffante.)

### Double mode (+10)
L'arme possède **deux modes d'emploi distincts** (ex. lame tranchante / chaîne de contrôle). On choisit le mode à chaque attaque.

### Portée doublée (+20)
**Double les deux distances** de l'arme (courte et longue). La variante *via propulseur* exige l'accessoire dédié (atlatl, fronde à bâton) pour fonctionner.

## Propriétés supprimées

Retirées du système car sans intérêt mécanique ou ne devant pas constituer un avantage :

- **Sans Force requise** — un prérequis de Force absent ne doit pas être un bonus.
- **Fiable** — supprimée (l'absence d'incident est l'état par défaut ; l'inverse est la contrainte *Enrayage possible*).
- **Robuste** — supprimée.
- **Improvisable** — supprimée (effet purement narratif).
- **Réutilisable** — supprimée (on ne garde que le statut *consommable* via *Usage unique*).
- **+20 dégâts conditionnels** (et variantes *vs armures lourdes*, *vs cibles non armurées*, *aux dégâts à mains nues*) — supprimées au profit d'*Éraflure* / *Aggravation*, qui agissent sur la marge plutôt que sur la Base.
- **Utilisable monté · Mains semi-libres · Paire · Bonus escalade · Bonus mains nues** — supprimées (effets trop situationnels ou marginaux).
- **Dissimulable totale** — redondante avec *Dissimulable* ; les armes concernées utilisent désormais *Dissimulable* simple.
- **Discrète totale · Silencieuse** — le **silence est l'état par défaut** ; seul le bruit est pénalisé (contrainte *Bruyante*).
- **Non-létal au choix · Non-létal garanti** — tout le monde peut choisir de ne pas tuer ; ce n'est pas un avantage.
- **Entaille** — supprimée (équivalente à *Aggravation*).
- **Crochetage** — supprimée (équivalente à *Renversement* / mettre à terre) ; la *Hallebarde* utilise *Renversement*.
- **Crochetage d'arme** — supprimée (équivalente à *Désarmement*) ; la *Faucille* utilise *Désarmement*.
- **Liaison** — supprimée (n'était qu'une *Allonge*) ; les *Crochets chinois* utilisent *Allonge*.
- **Défensive · Blocage · Bonus de défense conservé** — supprimées : la valeur défensive (boucliers, armes de parade) relèvera des règles d'armure/équipement, pas du tableau d'armes.
- **Contre-charge** — supprimée ; la *Lance* devient *Polyvalente*.
- **Désarmement supérieur** — supprimée (le *Désarmement* simple suffit) ; le *Sai/Jutte* utilise *Désarmement*.
- **Ignore les boucliers · Contourne la parade** — supprimées ; le *Fléau d'armes* devient une frappe brute (120 de dégâts).
- **Insoupçonnable** — supprimée (redondante avec *Surprise*).
- **Ignore l'armure souple** — supprimée (c'était *Perce-armure*) ; le *Taser* utilise *Perce-armure*.
- **Couverture vs projectiles** — supprimée (défensive ; relève des règles d'équipement).
- **Légale / discrète socialement** — supprimée (doublon avec le système d'étoiles) ; la *Carabine civile* est rééquilibrée.
- **Mise à mort silencieuse** — renommée **Réduit au silence** (effet recentré : empêcher la cible de parler/crier).
"""

# Démotion des titres d'un cran (# -> ##, ## -> ###, ### -> ####).
g = re.sub(r"(?m)^#", "##", GLOSSAIRE)
# Tirets cadratins -> deux-points (règle du livre).
g = g.replace(" — ", " : ")
assert "—" not in g, "tiret cadratin résiduel"

P = Path("docs/content/livre/armes.md")
text = P.read_text(encoding="utf-8")
if "Glossaire des propriétés d'armes" not in text:
    text = text.rstrip() + "\n\n---\n\n" + g.strip() + "\n"
    P.write_text(text, encoding="utf-8")
    print("OK - glossaire ajouté")
else:
    print("Glossaire déjà présent, rien fait")
