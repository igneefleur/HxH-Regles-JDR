# Fiche HxH sur Roll20 — extension Firefox

Affiche une fiche de personnage HxH (créée sur le site) à la place de la fiche
Roll20, avec les jets envoyés dans le tchat.

## Fonctionnement

- Le **site HxH** calcule chaque fiche et l'écrit dans son `localStorage` sous
  forme de « carte » lecture seule (`creation-cards`). Aucune règle n'est
  recopiée dans l'extension.
- `content-hxh.js` recopie ces cartes dans `browser.storage.local` quand on
  visite le site.
- `content-roll20.js` ajoute un bouton **Fiche HxH** sur l'éditeur Roll20 ; il
  ouvre un panneau qui affiche la fiche choisie (rendue par `render.js`) et
  envoie les jets dans le tchat.
- Le **popup** de la barre d'outils liste les fiches synchronisées et choisit
  celle affichée par défaut.

## Installer (Firefox)

Installation temporaire (redémarre à la fermeture de Firefox) :

1. `about:debugging#/runtime/this-firefox`
2. « Charger un module complémentaire temporaire… »
3. choisir `manifest.json` de ce dossier (ou l'archive `.xpi`).

Puis : ouvrir le créateur sur le site HxH (les personnages se synchronisent),
ouvrir une partie Roll20, cliquer **Fiche HxH**.

## Développement

Fichiers : `manifest.json`, `render.js` (rendu + jets, pur), `content-hxh.js`
(sync depuis le site), `content-roll20.js` (bouton + panneau), `overlay.css`,
`popup/`, `icons/`.
