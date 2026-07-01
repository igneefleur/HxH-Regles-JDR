# Générateur de monde (TTRPG) — monde plat, génération « façon Terre »

Génère **quatre cartes du même monde** procédural, toutes dans un cadre
rectangulaire à **grille uniforme** (cases de taille identique partout) :

| Carte | Fichier | Contenu |
|---|---|---|
| Aplat | `monde_plat_aplat.png` | terres / mer, côtes vectorielles |
| Relief | `monde_plat_relief.png` | hypsométrie + ombrage (bathymétrie) |
| Plaques | `monde_plat_plaques.png` | plaques tectoniques + mouvements |
| Continents | `monde_plat_continents.png` | terres colorées **par continent** (îles comprises) |

Le monde est **plat** (génération 2D, pas une sphère). La grille est régulière.
L'objectif est une géographie **proche de la Terre** — formes de continents et
reliefs cohérents avec le monde réel — mesurée par un **score de ressemblance**
(`earth_score`, 0..1) calé sur les statistiques d'ETOPO1.

## Méthode

La forme des continents vient d'une **continentalité bruitée**, pas d'un découpage
géométrique ; le relief vient d'un **transfert hypsométrique** vers la courbe
terrestre. (L'ancien découpage en « fossés de Voronoï » donnait des galettes
~égales aux côtes lisses — peu réaliste ; il a été remplacé.)

1. **Bords du cadre = océan** (fenêtre cernée d'eau, tous les continents à l'intérieur).
2. **Continentalité `C`** : un champ de bruit fractal (fBm) **multi-octaves à
   domaine déformé** (*domain warping*) donne des **côtes fractales** (dimension
   ~1.25) et des **tailles inégales** ; **deux lobes gaussiens dominants** (façon
   Afro-Eurasie + Amériques) imposent deux grandes masses ; une **bande haute
   fréquence dédiée** (`coast_rough`) rugosifie la côte ; un **couplage doux aux
   plaques** continentales corrèle terre et croûte. Le **niveau marin** (percentile)
   vise ~**29 %** de terres. Aucun fossé creusé → la séparation des masses émerge
   des creux de bruit (côtes naturelles).
3. **Plaques tectoniques** (méthode [redblobgames](https://www.redblobgames.com/x/1843-planet-generation/),
   adaptée au plan) : noyaux espacés → remplissage BFS → plaques océaniques /
   continentales + dérive → **collisions** aux frontières → champ de **convergence**.
4. **Relief par orogenèse tectonique + transfert hypsométrique**. Les montagnes ne
   sortent **pas** du champ d'altitude (ce qui ferait des **dômes ronds**) : elles
   sont **tracées en rubans étroits le long des frontières de plaques en
   compression** (raster), l'amplitude suit la **convergence locale** et **s'éteint
   en pointe** aux extrémités → **cordillères linéaires** (largeur réglée par
   `relief_width`). La **subduction** (frontière océan/continent) donne une chaîne
   **côtière** appariée à une **fosse au large** ; la **collision** continent/continent
   donne une chaîne **intérieure** type Himalaya. On classe ensuite les pixels de
   terre (rang : *intérieur léger + ceintures + continentalité*) et on calque ce rang
   sur la **courbe hypsométrique terrestre** (LUT) → surtout des **plaines basses**,
   fine **queue de montagnes**. Côté océan, une LUT
   **plateau / talus / abysse / fosse** donne un histogramme **bimodal** (plateau
   ~−130 m, mode abyssal ~−4500 m). **Érosion** thermique pour les vallées.
5. **Relief continu (pas « binaire »).** Pour éviter le rendu « vert plat OU ruban
   de montagne, rien entre », on superpose un **crag** (bruit ridged multi-octaves)
   à **moyenne nulle exacte** (`crag − crag[land].mean()`), calé par une **amplitude
   qui croît avec l'altitude** (`cragamp = 470 + 0.42·elev`). La moyenne nulle est
   essentielle : elle ajoute contreforts/plateaux/dégradé **sans dériver
   l'hypsométrie** (le rang est préservé → `earth_score` stable). L'océan reçoit une
   **texture abyssale** (collines basse + moyenne fréquence, **dorsale** ridged loin
   des côtes, dither de plateau près des côtes).
6. **Rendu « roche mate ».** Les cœurs de montagne paraissaient **vitreux/plastiques**
   parce que l'ombrage **floutait les normales** (σ 0.4) avant le hillshade et lissait
   les facettes. Correctif côté rendu : **dé-flouter** l'ombrage (σ 0.2) pour que les
   facettes portent l'ombre, + **assombrissement passe-haut** « roche mate »
   (`|z − flou(z)|`, gaté à l'altitude). L'océan profond, dont le relief existait dans
   la donnée mais ne s'ombrait pas, reçoit une **exagération d'ombrage** (×3.5) et une
   **palette profonde resserrée** → collines abyssales visibles.

**Découplage résolution.** La géographie est calculée sur une **grille FIXE**
(`gow×goh = 1300×1101`) puis **rééchantillonnée** vers le rendu `--ow` : le
**nombre de continents ne dépend pas de `--ow`**.

## Score de ressemblance à la Terre (`earth_score`, 0..1)

Moyenne pondérée de **7 sous-scores** comparant le monde aux statistiques réelles
(chaque sous-score = proximité à une cible terrestre, tolérance serrée) :

| Sous-score | Poids | Cible Terre |
|---|---|---|
| `land_fraction` | 0.10 | 29 % de terres |
| `hypsometry_land_match` | 0.20 | bandes d'altitude des terres (surtout basses, médiane ≪ moyenne) |
| `ocean_depth_bimodality` | 0.18 | histogramme bimodal, mode abyssal ~−4500 m, talus sparse |
| `coastline_fractal_dimension` | 0.16 | dimension fractale de la côte ~1.25 |
| `landmass_size_inequality` | 0.16 | une-deux masses dominantes (largest ~0.5, top-2 ~0.84) |
| `mountain_fraction_and_linearity` | 0.12 | montagnes en **ceintures linéaires**, ~24 % des terres |
| `continent_count_soft` | 0.08 | ~6 continents (poids faible) |

La recherche de graine garde la première graine de score `>= --earth-target`
(défaut 0.75), sinon la meilleure. **Repère** : la Terre elle-même score **~0.86**
sur cette métrique (les tolérances sont serrées) ; viser ~0.75 ≈ **85 % de la
Terre**. L'ancien générateur (galettes) scorait ~0.36.

```bash
python worldflat.py metric --seed 12        # détail des 7 sous-scores pour une graine
python worldflat.py sweep --tries 40        # score moyen + P(score >= cible) sur N graines
```

## Utilisation

```bash
# Graine ALÉATOIRE filtrée pour ressembler à la Terre (score >= 0.75)
python worldflat.py

# Reproduire un monde précis
python worldflat.py --seed 12 --ow 3000 --no-pick

# Régler la forme : moins/plus de continents, côtes plus découpées, masse dominante
python worldflat.py --base-freq 1.8          # moins de continents, plus grands
python worldflat.py --warp1 0.5 --coast-rough 1.0   # côtes plus fractales (trop = trame directionnelle)
python worldflat.py --dom-gain 0.10 --dom-gain2 0.0  # une seule grande masse

# Très haute résolution : séparer build (lent) et rendu (rapide)
python worldflat.py build --ow 4000    # calcule -> out/world.npz (graine notée dedans)
python worldflat.py render             # rend les 4 cartes depuis le cache
```

Options principales : `--seed`, `--crust` (fraction de terres ~0.29), `--plates`,
`--plate-smooth`, et les **knobs de forme/relief** ci-dessous. Le filtrage de graine
sonde à la résolution géo (`--pick-ow`, défaut 1300) ; le compte y est stable.

## Réglages principaux (knobs)

| Knob | Rôle | Défaut |
|---|---|---|
| `base_freq` | fréquence basse de la continentalité : **nombre/taille** des continents (bas = peu, grands) | `2.4` |
| `cont_gain` | persistance du fBm : rougit le spectre → inégalité des tailles + queue d'îles | `0.60` |
| `cont_octaves` | octaves de continentalité : **détail fractal** de la côte | `8` |
| `warp1` / `warp2` | domain-warp basse / fine fréquence : casse les galettes, golfes, péninsules, fjords. **L'azimut du warp tourne par région** (champ d'angle bruité) pour éviter une **trame directionnelle** (peigne d'îles/lagunes alignées) | `0.25` / `0.04` |
| `coast_rough` | bande haute fréquence dédiée à la **rugosité de côte** (dimension fractale ~1.25) | `0.65` |
| `dom_gain` / `dom_gain2` | force des **2 lobes dominants** (deux grandes masses) | `0.18` / `0.16` |
| `lobe_sigma` / `lobe2_scale` | taille du 1er lobe / du 2e relative | `0.48` / `0.90` |
| `lobe_aniso` | anisotropie des lobes (>1 = étiré, façon Eurasie) | `2.2` |
| `harm_w` | poids du champ harmonique (plaques) réinjecté comme texture côtière | `0.04` |
| `plate_bias` | couplage doux terre ↔ croûte continentale | `0.15` |
| `crust_frac` | **fraction de terres** émergées visée (niveau marin par percentile) | `0.29` |
| `relief_chains` | amplitude des **ceintures de montagnes** (rubans le long des collisions) | `1.0` |
| `relief_width` | demi-largeur des crêtes (fraction de largeur) : bas = **cordillères étroites**, haut = chaînes larges | `0.011` |
| `conv_ref_pct` | percentile de convergence servant d'échelle aux ceintures | `88` |
| `mtn_tail` | hauteur/raideur de la queue haute (rareté/altitude des montagnes) | `1.0` |
| `shelf_frac` / `slope_w` | largeur (rang) du plateau / du talus continental (bimodalité océan) | `0.075` / `0.135` |
| `abyss_depth_m` / `shelf_depth_m` | profondeur du mode abyssal / du shelf-break (m) | `-4500` / `-130` |
| `trench_amp` | plongée des fosses (convergence océan-océan) | `0.8` |
| `erosion_iters` | érosion thermique du relief (vallées) | `16` |
| `elev_scale_m` | mètres correspondant à +1.0 normalisé (échelle de rendu) | `5000` |
| `n_plates` | nombre de **plaques** tectoniques | `10` |
| `continent_area` | aire d'**un continent** ; au-delà, une masse scinde (Eurasie/Europe+Asie, plafond 3) | `0.035` |
| `island_min` | aire minimale d'un groupe pour **compter** comme continent (toujours coloré) | `0.009` |
| `geo_ow` | largeur de la **grille géo fixe** (découplage résolution) | `1300` |

## Comptage et coloration des continents

`count_continents` compte, `label_continents` colore :
- **un continent est une masse de terre** ; les masses séparées par moins d'un
  « pont maritime » (`sea_bridge`) sont réunies (une île proche s'y rattache) ;
- un groupe dont la terre couvre moins de `island_min` est ignoré pour le **compte**
  (mais reste **coloré**, rattaché au continent le plus proche) ;
- une masse géante (type **Eurasie**) compte pour `round(aire / continent_area)`,
  **plafonné à 3** (Europe + Asie + …).

## Performance

Géographie calculée à la résolution **géo fixe** (`1300×1101`) quelle que soit
`--ow` ; un build complet coûte ~**25–30 s** (continentalité + transfert
hypsométrique par rang + érosion sur 1,43 M de points), `--ow` ne coûte que le
**rééchantillonnage**. La recherche de graine enchaîne des builds (chemin
`count_only` rapide pour ne pas payer le transfert hypsométrique). Le bruit de
Perlin est vectorisé (forme « improved noise » à coins de permutation partagés).

## Notes

- L'affichage est rectangulaire à grille uniforme : le monde est plat, les
  latitudes n'ont pas de sens physique ici.
- `out/world.npz` est un cache (altitude, masques, plaques, graine) ; supprimable.
- Plaques d'après *Red Blob Games — Procedurally generating a planet*
  (`redblobgames.com/x/1843-planet-generation/`), adaptées au monde plat ; la
  forme des continents et l'hypsométrie sont calées sur la **Terre** (ETOPO1).
