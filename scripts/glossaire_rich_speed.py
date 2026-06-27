# -*- coding: utf-8 -*-
"""Passe toutes les cartes de distance (vitesse) au format riche (2 paragraphes).
Usage : python scripts/glossaire_rich_speed.py"""
import re, sys
sys.stdout.reconfigure(encoding="utf-8")
GLOSS = "docs/includes/glossaire.md"

NEW = {
    "1 m": "Un mètre par tour, soit 0,6 km/h ou dix-sept centimètres par seconde : un déplacement au ralenti, plus lent qu'une marche d'enfant.\n\nConcrètement : il faut près d'une minute pour franchir dix mètres, et plus d'une heure et demie pour un seul kilomètre.",
    "2 m": "Deux mètres par tour, soit environ 1 km/h : l'allure d'un escargot rapide ou d'une foule très dense qui piétine.\n\nConcrètement : un kilomètre prendrait près d'une heure, cinq fois plus lentement qu'une marche normale.",
    "3 m": "Trois mètres par tour, soit 1,8 km/h : une marche très lente, celle d'une promenade en traînant les pieds.\n\nConcrètement : on met une demi-heure pour un kilomètre, presque trois fois moins vite qu'un marcheur ordinaire.",
    "4 m": "Quatre mètres par tour, soit 2,4 km/h : une flânerie tranquille, sans le moindre effort.\n\nConcrètement : un kilomètre en vingt-cinq minutes, environ la moitié d'une marche normale.",
    "5 m": "Cinq mètres par tour, soit 3 km/h : une marche lente, en dessous de l'allure naturelle d'un adulte.\n\nConcrètement : un kilomètre en vingt minutes.",
    "6 m": "Six mètres par tour, soit 3,6 km/h ou un mètre par seconde : une marche tranquille, du pas d'une balade en ville.\n\nConcrètement : un kilomètre en un peu moins de dix-sept minutes.",
    "8 m": "Huit mètres par tour, soit 5 km/h : la vitesse de marche normale d'un adulte.\n\nConcrètement : un kilomètre en douze minutes, ou dix kilomètres en deux heures.",
    "9 m": "Neuf mètres par tour, soit 5,4 km/h : une marche soutenue, du pas pressé de quelqu'un en retard.\n\nConcrètement : un kilomètre en un peu plus de onze minutes.",
    "10 m": "Dix mètres par tour, soit 6 km/h : une marche rapide, à la limite du petit trot.\n\nConcrètement : un kilomètre en dix minutes, à peine plus qu'une marche ordinaire.",
    "12 m": "Douze mètres par tour, soit 7,2 km/h ou deux mètres par seconde : un petit footing tranquille.\n\nConcrètement : un kilomètre en un peu plus de huit minutes.",
    "15 m": "Quinze mètres par tour, soit 9 km/h : un footing régulier, l'allure d'un coureur du dimanche.\n\nConcrètement : un kilomètre en près de sept minutes, presque deux fois la vitesse de la marche.",
    "16 m": "Seize mètres par tour, soit 9,6 km/h : un jogging franc.\n\nConcrètement : un kilomètre en un peu plus de six minutes.",
    "18 m": "Dix-huit mètres par tour, soit 10,8 km/h : une course légère et soutenue.\n\nConcrètement : un kilomètre en cinq minutes et demie.",
    "20 m": "Vingt mètres par tour, soit 12 km/h : une course de fond, l'allure d'un marathonien amateur.\n\nConcrètement : un kilomètre en cinq minutes, un marathon en un peu plus de trois heures et demie.",
    "24 m": "Vingt-quatre mètres par tour, soit 14,4 km/h ou quatre mètres par seconde : un bon coureur de fond en rythme de compétition.\n\nConcrètement : un kilomètre en un peu plus de quatre minutes.",
    "30 m": "Trente mètres par tour, soit 18 km/h : un coureur rapide, ou un cycliste de promenade.\n\nConcrètement : un kilomètre en un peu plus de trois minutes, plus de trois fois la vitesse de la marche.",
    "40 m": "Quarante mètres par tour, soit 24 km/h : un sprint pour un amateur, ou un bon cycliste lancé.\n\nConcrètement : un kilomètre en deux minutes et demie, cinq fois plus vite qu'un marcheur.",
    "45 m": "Quarante-cinq mètres par tour, soit 27 km/h : un cycliste lancé, ou un chien qui court à fond.\n\nConcrètement : un kilomètre en un peu plus de deux minutes.",
    "50 m": "Cinquante mètres par tour, soit 30 km/h : un cheval au trot rapide, ou un coureur d'élite en plein sprint.\n\nConcrètement : un kilomètre en deux minutes, six fois la vitesse de la marche.",
    "60 m": "Soixante mètres par tour, soit 36 km/h ou dix mètres par seconde : un très bon cycliste à fond, ou un éléphant qui charge.\n\nConcrètement : un kilomètre en cent secondes.",
    "80 m": "Quatre-vingts mètres par tour, soit 48 km/h : un cheval au galop, ou un sanglier en pleine course.\n\nConcrètement : un kilomètre en soixante-quinze secondes, près de dix fois la vitesse de la marche.",
    "100 m": "Cent mètres par tour, soit 60 km/h : un lévrier lancé, parmi les plus rapides des animaux terrestres.\n\nConcrètement : un kilomètre en une minute pile, ou dix kilomètres en dix minutes.",
    "120 m": "Cent vingt mètres par tour, soit 72 km/h ou vingt mètres par seconde : un cheval de course pur-sang à pleine vitesse.\n\nConcrètement : un kilomètre en cinquante secondes.",
    "150 m": "Cent cinquante mètres par tour, soit 90 km/h : un guépard presque à fond, le plus rapide des animaux terrestres.\n\nConcrètement : un kilomètre en quarante secondes, dix-huit fois la vitesse de la marche.",
    "160 m": "Cent soixante mètres par tour, soit 96 km/h : un guépard lancé, ou une voiture à vive allure.\n\nConcrètement : un kilomètre en trente-sept secondes.",
    "200 m": "Deux cents mètres par tour, soit 120 km/h ou trente-trois mètres par seconde : une voiture sur l'autoroute, ou un faucon en vol horizontal.\n\nConcrètement : un kilomètre en trente secondes, ou deux kilomètres en une minute.",
    "300 m": "Trois cents mètres par tour, soit 180 km/h : un train rapide, ou une moto de sport lancée.\n\nConcrètement : un kilomètre en vingt secondes, trois kilomètres en une minute.",
    "400 m": "Quatre cents mètres par tour, soit 240 km/h : une voiture de sport à fond, ou un TGV en accélération.\n\nConcrètement : un kilomètre en quinze secondes, quatre kilomètres en une minute.",
    "500 m": "Cinq cents mètres par tour, soit 300 km/h ou quatre-vingt-trois mètres par seconde : un TGV en vitesse commerciale, ou une Formule 1 en ligne droite.\n\nConcrètement : cinq kilomètres en une minute, soixante fois la vitesse de la marche.",
    "600 m": "Six cents mètres par tour, soit 360 km/h : un TGV à pleine vitesse, ou le plongeon d'un faucon pèlerin.\n\nConcrètement : six kilomètres en une minute, un kilomètre en dix secondes.",
    "750 m": "Sept cent cinquante mètres par tour, soit 450 km/h : la vitesse d'un avion à hélice, ou d'une voiture de record terrestre.\n\nConcrètement : sept kilomètres et demi en une minute.",
    "800 m": "Huit cents mètres par tour, soit 480 km/h : un avion à hélice rapide, ou un petit avion d'affaires.\n\nConcrètement : huit kilomètres en une minute, près de cent fois la vitesse de la marche.",
    "1 km": "Un kilomètre par tour, soit 600 km/h ou cent soixante-sept mètres par seconde : un avion de ligne au décollage.\n\nConcrètement : dix kilomètres en une minute, à peine la moitié de la vitesse du son.",
    "1,2 km": "1,2 km par tour, soit 720 km/h : un avion de ligne en début de croisière.\n\nConcrètement : douze kilomètres en une minute, près de soixante pour cent de la vitesse du son.",
    "1,5 km": "1,5 km par tour, soit 900 km/h : un avion de ligne en croisière, juste sous le mur du son.\n\nConcrètement : quinze kilomètres en une minute, les trois quarts de la vitesse du son.",
    "1,6 km": "1,6 km par tour, soit 960 km/h : un avion de ligne rapide, à la limite du domaine subsonique.\n\nConcrètement : seize kilomètres en une minute, on frôle le mur du son.",
    "3 km": "3 km par tour, soit 1 800 km/h (Mach 1,5) : un avion de chasse en supersonique franc.\n\nConcrètement : trente kilomètres en une minute, une fois et demie la vitesse du son.",
    "4 km": "4 km par tour, soit 2 400 km/h (Mach 2) : un chasseur de combat à pleine vitesse, comme un Mirage ou un F-15.\n\nConcrètement : deux fois la vitesse du son, le tour de la Terre en moins de dix-sept heures.",
    "5 km": "5 km par tour, soit 3 000 km/h (Mach 2,5) : plus rapide que presque tous les avions militaires en service.\n\nConcrètement : deux fois et demie la vitesse du son, le tour de la Terre en treize heures.",
    "6 km": "6 km par tour, soit 3 600 km/h (Mach 3) : l'avion-espion SR-71 Blackbird, l'avion habité le plus rapide jamais construit.\n\nConcrètement : un kilomètre par seconde, le tour de la Terre en onze heures.",
    "7,5 km": "7,5 km par tour, soit 4 500 km/h (Mach 3,6) : au-delà de tout avion habité, dans le domaine des missiles.\n\nConcrètement : soixante-quinze kilomètres en une minute, près de quatre fois la vitesse du son.",
    "10 km": "10 km par tour, soit 6 000 km/h (Mach 5) : le seuil de l'hypersonique, celui des planeurs expérimentaux et des missiles de croisière avancés.\n\nConcrètement : cinq fois la vitesse du son, le tour de la Terre en moins de sept heures.",
    "15 km": "15 km par tour, soit 9 000 km/h (Mach 7) : la vitesse d'un missile hypersonique de pointe.\n\nConcrètement : cent cinquante kilomètres en une minute, sept fois la vitesse du son.",
    "20 km": "20 km par tour, soit 12 000 km/h (Mach 10) : un planeur hypersonique expérimental.\n\nConcrètement : cent kilomètres en une demi-minute, le tour de la Terre en un peu plus de trois heures.",
    "25 km": "25 km par tour, soit 15 000 km/h (Mach 12) : au-delà de tout véhicule atmosphérique connu.\n\nConcrètement : douze fois la vitesse du son, deux cent cinquante kilomètres en une minute.",
    "40 km": "40 km par tour, soit 24 000 km/h (Mach 20) : une capsule spatiale lors de sa rentrée dans l'atmosphère, freinée par une boule de feu.\n\nConcrètement : le tour de la Terre en moins de deux heures, vingt fois la vitesse du son.",
    "50 km": "50 km par tour, soit 30 000 km/h (Mach 24) : la vitesse de satellisation, celle qu'il faut atteindre pour rester en orbite autour de la Terre.\n\nConcrètement : huit kilomètres par seconde, le tour de la Terre en un peu plus d'une heure.",
    "100 km": "100 km par tour, soit 60 000 km/h (Mach 49) : plus vite qu'aucun engin humain en vol atmosphérique, l'ordre des sondes spatiales les plus rapides au lancement.\n\nConcrètement : le tour de la Terre en quarante minutes, près de cinquante fois la vitesse du son.",
    "200 km": "200 km par tour, soit 120 000 km/h (Mach 97) : le domaine des objets célestes.\n\nConcrètement : on rejoindrait la Lune en un peu plus de trois heures, et le tour de la Terre en vingt minutes.",
    "250 km": "250 km par tour, soit 150 000 km/h (Mach 121) : une vitesse purement cosmique, plus de mille fois plus rapide qu'un avion de ligne.\n\nConcrètement : le tour de la Terre en seize minutes, ou la Lune en deux heures et demie, mais encore moins d'un millième de la vitesse de la lumière.",
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
print("cartes de vitesse enrichies :", n, "/", len(NEW))
