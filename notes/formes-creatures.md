# Formes — journal de calibrage

> Fichier de travail, **hors du livre**. Les deux tableaux (membres par forme, modificateurs de caractéristiques) sont désormais dans le livre, page canonique **[Formes du vivant](../docs/content/regles/nen/formes.md)**. Ici on ne garde que la logique de conception et les arbitrages ouverts, qui n'ont pas leur place dans `docs/`.

## Hypothèses de calibrage

- **Référence = l'humain** (forme *Bipède à bras*) : 0 partout. Toutes les valeurs sont des écarts à l'humain, moyenne physique 5.
- **La taille est traitée à part** (futur module *Changement de taille*). Les modificateurs décrivent le **plan de corps à échelle comparable**, pas la masse : la force d'une baleine vient de sa taille, pas de la forme.
- **La Dextérité est ancrée sur la main humaine** (meilleur outil de précision) : presque toutes les formes sont en malus de DEX ; trompe et pince remontent à −1, seul le céphalopode passe en bonus (+1).
- **Les sens ont leur propre module** (*Sens modifiés* / *Sens amplifiés*). La PER de forme ne fixe que la disposition de base ; gros écarts réservés aux formes sans tête.

## Logique par caractéristique (axes de calibrage)

- **FOR** — puissance du bâti du plan (pas la masse). Positive pour les charpentes robustes (quadrupèdes, trompe, pinces) ; négative pour les corps mous ou minuscules.
- **DEX** — précision et maniement, ancrée sur la main humaine. Malus dès qu'il n'y a plus de main ; atténué par trompe/pince, bonus seulement pour le tentacule du céphalopode.
- **AGI** — vivacité, équilibre, esquive, escalade. Positive pour pattes multiples et vol ; négative pour radiaires/sessiles et l'absence de membre.
- **END** — résistance biologique. Positive pour cuirassés, segmentés, marins ; négative pour les corps mous.
- **PER** — disposition sensorielle de base (gros écarts via le module Sens). Chute nette pour les formes **sans tête**.
- **PRÉ** — ascendant par l'apparition. Positive pour les silhouettes imposantes ; négative pour les corps informes ou minuscules.

## Décisions actées (calibrage fait, 6 juillet 2026)

Recalibrage complet par passe multi-agent (6 colonnes + 4 tables holistiques + synthèse + 2 critiques adverses). Valeurs définitives dans le livre.

- **Amplitude −4 à +4** (élargie depuis −4..+3).
- **DEX** : l'humain est la référence (0), pas un plafond. Seul le **céphalopode** dépasse 0 (+3) ; trompe et pinces restent sous la main (−1, −2).
- **PER des formes sans tête** : lecture « acuité réelle », pas « couverture 360° ». Méduse et étoile de mer à **−2** (capteurs diffus, sans cerveau : piètres percepteurs, au-dessus de l'éponge à −4, sous le ver à −1). Conséquence assumée : la méduse est une forme globalement faible, réaliste pour de la création de créature.
- **14 et 15** différenciés par la passe (Octopode à pinces FOR +2 ; à pinces et queue FOR +3).
- **Dominations** : aucune stricte après correction, sauf la méduse (radiaire à tentacules) faiblement dominée par le vermiforme depuis la baisse de PER, acceptée au nom du réalisme (un serpent est un meilleur plan qu'une méduse partout sauf robustesse).

## Formes ajoutées (recherche des manques, 6 juillet 2026)

Passe multiagent sur les animaux importants sans forme à inventaire exact. Deux ajouts (22 formes au total) :

- **Hexapode à deux ailes** (1 tête, 6 pattes, 2 ailes) : diptères (mouche, moustique). Scindée de l'Hexapode à quatre ailes. Carac calquées dessus (END +1 au lieu de +2, corps plus grêle).
- **Céphalopode à dix tentacules** (1 tête, 10 tentacules) : calmar, seiche. Scindée du Céphalopode à huit tentacules (poulpe). Carac = poulpe mais DEX +2 (bras moins adroits) et AGI +3 (nage à réaction).

Décisions liées :
- **Coléoptère laissé en Hexapode à quatre ailes** : les élytres sont des ailes antérieures durcies, le scarabée a bien 4 ailes. Divergence assumée avec la passe qui le rangeait en 2 ailes.
- **Corps modulaires : nombres figés conservés** (choix utilisateur) — Radiaire à tentacules 8 et Radiaire à cinq bras restent des gabarits canoniques ; la scission stricte ne vaut que pour les membres nettement dénombrables (ailes, bras de céphalopode). Le Myriapode, lui, passe en seuil **≥ 10 pattes** (premier palier au-dessus des formes à 8 pattes), ce qui absorbe cloporte (14), scolopendre (30-46), iules (jusqu'à ~750).

## Page déplacée + sens (7 juillet 2026)

- **Page déplacée** dans L'Échelle du Monde : `content/regles/monde/formes.md` (ancien `nen/formes.md` supprimé, liens internes en `../nen/`, nav mise à jour).
- **4 tableaux** au format armes (layout fixe, gabarits CSS `.formes.membres` / `.carac` / `.sens`, sommés à 100 %) : membres (+ exemples), caractéristiques physiques, sens externes, sens internes.
- **Sens** repris de `personnage/sens.md` (vocabulaire fermé : **17 externes**, **6 internes**). Chaque forme range TOUS les sens par niveau (primaire → inexistant). Le Bipède à bras reproduit la grille humaine du livre à l'identique. Validé exhaustif (0 manque/doublon sur 22 formes) ; fidélité au réel ~95 % via passe multiagent (4 attributeurs + synthèse + 3 critiques adverses par domaine sensoriel + finale). Générateur : `scripts/gen_formes.py` (données embarquées, source unique de la page).

## Points encore ouverts

- **Grenouille AGI +2** (à égalité avec le quadrupède agile) : tranché ainsi pour lever deux quasi-dominations ; un crapaud est pataud, mais la forme couvre aussi la grenouille bondissante.
- **Coûts DT/INS/UAA/MA** des formes (dans la Métamorphose) : toujours de première passe, non recalibrés.

## Fuites de taille (audit après coup)

Rappel : toutes les formes sont calibrées à **taille moyenne**, la taille étant un axe séparé.

- **Corrigé — Quadrupède à trompe** : le spécialiste FOR avait imposé +4 (force d'éléphant = taille), là où les 4 tables holistiques disaient +1/+2. Ramené à un tapir de taille moyenne : FOR +4→+2, AGI −1→0, PRÉ +2→+1.
- **PRÉ — lecture actée : allure et charisme** (pas menace de la silhouette). La PRÉ mesure magnétisme, ascendant, commandement, allure : un insecte n'en dégage aucun quelle que soit sa taille. Les négatifs des arthropodes/insectes tiennent donc à taille neutre (ce ne sont pas des fuites de taille). Colonne PRÉ figée, hors trompe déjà corrigée.

Bilan : après correction de la trompe, le tableau est calibré à taille moyenne sur les six axes. Plus de fuite de taille connue.

## Refonte des noms (7 juillet 2026)

Passe multi-agent (étymologie / cohérence interne / clarté joueur / schéma) + synthèse. Système jugé cohérent à ~75 %. Convention actée : **racine morphologique + nombre du membre distinctif**, jamais de nom fonctionnel.

- Famille **« Marcheur » (fonctionnelle) retirée**, réalignée sur l'échelle en -pode : Marcheur à pinces → **Octopode à pinces** (crabe, 8 pattes) ; Marcheur à pinces et queue → **Octopode à pinces et queue** (scorpion, homard) ; Marcheur à queue → **Décapode à queue** (crevette, limule, 10 pattes — corrige aussi la fiche Métamorphose qui disait 8).
- Échelle des pattes complète : Bipède → Quadrupède → Hexapode → Octopode → Décapode → Myriapode.
- **Quadrupède sans queue → Quadrupède** (retire la seule tournure négative ; grenouille = racine nue, chien = « à queue »).
- **Radiaire à bras → Radiaire à cinq bras** ; **Bipède ailé → Bipède à deux ailes** (uniformise « à N ailes »). Rappel : Corps nu → **Informe** (retire la connotation « déshabillé »).
- Gardés volontairement : « Céphalopode à N tentacules » (clarté > exactitude « bras ») ; « Octopode » araignée (collision d'image pieuvre assumée) ; « Radiaire à tentacules » non chiffré (nombre vraiment variable). Non retenues : Bipède à deux bras, Informe → Asymétrique.
- **Réglé (7 juillet)** : comptes de membres re-synchronisés entre `formes.md` et la fiche Métamorphose (seule dérive = Décapode 8→10) ; les 22 formes triées dans le même ordre (regroupées par plan de corps : bipèdes, quadrupèdes, vermiforme, nageurs, hexapodes, octopodes, décapode, myriapode, céphalopodes, radiaires, informe) sur les deux pages ; générateur déplacé dans `scripts/gen_formes.py` (chemin robuste, source persistante).

## Déplacement (7 juillet 2026)

Règles de texte dans formes.md (section « Le déplacement »), **PAS de table par forme** (l'utilisateur a refusé le tableau que j'avais ajouté : « je t'ai jamais demandé un tableau »). Calibré par passe multi-agent (vitesses réelles → paliers sur la table de mouvement de `capacites-physiques.md`, où 1 palier = 1 point d'AGI).

- **Aérien** : aile → naturel ; sinon impossible (binaire, l'aile est tout-ou-rien).
- **Terrestre** : patte/jambe → naturel ; sinon **−4 paliers** (÷4 ≈ serpent vs animal à pattes ; le −2 par défaut ne faisait que ÷1,8, trop faible).
- **Aquatique** : sans nageoire → **−3 paliers** (÷2,7 ≈ courir vs nager d'un humain), SAUF si la forme porte une propriété spéciale de nage.
- Asymétrie 4 vs 3 voulue : se traîner sans pattes au sol coûte plus cher que pagayer, l'eau portant le corps.
- **Exceptions aquatiques via une colonne « Propriété spéciale »** ajoutée au 1er tableau (« Les formes en bref »), PAS dans la règle (choix utilisateur) : Ondulation (Vermiforme), Propulsion à réaction (Céphalopodes), Pulsation (Radiaire à tentacules), Podia (Radiaire à cinq bras) ; ces propriétés dispensent du malus aquatique. Dict `PROP` dans `gen_formes.py`.
- **Légendes** (defs sous le tableau bio) : un lead-in énonce l'effet commun (nage à Agilité pleine, sans malus aquatique), puis une entrée par propriété décrit son mécanisme. Podia calé sur l'**aquatique seul** (étoile de mer inerte hors de l'eau), pas terre + eau comme l'exemple donné par l'utilisateur — à rouvrir s'il le veut.
- **Coût en membres** (demandé : « combien de bras pour me déplacer ? un membre qui propulse ne peut pas tenir un fusil »). Règle générale dans la section Déplacement : les jambes avancent et les bras restent libres ; quand les mêmes membres portent ET agissent, la propriété chiffre le coût. Par propriété : **pulsation** (méduse) = poussée du corps → tentacules libres en tout temps ; **propulsion à réaction** (céphalopode) = tentacules libres à l'arrêt et en croisière, mais plaqués en fuseau (occupés) en sprint / allure lourde (choix utilisateur, nuance réaliste) ; **ondulation** = corps entier → aucun membre à occuper ; **podia = moitié des bras arrondie au sup. = 3 des 5 bras de l'étoile → 2 libres** (pile un fusil à 2 mains). Nombres à retoucher si besoin.
- **Principe anti-double-comptage** (soulevé par l'utilisateur) : ne JAMAIS pénaliser une forme dans son milieu natif, car son malus d'AGI porte déjà sa lenteur. Sinon double peine : l'étoile de mer (AGI −3) + −3 de déplacement = immobile dans l'eau, ce qui est faux. Le « corps radiaire » a été ajouté à l'exemption aquatique pour ça (étoile de mer, méduse : leur lenteur est dans l'AGI, pas dans un malus de milieu).
- Ratés assumés (« garder simple ») : l'éponge (Informe, sessile) garde −3/−4, mais son AGI −4 la fige de toute façon → immobile, ce qui est correct ; baleine/poisson prennent −4 à terre au lieu d'un statut « échoué ».
- Vitesses obtenues (créature moyenne AGI 5) : sans pattes au sol ≈ 1,2 / 2,4 / 6 km/h ; sans organe de nage ≈ 0,5 / 1,0 / 2,5 m/s.
