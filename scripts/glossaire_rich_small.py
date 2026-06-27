# -*- coding: utf-8 -*-
"""Passe toutes les cartes de poids < 100 t au format riche (2 paragraphes :
description + conversions + cube d'eau, puis « Concrètement » chiffré).
Usage : python scripts/glossaire_rich_small.py"""
import re, sys
sys.stdout.reconfigure(encoding="utf-8")
GLOSS = "docs/includes/glossaire.md"

NEW = {
    "moins d'1 kg": "Moins d'un kilogramme, à peine quelques centaines de grammes : le poids d'un téléphone, d'une pomme ou d'un petit livre. Moins d'un demi-litre d'eau, un cube d'environ huit centimètres de côté.\n\nConcrètement : on le tient au bout des doigts sans le remarquer ; il en faudrait plus de cent pour égaler un adulte.",
    "1 kg": "Un kilogramme, soit 1 000 grammes : une bouteille d'eau d'un litre, un paquet de sucre ou un petit ananas. C'est la masse de référence du système métrique, un cube d'eau de dix centimètres de côté.\n\nConcrètement : un litre d'eau exactement ; il en faudrait une soixantaine pour atteindre le poids d'un adulte.",
    "2 kg": "Deux kilogrammes, deux litres d'eau : un ordinateur portable, une grosse boîte de conserve ou un petit chat. Un cube d'eau d'environ treize centimètres de côté.\n\nConcrètement : deux bouteilles d'un litre, soit un trentième d'un adulte.",
    "3 kg": "Trois kilogrammes : un nouveau-né en bonne santé, un chat adulte ou un petit sac de pommes de terre. Trois litres d'eau, un cube de quatorze centimètres de côté.\n\nConcrètement : trois bouteilles d'un litre, soit un vingtième d'un adulte.",
    "5 kg": "Cinq kilogrammes : un haltère léger, un petit chien ou un sac de farine. Cinq litres d'eau, un cube de dix-sept centimètres de côté.\n\nConcrètement : cinq bouteilles d'un litre, soit un douzième d'un adulte ; ce qu'on porte sans y penser au bout du bras.",
    "8 kg": "Huit kilogrammes : une boule de bowling, un gros chat bien nourri ou un carton de bouteilles. Huit litres d'eau, un cube de vingt centimètres de côté.\n\nConcrètement : huit bouteilles d'un litre, soit un huitième d'un adulte.",
    "10 kg": "Dix kilogrammes : un sac de ciment, un pneu de voiture ou un chien moyen. Dix litres d'eau, un cube d'une vingtaine de centimètres de côté.\n\nConcrètement : dix bouteilles d'un litre, soit un sixième d'un adulte ; la charge d'un bagage cabine bien rempli.",
    "15 kg": "Quinze kilogrammes : une grosse valise pleine, un sac de plâtre ou un enfant de trois ans. Quinze litres d'eau, un cube de vingt-cinq centimètres de côté.\n\nConcrètement : quinze bouteilles d'un litre, soit le quart d'un adulte.",
    "20 kg": "Vingt kilogrammes : un enfant de six ans, un gros sac à dos de randonnée chargé ou deux packs d'eau. Vingt litres d'eau, un cube de vingt-sept centimètres de côté.\n\nConcrètement : vingt bouteilles d'un litre, soit près d'un tiers d'un adulte.",
    "30 kg": "Trente kilogrammes : un enfant de dix ans, un chien de grande taille ou un sac de ciment de chantier renforcé. Trente litres d'eau, un cube d'environ trente centimètres de côté.\n\nConcrètement : trente bouteilles d'un litre, soit la moitié d'un adulte.",
    "50 kg": "Cinquante kilogrammes, la moitié d'un quintal : une personne menue, un sac de plâtre professionnel ou un jeune veau. Cinquante litres d'eau, un cube de trente-sept centimètres de côté.\n\nConcrètement : cinquante bouteilles d'un litre, soit quatre cinquièmes d'un adulte moyen.",
    "60 kg": "Soixante kilogrammes : un adulte de corpulence moyenne, ou un grand chien de montagne. Soixante litres d'eau, un cube de trente-neuf centimètres de côté.\n\nConcrètement : soixante bouteilles d'un litre, soit le poids d'un adulte moyen.",
    "100 kg": "Cent kilogrammes, un quintal : un réfrigérateur plein, un grand gaillard musclé ou un cochon adulte. Cent litres d'eau, un cube de quarante-six centimètres de côté.\n\nConcrètement : cent bouteilles d'un litre, ou un adulte et demi ; c'est l'ordre du soulevé maximal d'un humain non entraîné.",
    "150 kg": "Cent cinquante kilogrammes : un panda géant, ou un motard avec sa moto légère. Cent cinquante litres d'eau, un cube d'environ cinquante-trois centimètres de côté.\n\nConcrètement : deux adultes et demi, ou cent cinquante bouteilles d'un litre.",
    "200 kg": "Deux cents kilogrammes : un lion mâle, un piano droit ou un tonneau de vin plein. Un cube d'eau de près de soixante centimètres de côté.\n\nConcrètement : trois adultes, ou deux cents bouteilles d'un litre.",
    "300 kg": "Trois cents kilogrammes : un ours brun, un piano à queue ou une jeune vache laitière. Un cube d'eau de soixante-sept centimètres de côté.\n\nConcrètement : près de cinq adultes, ou trois cents litres d'eau.",
    "500 kg": "Cinq cents kilogrammes, une demi-tonne : un cheval de selle, une vache adulte ou un piano à queue de concert. Un cube d'eau de quatre-vingts centimètres de côté.\n\nConcrètement : huit adultes, ou cinq cents litres d'eau ; c'est aussi l'ordre du record du monde de soulevé de terre.",
    "1 t": "Une tonne, soit 1 000 kg : une petite voiture citadine, un grand taureau, ou un mètre cube d'eau pure (un cube d'un mètre de côté).\n\nConcrètement : seize adultes, ou mille litres d'eau.",
    "2 t": "Deux tonnes : un gros SUV, un rhinocéros ou un hippopotame moyen. Deux mètres cubes d'eau, un cube d'environ 1,3 mètre de côté.\n\nConcrètement : une trentaine d'adultes, ou un peu plus d'une voiture.",
    "3 t": "Trois tonnes : un éléphant d'Asie, ou une camionnette utilitaire chargée. Trois mètres cubes d'eau, un cube de 1,4 mètre de côté.\n\nConcrètement : une cinquantaine d'adultes, ou deux voitures.",
    "5 t": "Cinq tonnes : un éléphant d'Afrique, un camion-benne à vide, ou un rocher d'un peu moins de deux mètres cubes. Un cube d'eau de 1,7 mètre de côté.\n\nConcrètement : quatre-vingts adultes, ou plus de trois voitures.",
    "6 t": "Six tonnes : un très grand éléphant de savane mâle, le plus lourd des animaux terrestres actuels, ou un autobus à vide. Un cube d'eau de 1,8 mètre de côté.\n\nConcrètement : une centaine d'adultes, quatre voitures, ou un gros éléphant.",
    "10 t": "Dix tonnes : un autobus, un camion-benne ou deux éléphants. Dix mètres cubes d'eau, un cube de plus de deux mètres de côté.\n\nConcrètement : cent soixante adultes, ou près de sept voitures.",
    "15 t": "Quinze tonnes : un semi-remorque à vide, trois éléphants, ou un char de la Première Guerre mondiale. Un cube d'eau de près de 2,5 mètres de côté.\n\nConcrètement : deux cent quarante adultes, ou dix voitures.",
    "20 t": "Vingt tonnes : un semi-remorque chargé, ou un char léger. Vingt mètres cubes d'eau, un cube de 2,7 mètres de côté.\n\nConcrètement : trois cent vingt adultes, quatre éléphants, ou treize voitures.",
    "30 t": "Trente tonnes : un char de combat moyen, une baleine à bosse, ou un wagon de marchandises plein. Un cube d'eau de 3,1 mètres de côté.\n\nConcrètement : près de cinq cents adultes, six éléphants, ou vingt voitures.",
    "50 t": "Cinquante tonnes : une locomotive, un char lourd moderne, ou une grande baleine à bosse. Un cube d'eau de près de quatre mètres de côté.\n\nConcrètement : huit cents adultes, dix éléphants, ou trente-trois voitures.",
}

text = open(GLOSS, encoding="utf-8").read()
n = 0
for key, new in NEW.items():
    pat = (r'(<div class="gcard gloss-card" data-key="' + re.escape(key) +
           r'" markdown>\n\*\*[^\n]*\*\*\n<div class="gcard-body" markdown>\n<div class="gcard-text" markdown>\n)'
           r'(.*?)(\n</div>\n<figure)')
    text, c = re.subn(pat, lambda m: m.group(1) + new + m.group(3), text, count=1, flags=re.S)
    if c:
        n += 1
    else:
        print("NON TROUVÉ :", key)
open(GLOSS, "w", encoding="utf-8").write(text)
print("cartes enrichies :", n, "/", len(NEW))
