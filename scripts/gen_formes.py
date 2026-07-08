# -*- coding: utf-8 -*-
# Source unique de la page « Formes du vivant » (docs/content/regles/monde/formes.md).
# Lancer depuis la racine du dépôt : `python scripts/gen_formes.py` (met PYTHONIOENCODING=utf-8).
# Les 5 tableaux (bio, membres, caractéristiques, sens externes, sens internes) sont tous
# dérivés de `forms` + SENS_EXT + SENS_INT + BIO ci-dessous. L'ordre d'affichage = l'ordre de `forms`.
# La fiche « Métamorphose » de docs/content/regles/nen/transmutation.md reprend les mêmes 22 formes,
# dans le MÊME ordre, tenue à jour à la main (voir la convention de nommage en mémoire).
import io, os
M = "−"  # minus typographique
# name, [Tête,Patte,Bras,Aile,Nageoire,Tentacule,Pince,Trompe,Queue], exemples, [FOR,DEX,AGI,END,PER,PRE]
forms = [
 ("Bipède à bras", [1,2,2,0,0,0,0,0,0], "humain, grand singe", [0,0,0,0,0,0]),
 ("Bipède à bras et queue", [1,2,2,0,0,0,0,0,1], "kangourou, théropode", [2,-1,1,1,0,1]),
 ("Bipède à deux ailes", [1,2,0,2,0,0,0,0,1], "oiseau, chauve-souris", [-1,-2,3,-1,2,2]),
 ("Quadrupède", [1,4,0,0,0,0,0,0,0], "grenouille", [1,-3,2,2,0,-1]),
 ("Quadrupède à queue", [1,4,0,0,0,0,0,0,1], "chien, lézard, dinosaure quadrupède", [2,-3,2,1,1,0]),
 ("Quadrupède à trompe", [1,4,0,0,0,0,0,1,1], "tapir, éléphant", [2,-1,0,1,1,1]),
 ("Vermiforme", [1,0,0,0,0,0,0,0,0], "ver, serpent", [1,-3,1,2,-1,0]),
 ("Nageur à deux nageoires", [1,0,0,0,2,0,0,0,1], "baleine, dauphin", [1,-4,1,2,2,-1]),
 ("Nageur à quatre nageoires", [1,0,0,0,4,0,0,0,1], "poisson, tortue marine", [0,-4,2,2,2,-1]),
 ("Hexapode", [1,6,0,0,0,0,0,0,0], "fourmi, puce", [1,-2,2,2,1,-2]),
 ("Hexapode à deux ailes", [1,6,0,2,0,0,0,0,0], "mouche, moustique", [0,-2,4,1,2,-2]),
 ("Hexapode à quatre ailes", [1,6,0,4,0,0,0,0,0], "papillon, libellule", [0,-2,4,2,2,-2]),
 ("Octopode", [1,8,0,0,0,0,0,0,0], "araignée", [0,-2,2,3,1,-1]),
 ("Octopode à pinces", [1,8,0,0,0,0,2,0,0], "crabe", [2,-2,1,3,1,-1]),
 ("Octopode à pinces et queue", [1,8,0,0,0,0,2,0,1], "scorpion, homard", [3,-2,0,3,1,0]),
 ("Décapode à queue", [1,10,0,0,0,0,0,0,1], "crevette, limule", [1,-2,1,3,1,-2]),
 ("Myriapode", [1,"≥ 10",0,0,0,0,0,0,0], "mille-pattes, scolopendre", [1,-3,0,3,0,0]),
 ("Céphalopode à huit tentacules", [1,0,0,0,0,8,0,0,0], "pieuvre", [2,3,2,-1,2,0]),
 ("Céphalopode à dix tentacules", [1,0,0,0,0,10,0,0,0], "calmar, seiche", [2,2,3,-1,2,0]),
 ("Radiaire à tentacules", [0,0,0,0,0,8,0,0,0], "méduse, anémone", [-3,-4,-2,2,-2,-2]),
 ("Radiaire à cinq bras", [0,0,5,0,0,0,0,0,0], "étoile de mer", [-2,-3,-3,3,-2,-3]),
 ("Informe", [0,0,0,0,0,0,0,0,0], "éponge", [-4,-4,-4,4,-4,-4]),
]

SENS_EXT = {
    'Bipède à bras': ('Vue', 'Ouïe, Toucher', 'Odorat, Goût, Chémesthésie, Thermoception, Séismoréception', 'Magnétoréception, Écholocation, Vision polarisée, Vision ultraviolette, Infrasons & ultrasons', 'Électroréception, Détection infrarouge, Ligne latérale, Hygroréception'),
    'Bipède à bras et queue': ('Vue', 'Ouïe, Toucher', 'Odorat, Goût, Chémesthésie, Thermoception, Séismoréception', 'Magnétoréception, Écholocation, Vision polarisée, Vision ultraviolette, Infrasons & ultrasons', 'Électroréception, Détection infrarouge, Ligne latérale, Hygroréception'),
    'Quadrupède à queue': ('Vue', 'Ouïe, Toucher', 'Odorat, Goût, Chémesthésie, Thermoception, Séismoréception, Infrasons & ultrasons', 'Magnétoréception, Écholocation, Vision polarisée, Vision ultraviolette', 'Électroréception, Détection infrarouge, Ligne latérale, Hygroréception'),
    'Quadrupède': ('Vue', 'Ouïe, Toucher', 'Odorat, Goût, Chémesthésie, Thermoception, Séismoréception, Hygroréception', 'Magnétoréception, Vision polarisée, Vision ultraviolette, Infrasons & ultrasons, Ligne latérale', 'Électroréception, Détection infrarouge, Écholocation'),
    'Vermiforme': ('Toucher', 'Séismoréception', 'Odorat, Goût, Chémesthésie, Thermoception, Hygroréception', 'Vue, Ouïe, Magnétoréception, Vision polarisée, Vision ultraviolette, Infrasons & ultrasons, Détection infrarouge', 'Écholocation, Électroréception, Ligne latérale'),
    'Bipède à deux ailes': ('Vue', 'Ouïe, Toucher, Magnétoréception, Écholocation', 'Odorat, Goût, Chémesthésie, Thermoception, Séismoréception, Vision polarisée, Vision ultraviolette, Infrasons & ultrasons', 'Hygroréception', 'Électroréception, Détection infrarouge, Ligne latérale'),
    'Quadrupède à trompe': ('Vue', 'Ouïe, Toucher, Séismoréception, Infrasons & ultrasons', 'Odorat, Goût, Chémesthésie, Thermoception', 'Magnétoréception, Écholocation, Vision polarisée, Vision ultraviolette, Hygroréception', 'Électroréception, Détection infrarouge, Ligne latérale'),
    'Nageur à deux nageoires': ('Écholocation', 'Vue, Ouïe, Infrasons & ultrasons', 'Toucher, Goût, Chémesthésie, Thermoception, Magnétoréception', 'Odorat, Séismoréception, Vision polarisée, Vision ultraviolette', 'Électroréception, Détection infrarouge, Ligne latérale, Hygroréception'),
    'Nageur à quatre nageoires': ('Vue', 'Ouïe, Ligne latérale, Électroréception', 'Toucher, Odorat, Goût, Chémesthésie, Thermoception, Magnétoréception, Vision polarisée, Vision ultraviolette', 'Séismoréception, Infrasons & ultrasons', 'Écholocation, Détection infrarouge, Hygroréception'),
    'Hexapode': ('Vue', 'Toucher, Odorat, Vision polarisée', 'Goût, Chémesthésie, Thermoception, Séismoréception, Vision ultraviolette, Hygroréception', 'Ouïe, Magnétoréception, Infrasons & ultrasons, Électroréception', 'Écholocation, Détection infrarouge, Ligne latérale'),
    'Hexapode à quatre ailes': ('Vue', 'Toucher, Odorat, Vision polarisée', 'Ouïe, Goût, Chémesthésie, Thermoception, Séismoréception, Magnétoréception, Vision ultraviolette, Infrasons & ultrasons, Hygroréception', 'Électroréception, Détection infrarouge', 'Écholocation, Ligne latérale'),
    'Hexapode à deux ailes': ('Vue', 'Toucher, Odorat, Thermoception', 'Ouïe, Goût, Chémesthésie, Séismoréception, Vision polarisée, Vision ultraviolette, Détection infrarouge, Hygroréception', 'Magnétoréception, Infrasons & ultrasons, Électroréception', 'Écholocation, Ligne latérale'),
    'Octopode': ('Toucher', 'Vue, Séismoréception', 'Odorat, Goût, Chémesthésie, Thermoception, Vision polarisée, Vision ultraviolette, Hygroréception', 'Ouïe, Magnétoréception, Infrasons & ultrasons, Électroréception', 'Écholocation, Détection infrarouge, Ligne latérale'),
    'Décapode à queue': ('Vue', 'Toucher, Odorat', 'Goût, Chémesthésie, Thermoception, Séismoréception, Vision polarisée, Vision ultraviolette', 'Ouïe, Magnétoréception, Infrasons & ultrasons', 'Écholocation, Électroréception, Détection infrarouge, Ligne latérale, Hygroréception'),
    'Octopode à pinces': ('Vue', 'Toucher, Odorat', 'Goût, Chémesthésie, Thermoception, Séismoréception, Vision polarisée', 'Ouïe, Magnétoréception, Vision ultraviolette, Infrasons & ultrasons, Hygroréception', 'Écholocation, Électroréception, Détection infrarouge, Ligne latérale'),
    'Octopode à pinces et queue': ('Toucher', 'Séismoréception', 'Vue, Odorat, Goût, Chémesthésie, Thermoception, Hygroréception', 'Ouïe, Magnétoréception, Vision polarisée, Vision ultraviolette, Infrasons & ultrasons', 'Écholocation, Électroréception, Détection infrarouge, Ligne latérale'),
    'Myriapode': ('Toucher', 'Odorat, Séismoréception', 'Goût, Chémesthésie, Thermoception, Hygroréception', 'Vue, Ouïe, Magnétoréception, Vision polarisée, Vision ultraviolette, Infrasons & ultrasons', 'Écholocation, Électroréception, Détection infrarouge, Ligne latérale'),
    'Céphalopode à huit tentacules': ('Vue', 'Toucher, Ligne latérale, Vision polarisée', 'Odorat, Goût, Chémesthésie, Thermoception', 'Séismoréception, Magnétoréception, Vision ultraviolette, Infrasons & ultrasons, Ouïe', 'Écholocation, Électroréception, Détection infrarouge, Hygroréception'),
    'Céphalopode à dix tentacules': ('Vue', 'Toucher, Vision polarisée, Ligne latérale', 'Odorat, Goût, Chémesthésie, Thermoception, Séismoréception', 'Ouïe, Magnétoréception, Vision ultraviolette, Infrasons & ultrasons', 'Écholocation, Électroréception, Détection infrarouge, Hygroréception'),
    'Radiaire à tentacules': ('Toucher', 'Séismoréception', 'Odorat, Goût, Chémesthésie, Thermoception', 'Vue', 'Ouïe, Magnétoréception, Écholocation, Vision polarisée, Vision ultraviolette, Infrasons & ultrasons, Électroréception, Détection infrarouge, Ligne latérale, Hygroréception'),
    'Radiaire à cinq bras': ('Toucher', 'Vue, Odorat', 'Goût, Chémesthésie, Thermoception, Séismoréception', 'Magnétoréception, Vision polarisée, Vision ultraviolette', 'Ouïe, Écholocation, Infrasons & ultrasons, Électroréception, Détection infrarouge, Ligne latérale, Hygroréception'),
    'Informe': ('Toucher', 'Chémesthésie', 'Odorat, Goût', 'Thermoception, Séismoréception', 'Vue, Ouïe, Magnétoréception, Écholocation, Vision polarisée, Vision ultraviolette, Infrasons & ultrasons, Électroréception, Détection infrarouge, Ligne latérale, Hygroréception'),
}
SENS_INT = {
    'Bipède à bras': ('Équilibrioception', 'Proprioception, Nociception', 'Intéroception, Chronoception', 'Baroréception', '—'),
    'Bipède à bras et queue': ('Équilibrioception', 'Proprioception, Nociception', 'Intéroception, Chronoception', 'Baroréception', '—'),
    'Quadrupède à queue': ('Équilibrioception', 'Proprioception, Nociception', 'Intéroception, Chronoception', 'Baroréception', '—'),
    'Quadrupède': ('Équilibrioception', 'Proprioception, Nociception', 'Intéroception, Chronoception', 'Baroréception', '—'),
    'Vermiforme': ('Équilibrioception', 'Proprioception, Nociception', 'Intéroception, Chronoception', 'Baroréception', '—'),
    'Bipède à deux ailes': ('Équilibrioception', 'Proprioception, Nociception', 'Intéroception, Chronoception, Baroréception', '—', '—'),
    'Quadrupède à trompe': ('Équilibrioception', 'Proprioception, Nociception', 'Intéroception, Chronoception', 'Baroréception', '—'),
    'Nageur à deux nageoires': ('Équilibrioception', 'Proprioception, Nociception', 'Intéroception, Chronoception, Baroréception', '—', '—'),
    'Nageur à quatre nageoires': ('Équilibrioception', 'Proprioception, Nociception', 'Intéroception, Chronoception, Baroréception', '—', '—'),
    'Hexapode': ('Équilibrioception', 'Proprioception, Nociception', 'Intéroception, Chronoception', 'Baroréception', '—'),
    'Hexapode à quatre ailes': ('Équilibrioception', 'Proprioception, Nociception', 'Intéroception, Chronoception', 'Baroréception', '—'),
    'Hexapode à deux ailes': ('Équilibrioception', 'Proprioception, Nociception', 'Intéroception, Chronoception', 'Baroréception', '—'),
    'Octopode': ('Équilibrioception', 'Proprioception, Nociception', 'Intéroception, Chronoception', 'Baroréception', '—'),
    'Décapode à queue': ('Équilibrioception', 'Proprioception, Nociception', 'Intéroception, Chronoception', 'Baroréception', '—'),
    'Octopode à pinces': ('Équilibrioception', 'Proprioception, Nociception', 'Intéroception, Chronoception', 'Baroréception', '—'),
    'Octopode à pinces et queue': ('Équilibrioception', 'Proprioception, Nociception', 'Intéroception, Chronoception', 'Baroréception', '—'),
    'Myriapode': ('Équilibrioception', 'Proprioception, Nociception', 'Intéroception, Chronoception', 'Baroréception', '—'),
    'Céphalopode à huit tentacules': ('Équilibrioception', 'Proprioception, Nociception', 'Intéroception, Chronoception, Baroréception', '—', '—'),
    'Céphalopode à dix tentacules': ('Équilibrioception', 'Proprioception, Nociception', 'Intéroception, Chronoception, Baroréception', '—', '—'),
    'Radiaire à tentacules': ('Équilibrioception', 'Nociception', 'Intéroception', 'Proprioception, Chronoception', 'Baroréception'),
    'Radiaire à cinq bras': ('Proprioception', 'Nociception, Équilibrioception', 'Intéroception', 'Chronoception', 'Baroréception'),
    'Informe': ('Intéroception', '—', '—', 'Chronoception', 'Équilibrioception, Proprioception, Nociception, Baroréception'),
}
# respiration, alimentation
BIO = {
    'Bipède à bras': ('air', 'omnivore'),
    'Bipède à bras et queue': ('air', 'herbivore ou carnivore'),
    'Quadrupède à queue': ('air', 'herbivore, carnivore ou omnivore'),
    'Quadrupède': ('air', 'carnivore'),
    'Vermiforme': ('air', 'détritivore ou carnivore'),
    'Bipède à deux ailes': ('air', 'herbivore, carnivore ou omnivore'),
    'Quadrupède à trompe': ('air', 'herbivore'),
    'Nageur à deux nageoires': ('air', 'carnivore ou filtreur'),
    'Nageur à quatre nageoires': ('air ou eau', 'herbivore, carnivore ou omnivore'),
    'Hexapode': ('air', 'omnivore ou carnivore'),
    'Hexapode à quatre ailes': ('air', 'herbivore ou carnivore'),
    'Hexapode à deux ailes': ('air', 'détritivore ou carnivore'),
    'Octopode': ('air', 'carnivore'),
    'Décapode à queue': ('eau', 'détritivore ou omnivore'),
    'Octopode à pinces': ('eau', 'omnivore ou détritivore'),
    'Octopode à pinces et queue': ('air ou eau', 'carnivore ou omnivore'),
    'Myriapode': ('air', 'détritivore ou carnivore'),
    'Céphalopode à huit tentacules': ('eau', 'carnivore'),
    'Céphalopode à dix tentacules': ('eau', 'carnivore'),
    'Radiaire à tentacules': ('eau', 'carnivore'),
    'Radiaire à cinq bras': ('eau', 'carnivore ou détritivore'),
    'Informe': ('eau', 'filtreur'),
}
# Propriété spéciale : un mode de nage propre qui dispense du malus de déplacement aquatique.
PROP = {
    'Vermiforme': 'Ondulation',
    'Céphalopode à huit tentacules': 'Propulsion à réaction',
    'Céphalopode à dix tentacules': 'Propulsion à réaction',
    'Radiaire à tentacules': 'Pulsation',
    'Radiaire à cinq bras': 'Podia',
}

def cell(v):
    return "" if (v == 0 or v is None or v == "") else str(v)
def car(v):
    return "0" if v == 0 else (("+" if v > 0 else M) + str(abs(v)))

L = []
def row(cells): L.append("| " + " | ".join(cells) + " |")
def sep(n): L.append("| " + " | ".join(["---"]*n) + " |")

L += ["# Formes du vivant", ""]
L += ["Une forme est le plan de corps d'un être : son inventaire de membres, et rien d'autre. Elle sert à bâtir une créature qui n'est pas humaine, qu'on la [conjure](../nen/conjuration.md), qu'on l'[émette](../nen/emission.md), qu'on la [manipule](../nen/manipulation.md) ou qu'on s'y remodèle par la [métamorphose](../nen/transmutation.md).", ""]
L += ["L'humain, le bipède à bras, sert de référence : ses caractéristiques physiques valent la moyenne, et tous les écarts se comptent à partir de lui. Ces écarts décrivent le plan de corps à taille comparable ; la taille propre de la créature se règle séparément.", ""]
L += ["Ce qu'une forme n'inclut pas se pose ailleurs : les cornes, dards et défenses sont des armes, la carapace et la coquille une armure, les antennes et les yeux servent les sens.", ""]

# 0. Identité / biologie (premier tableau)
L += ["### Les formes en bref", ""]
L += ["Chaque forme, ses animaux-types et sa biologie de base : le milieu où elle respire, son alimentation courante et, s'il y a lieu, une propriété spéciale qui touche son déplacement.", ""]
L += ['<div class="cj-modules anima formes bio" markdown>', ""]
hdrbio = ["Forme","Exemples","Respiration","Alimentation","Propriété spéciale"]
row(hdrbio); sep(len(hdrbio))
for name, mem, ex, cc in forms:
    r, a = BIO.get(name, ("—", "—"))
    row([name, ex, r, a, PROP.get(name, "—")])
L += ["", "</div>", ""]

L += ['<div class="defs" markdown>', ""]
L += ["**Herbivore :** se nourrit de végétaux : folivore (feuilles), frugivore (fruits), granivore (graines), nectarivore (nectar), palynivore (pollen), algivore (algues), xylophage (bois).", ""]
L += ["**Carnivore :** se nourrit d'animaux : insectivore (insectes), piscivore (poissons), hématophage (sang), ovivore (œufs), molluscivore (mollusques), vermivore (vers).", ""]
L += ["**Omnivore :** aussi bien végétal qu'animal.", ""]
L += ["**Détritivore :** matière organique morte : saprophage (débris en décomposition), nécrophage ou charognard (charognes), coprophage (excréments).", ""]
L += ["**Filtreur :** particules et plancton filtrés dans l'eau : planctonivore, microphage, suspensivore.", ""]
L += ["**Fongivore :** se nourrit de champignons, ni plante ni animal ; rare, aucune forme ci-dessus ne s'y limite.", ""]
L += ["**Mixotrophe :** complète son régime en cultivant des algues symbiotiques dans ses tissus, comme les coraux, les bénitiers ou certaines méduses.", ""]
L += ["</div>", ""]

L += ["Certaines formes portent une propriété spéciale qui leur tient lieu de nageoire : elles se déplacent dans l'eau à leur Agilité pleine, sans subir le malus de déplacement aquatique. Chaque légende précise aussi combien de membres cette nage occupe, car un membre qui propulse ne peut agir en même temps.", ""]
L += ['<div class="defs" markdown>', ""]
L += ["**Ondulation :** le corps allongé se propulse en ondulant d'un bout à l'autre, sans nageoire ; il n'a aucun membre à occuper.", ""]
L += ["**Propulsion à réaction :** la forme aspire l'eau dans son corps puis la chasse par un jet que son siphon oriente ; la poussée venant du corps, ses tentacules restent libres d'agir. En pleine fuite toutefois, à l'allure lourde, elle les plaque en fuseau derrière elle pour fendre l'eau, et ils cessent d'être libres.", ""]
L += ["**Pulsation :** la forme nage en contractant et relâchant tout son corps ; la poussée vient du corps, donc ses tentacules restent libres d'agir.", ""]
L += ["**Podia :** des centaines de petits pieds font ramper la forme sur le fond ; avancer occupe la moitié de ses bras, arrondie au supérieur, soit trois des cinq bras de l'étoile de mer, et laisse les autres libres.", ""]
L += ["</div>", ""]

# 1. Membres
L += ["### Les membres de chaque forme", ""]
L += ["Chaque forme porte une tête ou non, et des membres pris dans une palette : la patte ou la jambe, l'aile, la nageoire, le bras, le tentacule, la pince, la trompe, la queue.", ""]
L += ['<div class="cj-modules anima formes membres" markdown>', ""]
hdr = ["Forme","Tête","Patte / jambe","Bras","Aile","Nageoire","Tentacule","Pince","Trompe","Queue"]
row(hdr); sep(len(hdr))
for name, mem, ex, cc in forms:
    row([name] + [cell(x) for x in mem])
L += ["", "</div>", ""]

# 2. Caractéristiques
L += ["### Les caractéristiques de chaque forme", ""]
L += ["Le plan de corps hausse ou abaisse les six caractéristiques physiques. Les valeurs se comptent à partir de l'humain, à taille comparable ; un zéro signale une caractéristique identique à la sienne.", ""]
L += ['<div class="cj-modules anima formes carac" markdown>', ""]
hdr2 = ["Forme","FOR","DEX","AGI","END","PER","PRÉ"]
row(hdr2); sep(len(hdr2))
for name, mem, ex, cc in forms:
    row([name] + [car(x) for x in cc])
L += ["", "</div>", ""]

# 2b. Déplacement (règles ; les exceptions aquatiques sont portées par la colonne Propriété spéciale)
L += ["### Le déplacement", ""]
L += ["Une forme se déplace dans trois milieux : sur terre, dans l'eau et dans les airs. Sa vitesse se lit sur la table de mouvement des [capacités physiques](../personnage/capacites-physiques.md), à l'Agilité de la créature. Selon ses membres, un milieu lui est ouvert normalement, pénalisé ou fermé ; une pénalité retranche autant de paliers sur cette table, comme un terrain difficile.", ""]
L += ["Sans aile, une forme ne vole pas : le ciel lui est fermé. Sans patte ni jambe, elle rampe et lit sa vitesse terrestre quatre paliers plus bas. Sans nageoire, elle patauge et lit sa vitesse aquatique trois paliers plus bas, à moins qu'une propriété spéciale, portée par la dernière colonne du premier tableau, ne lui tienne lieu de nage.", ""]
L += ["Se déplacer occupe les membres qui portent et propulsent le corps ; les autres agissent librement. Sur pattes, les jambes avancent et les bras demeurent libres. Quand les mêmes membres portent et agissent, comme les bras d'une étoile de mer, la propriété spéciale de la forme dit combien il en faut pour avancer.", ""]
L += ['<div class="memo" markdown>', ""]
L += ["Pour mémoire, ces pénalités collent au réel pour une créature de taille et d'Agilité moyennes : ramper sans pattes ramène la course entre 1 et 6 km/h, comme un serpent, et nager sans nageoire entre un demi et deux mètres et demi par seconde, comme un humain.", ""]
L += ["</div>", ""]

# 3-4. Sens : matrices (formes en lignes, un sens par colonne, cases P/S/T/L/I)
EXT_ORDER = ['Vue','Ouïe','Toucher','Odorat','Goût','Chémesthésie','Thermoception','Séismoréception','Magnétoréception','Écholocation','Vision polarisée','Vision ultraviolette','Infrasons & ultrasons','Électroréception','Détection infrarouge','Ligne latérale','Hygroréception']
INT_ORDER = ['Équilibrioception','Proprioception','Nociception','Intéroception','Chronoception','Baroréception']
def invert(d, order, name):
    m = {}
    for ti, tierstr in enumerate(d[name]):
        for s in str(tierstr).split(','):
            s = s.strip()
            if s and s != '—': m[s] = "PSTLI"[ti]
    return [m.get(s, "?") for s in order]

LC = {'P':'p','S':'s','T':'t','L':'l','I':'i'}
def matrix(d, order, cls):
    out = ['<div class="cj-modules anima formes sens-grille %s">' % cls, '<table>']
    out.append('<thead><tr><th>Forme</th>' + ''.join('<th><span class="vh">%s</span></th>' % s for s in order) + '</tr></thead>')
    out.append('<tbody>')
    for name, mem, ex, cc in forms:
        tds = ''.join('<td class="%s">%s</td>' % (LC[l], '' if l == 'I' else l) for l in invert(d, order, name))
        out.append('<tr><td>%s</td>%s</tr>' % (name, tds))
    out += ['</tbody>', '</table>', '</div>']
    return out

L += ["### Les sens externes de chaque forme", ""]
L += ["Les sens externes mesurent le monde autour. Chaque colonne est l'un des dix-sept sens externes du livre ; la couleur d'une case donne le niveau du sens pour la forme, une case vide signalant un sens inexistant : P primaire, S secondaire, T tertiaire, L latent. L'humain y retrouve exactement la grille des [sens](../personnage/sens.md).", ""]
L += matrix(SENS_EXT, EXT_ORDER, "mat-ext")
L += [""]

L += ["### Les sens internes de chaque forme", ""]
L += ["Les sens internes mesurent l'état du corps même, avec la même notation (P, S, T, L ; case vide pour un sens inexistant).", ""]
L += matrix(SENS_INT, INT_ORDER, "mat-int")
L += [""]

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_OUT = os.path.join(_ROOT, "docs", "content", "regles", "monde", "formes.md")
io.open(_OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
print("written", len(forms), "forms | ext:", len(SENS_EXT), "| int:", len(SENS_INT), "->", _OUT)
