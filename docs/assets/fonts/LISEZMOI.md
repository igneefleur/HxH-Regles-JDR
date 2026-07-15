# Polices du livre — auto-hébergées

Les cinq polices du site et du PDF sont hébergées ici, et non chargées depuis
Google Fonts. Conséquences : le navigateur du visiteur ne contacte aucun tiers
(son adresse IP n'est transmise à personne) et le build du PDF ne dépend pas du
réseau.

Les fichiers `.woff2` de ce dossier sont générés par `scripts/get_fonts.py`, qui
écrit aussi les `@font-face` dans `docs/stylesheets/fonts.css`. Ne pas les éditer
à la main : relancer le script.

## Les polices et leurs licences

Les cinq sont sous **SIL Open Font License 1.1**. Le texte complet de chaque
licence est dans `licences/`, comme l'OFL l'exige dès lors qu'on redistribue les
fichiers de police.

| Police | Rôle | Copyright | Licence |
|---|---|---|---|
| Alegreya | corps du livre + interface | Copyright 2011 The Alegreya Project Authors (huertatipografica) | [OFL 1.1](licences/alegreya-OFL.txt) |
| Cinzel | titres du livre | Copyright 2020 The Cinzel Project Authors (NDISCOVER) | [OFL 1.1](licences/cinzel-OFL.txt) |
| EB Garamond | repli et Forge | Copyright 2017 The EB Garamond Project Authors (octaviopardo) | [OFL 1.1](licences/eb-garamond-OFL.txt) |
| IBM Plex Sans | interface de l'Atelier | Copyright © 2017 IBM Corp., avec nom réservé « Plex » | [OFL 1.1](licences/ibm-plex-sans-OFL.txt) |
| Roboto Mono | blocs de code | Copyright 2015 The Roboto Mono Project Authors (googlefonts) | [OFL 1.1](licences/roboto-mono-OFL.txt) |

## Ce que l'OFL permet et impose

Elle autorise l'usage commercial, l'auto-hébergement, la modification, et
l'intégration des polices dans un document : le PDF du livre les embarque, ce qui
est explicitement prévu, et n'impose aucune licence au document lui-même.

Trois obligations, toutes déjà remplies ici :

- **Joindre la licence** aux fichiers redistribués : c'est le dossier `licences/`.
- **Ne pas vendre les polices seules.** Vendre un livre qui les embarque reste permis.
- **Renommer** toute police modifiée avant de la redistribuer (clause du nom réservé).
  Les fichiers de ce dossier sont inchangés, tels que publiés par Google Fonts.

Aucune attribution n'est à afficher sur le site : l'OFL ne l'exige pas.

## Sous-ensembles

Seuls `latin` et `latin-ext` sont embarqués : cela suffit au français (le œ est
dans « latin ») et évite de trimballer le cyrillique, le grec et le vietnamien.
Les `unicode-range` des `@font-face` font que le navigateur ne télécharge que les
fichiers dont il a réellement besoin.
