# HxH Système JDR

Un jeu de rôle sur table dans l'univers de Hunter × Hunter : un livre de règles
complet et les outils qui vont avec.

**Le site : <https://igneefleur.github.io/HxH-Regles-JDR/>**

## Œuvre de fan

Ce projet est une œuvre de fan, sans but lucratif et sans lien avec les ayants
droit. « Hunter × Hunter », le Nen, les Hunters, les personnages et les lieux
appartiennent à Yoshihiro Togashi et à Shueisha.

Le système de règles, les textes et le code sont de l'auteur et sont en **tous
droits réservés** : le dépôt est public pour consultation, pas pour réutilisation.
Voir [LICENSE.md](LICENSE.md) pour le détail, y compris les composants tiers
(polices, thème, chaîne de construction) qui gardent leurs propres licences.

## Ce que contient le projet

**Le livre** : les règles (personnage, formations, arts, échelle du monde, combat,
Nen) et l'univers. Il se lit en défilement continu d'un chapitre à l'autre, et se
télécharge en PDF (2 colonnes, mis en page comme le site).

**Trois outils**, servis par le même site :

| Outil | Adresse | Rôle |
|---|---|---|
| Création | `/personnage/` | créateur de personnage complet |
| Forge | `/forge/` | conception d'armes sur un budget de 100 points |
| Atelier | `/creation/` | conception de pouvoirs de Nen, éditeur à nœuds |

**Une extension navigateur** (Firefox et Chrome) qui fait tourner le vrai créateur
dans une fiche Roll20 et persiste le personnage dans ses attributs.

## Le principe : les règles sont la source unique

Les outils n'ont pas leur propre copie des données. À chaque construction, des
*hooks* Python relisent les pages de règles et en extraient le JSON que consomme le
JavaScript. Modifier une table dans le livre mène donc l'outil à jour, sans double
saisie ni risque de divergence.

| Hook | Lit | Produit |
|---|---|---|
| `hooks/creation.py` | les règles du personnage | `creation.json` (caractéristiques, compétences, arts, armes…) |
| `hooks/forge.py` | `combat/armes.md` | `forge.json` (fiches de propriétés, barème) |
| `hooks/nen_atelier.py` | les règles du Nen | `nen-atelier.json` (modules) |
| `hooks/changelog.py` | l'historique git | les dernières modifications, en page d'accueil |

## Développer

```bash
pip install mkdocs-material
mkdocs serve          # http://127.0.0.1:8000
```

Le site se construit avec `mkdocs build`. Les hooks tournent à chaque
construction : les JSON des outils sont donc toujours régénérés.

### Le PDF

Le PDF est généré par WeasyPrint (plugin `mkdocs-to-pdf`) et **uniquement en CI**,
via une configuration séparée :

```bash
ENABLE_PDF_EXPORT=1 mkdocs build --config-file mkdocs.ci.yml
```

Il vit dans `mkdocs.ci.yml` et non dans `mkdocs.yml` pour une raison précise : le
plugin importe WeasyPrint dès le chargement du module, or WeasyPrint réclame des
bibliothèques natives (Pango, GTK) absentes de Windows. L'inscrire dans la config
principale casserait `mkdocs serve` en local.

Sous Windows, on peut quand même construire le PDF en prêtant à WeasyPrint les DLL
de GIMP : mettre `C:\Program Files\GIMP 3\bin` en tête du `PATH` et dans
`WEASYPRINT_DLL_DIRECTORIES`, puis lancer la commande ci-dessus.

### Les polices

Les sept polices sont auto-hébergées : le site ne contacte pas Google Fonts, donc
l'adresse IP du visiteur n'est transmise à personne, et le PDF se construit hors
ligne. Pour les régénérer (fichiers, licences et `@font-face`) :

```bash
python scripts/get_fonts.py
```

Détails et licences : [`docs/assets/fonts/LISEZMOI.md`](docs/assets/fonts/LISEZMOI.md).

## Structure

| Chemin | Contenu |
|---|---|
| `docs/content/` | le livre : règles et univers |
| `docs/personnage/`, `docs/forge/`, `docs/creation/` | les pages des trois outils |
| `docs/javascripts/` | les outils, la lecture continue, le mode nuit, le glossaire |
| `docs/stylesheets/` | `extra.css` porte la mise en page du livre ; `fonts.css` est générée |
| `docs/assets/fonts/` | les polices auto-hébergées et leurs licences |
| `hooks/` | l'extraction des règles vers le JSON des outils |
| `scripts/` | outillage : polices, extension, générateurs de contenu |
| `extension/` | l'extension Roll20 (Firefox et Chrome) |
| `overrides/` | surcharges du thème Material |
| `templates/styles.scss` | retouches CSS appliquées au PDF seulement |

## Déploiement

Chaque envoi sur `main` déclenche `.github/workflows/deploy.yml`, qui construit le
site **et** le PDF, puis publie sur GitHub Pages.
