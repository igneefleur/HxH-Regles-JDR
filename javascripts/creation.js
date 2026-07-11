/* Création — créateur de personnage (sans le Nen), mise en page « fiche ».
 *
 * Contenu (caractéristiques, Éclat, compétences, formations, arts, sens,
 * tailles, tables de capacités, catalogue d'armes) issu de creation.json,
 * produit au build par hooks/creation.py depuis les pages de règles : une seule
 * source de vérité, comme la Forge et l'Atelier.
 *
 * La présentation reprend les codes de la fiche Anima Beyond Fantasy de
 * Roll20 : feuille blanche centrée, en-tête d'identité sur lignes soulignées,
 * onglets en pilules (Général / Compétences / Formations / Arts / Équipement),
 * trois colonnes de blocs à titres serif, tables rayées, gros encadrés pour
 * les valeurs finales. Ce fichier ne porte que l'interface et les règles de
 * calcul prosaïques :
 *   - achat de caractéristiques : base 3, budget/moyenne/plafond selon l'Éclat
 *     (table de caracteristiques.md), 1 pt par cran jusqu'à la moyenne puis
 *     2, 3, 4… jusqu'au plafond ;
 *   - compétences : 5 PF = +20 de base, plafond de 5 PF par compétence et par
 *     niveau (points-formation.md) ; valeur = base + modificateur de carac ;
 *   - niveau = ⌈PF ÷ 100⌉ (points-formation.md) ;
 *   - PV max = (PV par niveau + modificateur de taille) × niveau (tailles.md) ;
 *   - familiarité des armes : −20 même famille, −40 famille étrangère
 *     (formations-martiales.md) ;
 *   - frappe d'un art martial : base + multiple du modificateur de Force
 *     (arts-martiaux.md).
 *
 * Les règles encore en chantier dans le livre (classes donc PV par niveau,
 * avantages, capital de PF et argent de départ, coût des arts) sont exposées en
 * champs réglables plutôt qu'inventées ici. Les personnages s'enregistrent dans
 * localStorage (« creation-persos ») et s'exportent/importent en JSON ; les
 * armes forgées (« forge-weapons ») sont proposées dans l'équipement.
 */
(function () {
  "use strict";

  var DATA = null;
  var state = null;
  var rootEl = null;
  var updaters = [];   // rafraîchisseurs des valeurs affichées sur la feuille

  // --- petites aides ---------------------------------------------------------
  function el(tag, cls, txt) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (txt != null) e.textContent = txt;
    return e;
  }
  function siteBase() {
    var l = document.querySelector('link[href*="assets/"], script[src*="assets/"]');
    var u = l ? (l.href || l.getAttribute("src")) : null;
    if (u) { var i = u.indexOf("assets/"); if (i >= 0) return u.slice(0, i); }
    return new URL(".", location.href).href;
  }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function num(v, d) { var n = parseInt(v, 10); return isNaN(n) ? d : n; }
  function fmt(n) {   // 8000 -> « 8 000 »
    var s = String(Math.abs(n)), out = "";
    while (s.length > 3) { out = " " + s.slice(-3) + out; s = s.slice(0, -3); }
    return (n < 0 ? "−" : "") + s + out;
  }
  function signed(n) { return n > 0 ? "+" + n : n < 0 ? "−" + (-n) : "+0"; }

  // --- état ------------------------------------------------------------------
  function blank() {
    return {
      v: 1,
      name: "", age: "", genre: "", tailleCm: "", poids: "", classe: "", notes: "",
      tailleCat: "Moyenne",
      pfTotal: 100, pvParNiveau: 100, argent: 0,
      eclatN: 10, eclatA: 10,
      caracs: { FOR: 3, DEX: 3, AGI: 3, END: 3, PER: 3, "PRÉ": 3, VOL: 3, LOG: 3, INS: 3, "ÉRU": 3, IMA: 3, CHA: 3 },
      comps: {},          // nom -> PF investis (multiples de 5)
      customComps: [],    // compétences personnalisées : [{ name, carac, pf, divers }]
      divers: {},         // nom de compétence -> bonus/malus divers (équipement, MJ...)
      modGlobal: 0,       // modificateur à toutes les actions (style « All Action Mod »)
      formations: [],     // [{ name, choix }]
      arts: {},           // nom -> « Basique » | « Avancé » | « Expert »
      armeDepart: "",
      armes: [],          // armes portées au combat : [{ name, forge }]
      inventaire: [],     // [{ name, prix, arme }]
      acuite: {},         // sens -> 0..10 (défaut 10)
      de: "1d100",        // dé des jets (seul dé nommé par les règles : critique-blessures)
      pv: null,           // PV courants (null = au maximum)
      fatigue: null,      // points de fatigue courants (réserve, max = Endurance ; null = au maximum)
      etatsActifs: {},    // nom d'état -> true, ou nom du palier
      avantages: [],      // lignes libres [{ name, note }] (la page du livre est en chantier)
      portrait: ""        // URL d'une image de personnage
    };
  }
  // Toute donnée entrante (localStorage, import JSON, bibliothèque) est
  // normalisée sur blank() : champ manquant -> valeur par défaut, type
  // inattendu -> ignoré. Sans cela, un personnage partiel planterait mount()
  // et l'état corrompu, autosauvegardé, casserait la page à chaque visite.
  function normalize(s) {
    if (!s || typeof s !== "object" || !s.caracs) return null;
    var b = blank();
    for (var k in b) {
      if (s[k] == null) continue;
      var want = Object.prototype.toString.call(b[k]);
      if (Object.prototype.toString.call(s[k]) !== want) continue;
      b[k] = s[k];
    }
    // valeurs imbriquées : on ne garde que ce qui a le bon type (un import
    // trafiqué ne doit ni planter le montage ni concaténer des chaînes)
    function numMap(m, lo, hi) {
      var o = {};
      for (var k2 in m) if (typeof m[k2] === "number" && isFinite(m[k2])) o[k2] = clamp(m[k2], lo, hi);
      return o;
    }
    var ref = blank().caracs, caracs = {};
    for (var a in ref) caracs[a] = typeof b.caracs[a] === "number" && isFinite(b.caracs[a]) ? clamp(b.caracs[a], 0, 30) : ref[a];
    b.caracs = caracs;
    b.comps = numMap(b.comps, 0, 9999);
    b.divers = numMap(b.divers, -9999, 9999);
    b.acuite = numMap(b.acuite, 0, 10);
    b.formations = b.formations.filter(function (f) { return f && typeof f.name === "string"; });
    b.customComps = b.customComps.filter(function (c) {
      return c && typeof c.name === "string" && typeof c.carac === "string";
    }).map(function (c) {
      c.pf = typeof c.pf === "number" && isFinite(c.pf) ? Math.max(0, c.pf) : 0;
      c.divers = typeof c.divers === "number" && isFinite(c.divers) ? c.divers : 0;
      return c;
    });
    b.armes = b.armes.filter(function (x) { return x && typeof x.name === "string"; });
    b.avantages = b.avantages.filter(function (x) { return x && typeof x === "object"; }).map(function (x) {
      return { name: typeof x.name === "string" ? x.name : "", note: typeof x.note === "string" ? x.note : "" };
    });
    var ea = {};
    for (var e in b.etatsActifs) if (b.etatsActifs[e] === true || typeof b.etatsActifs[e] === "string") ea[e] = b.etatsActifs[e];
    b.etatsActifs = ea;
    if (typeof s.pv === "number" && isFinite(s.pv)) b.pv = s.pv;           // null par défaut : le test de type l'aurait écarté
    if (typeof s.fatigue === "number" && isFinite(s.fatigue)) b.fatigue = clamp(s.fatigue, -30, 30);
    else b.fatigue = null;
    return b;
  }
  function save() {
    try { localStorage.setItem("creation-perso", JSON.stringify(state)); } catch (e) {}
    syncCards();
  }

  // --- cartes de jeu (pont vers l'extension navigateur) ---------------------------
  // L'extension Roll20 n'a pas le moteur : elle affiche une « carte » calculée,
  // structurée, produite ici (donc aucune règle dupliquée). On écrit dans
  // localStorage « creation-cards » un objet { id -> carte } que le content
  // script de l'extension recopie ; le brouillon en cours vit sous « _current ».
  function computeCard() {
    var g = modsGlobaux();
    var t0 = tailleCat();
    var comps = [];
    DATA.competences.forEach(function (k) {
      comps.push({ name: k.name, carac: caracAbbr(k.carac), champ: k.champ,
        total: compTotal(k.name), roll: compTotal(k.name) + g,
        invested: state.comps[k.name] > 0 || !!diversOf(k.name), accessible: k.accessible });
    });
    state.customComps.forEach(function (c) {
      comps.push({ name: c.name, carac: c.carac, champ: "Personnalisé",
        total: customTotal(c), roll: customTotal(c) + g, invested: c.pf > 0 || !!c.divers, custom: true });
    });
    var portees = DATA.armes.filter(function (a) { return a.corps; }).map(function (a) { return { a: a, name: a.name }; })
      .concat(state.armes.map(function (e) { return { a: armeByName(e.name), name: e.name, forge: e.forge }; }));
    var armes = portees.map(function (x) {
      if (!x.a) return { name: x.name, forge: x.forge, unknown: true };
      var lourd = lourdeurMalus(x.a);
      var atk = armeTypes(x.a).map(function (ty) {
        return { label: ty.label, roll: compTotal(ty.comp) + malusArme(x.a, ty.label) + lourd + g };
      });
      var md = modDegatsArme(x.a);
      return {
        name: x.name, corps: x.a.corps, famille: x.a.famille, am: x.a.am,
        attaques: atk,
        parade: /\bParade\b/.test(x.a.props) ? (compTotal("Parade") + malusArme(x.a, "Parade") + g) : null,
        degats: x.a.degats, mod: md.val, modTxt: md.txt, munitions: x.a.munitions
      };
    });
    var arts = Object.keys(state.arts).map(function (n) {
      var a = artByName(n), pal = state.arts[n], pd = null;
      (a && a.paliers || []).forEach(function (x) { if (x.niveau === pal) pd = x; });
      return { name: n, palier: pal, frappe: a && a.frappe ? frappeTxt(a, pal) : "", effet: pd && pd.effet ? pd.effet : "" };
    });
    var etats = [];
    (DATA.etats || []).forEach(function (e) {
      var v = state.etatsActifs[e.name];
      if (!v) return;
      var p = null;
      if (v !== true) e.paliers.forEach(function (x) { if (x.name === v) p = x; });
      var mods = (p ? p.mods : e.mods).map(function (m) { return m.cible + " " + signed(m.val); }).join(" · ");
      etats.push({ name: e.name + (p ? " (" + p.name + ")" : ""),
        effet: (e.name === "Abri" ? "subi par l'assaillant : " : "") + (mods || "voir la règle") });
    });
    return {
      name: state.name || "Personnage sans nom",
      portrait: state.portrait || "",
      de: state.de || "1d100",
      header: [
        "Niveau " + niveau() + " (" + fmt(state.pfTotal) + " PF)",
        "Éclat " + state.eclatA + (state.eclatA !== state.eclatN ? " (naissance " + state.eclatN + ")" : ""),
        state.classe ? "Classe : " + state.classe : null,
        state.age ? state.age + " ans" : null, state.genre || null,
        state.tailleCm ? state.tailleCm + " m" : null, state.poids ? state.poids + " kg" : null,
        "Taille " + state.tailleCat + (t0 && t0.pvMod ? " (" + signed(t0.pvMod) + " PV/niv)" : "")
      ].filter(Boolean),
      // en-tête d'identité structuré (l'extension reproduit la grille pc-id de la fiche)
      identity: {
        nom: state.name || "", classe: state.classe || "", genre: state.genre || "",
        age: state.age || "", taille: state.tailleCm || "", poids: state.poids || "",
        categorie: state.tailleCat || "", bourse: state.argent || 0,
        niveau: niveau(), pf: state.pfTotal, eclatA: state.eclatA, eclatN: state.eclatN
      },
      caracs: DATA.caracs.map(function (k) { return { abbr: k.abbr, name: k.name, groupe: k.groupe, val: caracVal(k.abbr), mod: modOf(caracVal(k.abbr)) }; }),
      combat: {
        pv: pvCourant(), pvMax: pvMax(),
        init: compTotal("Initiative") + g, esquive: compTotal("Esquive") + g, parade: compTotal("Parade") + g,
        fatigue: fatiguePts(), fatigueMax: caracVal("END"), modGlobal: g
      },
      capacites: {
        mouvement: capRow("mouvement", caracVal("AGI")) || [],
        port: capRow("port", caracVal("FOR")) || [],
        apnee: capRow("apnee", caracVal("END")) || [],
        sommeil: capRow("sommeil", caracVal("END")) || [],
        sommeilCols: DATA.capacites.sommeil ? DATA.capacites.sommeil.cols : []
      },
      competences: comps,
      armes: armes,
      arts: arts,
      formations: (state.armeDepart ? [{ name: "Arme de départ", info: state.armeDepart }] : []).concat(
        state.formations.map(function (f) { return { name: f.name + (f.choix ? " (" + f.choix + ")" : ""), info: "" }; })),
      sens: DATA.sens.filter(function (s) { return s.niveau !== "Inexistant" && s.niveau !== "Latent"; })
        .map(function (s) { return { name: s.name, niveau: s.niveau, acuite: state.acuite[s.name] != null ? state.acuite[s.name] : 10 }; }),
      avantages: state.avantages.filter(function (a) { return (a.name || "").trim(); }).map(function (a) { return { name: a.name, note: a.note || "" }; }),
      etats: etats,
      notes: state.notes || "",
      difficultes: DATA.difficultes
    };
  }
  function syncCards() {
    if (!DATA) return;
    var cards;
    try { cards = JSON.parse(localStorage.getItem("creation-cards")) || {}; } catch (e) { cards = {}; }
    if (typeof cards !== "object" || !cards) cards = {};
    var card = computeCard();
    card.id = "_current"; card.updated = nowStamp();
    cards._current = card;
    // si le brouillon porte le nom d'un personnage enregistré, on met sa carte à jour aussi
    loadPersos().forEach(function (p) {
      if (p.name === state.name) { var c = computeCard(); c.id = p.id; c.updated = nowStamp(); cards[p.id] = c; }
    });
    try { localStorage.setItem("creation-cards", JSON.stringify(cards)); } catch (e) {}
  }
  function syncAllCards() {
    if (!DATA) return;
    var cards = {};
    var keep = state;
    loadPersos().forEach(function (p) {
      var st = normalize(JSON.parse(JSON.stringify(p.state)));
      if (!st) return;
      state = st;
      var c = computeCard(); c.id = p.id; c.updated = nowStamp();
      cards[p.id] = c;
    });
    state = keep;
    var cur = computeCard(); cur.id = "_current"; cur.updated = nowStamp();
    cards._current = cur;
    try { localStorage.setItem("creation-cards", JSON.stringify(cards)); } catch (e) {}
  }
  // Date.now() est indisponible dans certains contextes de test ; on tolère.
  function nowStamp() { try { return Date.now(); } catch (e) { return 0; } }
  function load() {
    try {
      return normalize(JSON.parse(localStorage.getItem("creation-perso")));
    } catch (e) { return null; }
  }
  function curTab() { try { return localStorage.getItem("creation-tab") || "general"; } catch (e) { return "general"; } }
  function setTab(id) { try { localStorage.setItem("creation-tab", id); } catch (e) {} }

  // --- bibliothèque de personnages -------------------------------------------
  var PKEY = "creation-persos";
  function loadPersos() { try { var a = JSON.parse(localStorage.getItem(PKEY)); return Array.isArray(a) ? a : []; } catch (e) { return []; } }
  function savePersos(a) { try { localStorage.setItem(PKEY, JSON.stringify(a)); } catch (e) {} }
  function saveCurrentPerso() {
    var name = (state.name || "").trim();
    if (!name) { alert("Donnez un nom au personnage avant de l'enregistrer."); return; }
    var arr = loadPersos();
    var rec = { name: name, state: JSON.parse(JSON.stringify(state)) };
    var i = -1;
    for (var k = 0; k < arr.length; k++) if (arr[k].name === name) { i = k; break; }   // upsert par nom
    if (i >= 0) { rec.id = arr[i].id; arr[i] = rec; }
    else { rec.id = "p" + Date.now().toString(36) + Math.floor(Math.random() * 1e6).toString(36); arr.push(rec); }
    savePersos(arr); syncAllCards(); refresh();
  }
  function deletePerso(id) {
    savePersos(loadPersos().filter(function (p) { return p.id !== id; }));
    try {
      var cards = JSON.parse(localStorage.getItem("creation-cards")) || {};
      delete cards[id];
      localStorage.setItem("creation-cards", JSON.stringify(cards));
    } catch (e) {}
    refresh();
  }
  function loadPersoInto(p) { state = normalize(JSON.parse(JSON.stringify(p.state))) || blank(); if (rootEl) mount(rootEl); }

  // --- armes de la Forge (localStorage partagé) --------------------------------
  function forgedWeapons() { try { var a = JSON.parse(localStorage.getItem("forge-weapons")); return Array.isArray(a) ? a : []; } catch (e) { return []; } }

  // --- règles : caractéristiques et Éclat --------------------------------------
  function modOf(v) {
    v = clamp(v, 0, 30);
    var rows = DATA.caracTables.modificateurs;
    for (var i = 0; i < rows.length; i++) if (v >= rows[i].min && v <= rows[i].max) return rows[i].mod;
    return 0;
  }
  var CARAC_POINTS = 60, CARAC_MIN = 3, CARAC_MAX = 9;   // création : 60 points à répartir, chaque caractéristique de 3 à 9 (1 point = 1 point de carac)
  function caracMax() { return CARAC_MAX; }
  function caracSpent() {   // coût d'une caractéristique = sa valeur (base 3 comprise), sans surcoût
    var s = 0;
    for (var k in state.caracs) s += state.caracs[k];
    return s;
  }
  function caracVal(abbr) { return state.caracs[abbr] != null ? state.caracs[abbr] : CARAC_MIN; }

  // --- règles : PF, niveau, compétences ----------------------------------------
  function niveau() { return Math.max(1, Math.ceil((state.pfTotal || 0) / 100)); }
  function compPfMax() { return 5 * niveau(); }   // 5 PF max par compétence et par niveau
  function compByName(name) {
    for (var i = 0; i < DATA.competences.length; i++) if (DATA.competences[i].name === name) return DATA.competences[i];
    return null;
  }
  function compBase(name) { return ((state.comps[name] || 0) / 5) * 20; }
  function diversOf(name) { return state.divers[name] || 0; }
  function compTotal(name) {
    var c = compByName(name);
    if (!c) return 0;
    var abbr = caracAbbr(c.carac);
    return compBase(name) + modOf(caracVal(abbr)) + diversOf(name);
  }
  // Points de fatigue courants : réserve dont le maximum est l'Endurance
  // (capacites-physiques.md) ; null = au maximum. Chaque point SOUS ZÉRO donne
  // −10 à tous les jets ; à −Endurance, le personnage s'effondre.
  function fatiguePts() { return state.fatigue == null ? caracVal("END") : state.fatigue; }
  // Modificateurs qui pèsent sur TOUS les jets : réglage MJ/temporaire, et les
  // points de fatigue négatifs (−10 par point sous zéro).
  function modsGlobaux() { return (state.modGlobal || 0) + 10 * Math.min(0, fatiguePts()); }
  function pvCourant() { return state.pv == null ? pvMax() : state.pv; }
  var _abbrCache = null;
  function caracAbbr(nomComplet) {
    if (!_abbrCache) {
      _abbrCache = {};
      DATA.caracs.forEach(function (c) { _abbrCache[c.name] = c.abbr; });
    }
    return _abbrCache[nomComplet] || nomComplet;
  }
  function pfComps() {
    var s = 0;
    for (var k in state.comps) s += state.comps[k];
    state.customComps.forEach(function (c) { s += c.pf || 0; });
    return s;
  }
  function customTotal(c) { return ((c.pf || 0) / 5) * 20 + modOf(caracVal(c.carac)) + (c.divers || 0); }
  function pfFormations() {
    var s = 0;
    state.formations.forEach(function (f) {
      var d = formationByName(f.name);
      if (d && d.cout) s += d.cout;
    });
    return s;
  }
  function pfSpent() { return pfComps() + pfFormations(); }
  function formationByName(name) {
    for (var i = 0; i < DATA.formations.length; i++) if (DATA.formations[i].name === name) return DATA.formations[i];
    return null;
  }
  function formationCount(name) {
    return state.formations.filter(function (f) { return f.name === name; }).length;
  }
  // Attaque supplémentaire : 1 achat par tranche de 100 dans la MEILLEURE
  // compétence d'attaque (la plus haute, pas la somme). La valeur retenue est
  // celle de la compétence (base + modificateur), sans bonus divers ni global.
  var ATTAQUE_COMPS = ["Armes de mêlée", "Armes de jet", "Armes de trait", "Armes à feu"];
  function tranchesAttaque() {
    var best = 0;
    ATTAQUE_COMPS.forEach(function (n) {
      var c = compByName(n);
      if (!c) return;
      var t = compBase(n) + modOf(caracVal(caracAbbr(c.carac)));
      if (t > best) best = t;
    });
    return Math.floor(best / 100);
  }

  // --- règles : PV, taille, capacités ------------------------------------------
  function tailleCat() {
    for (var i = 0; i < DATA.tailles.length; i++) if (DATA.tailles[i].name === state.tailleCat) return DATA.tailles[i];
    return null;
  }
  function pvMax() {
    var t = tailleCat();
    return ((state.pvParNiveau || 0) + (t ? t.pvMod : 0)) * niveau();
  }
  function capRow(key, val) {
    var c = DATA.capacites[key];
    if (!c) return null;
    return c.rows[clamp(val, 0, 30)];
  }

  // --- règles : armes et familiarité -------------------------------------------
  function armeByName(name) {
    for (var i = 0; i < DATA.armes.length; i++) if (DATA.armes[i].name === name) return DATA.armes[i];
    return null;
  }
  function couverture() {
    var armes = {}, familles = {}, jet = false, projectiles = false;
    if (state.armeDepart) armes[state.armeDepart] = 1;
    state.formations.forEach(function (f) {
      if ((f.name === "Arme proche" || f.name === "Arme étrangère") && f.choix) armes[f.choix] = 1;
      if (f.name === "Famille entière" && f.choix) familles[f.choix] = 1;
      if (f.name === "Armes de jet") jet = true;
      if (f.name === "Armes à projectiles") projectiles = true;
    });
    var pratiquees = {};   // familles contenant au moins une arme connue
    for (var n in armes) { var a = armeByName(n); if (a && a.famille) pratiquees[a.famille] = 1; }
    for (var fam in familles) pratiquees[fam] = 1;
    return { armes: armes, familles: familles, pratiquees: pratiquees, jet: jet, projectiles: projectiles };
  }
  // Malus de familiarité pour un TYPE D'EMPLOI donné (« Mêlée », « Jet », « Tir »,
  // « Parade ») : 0 connue, −20 même famille, −40 sinon. Les formations Armes de
  // jet et Armes à projectiles n'unifient que le JET D'ATTAQUE de leur type
  // (formations-martiales.md : « la justesse du lancer est acquise ») : elles ne
  // couvrent ni la mêlée ni la parade.
  function malusArme(arme, type) {
    if (!arme || arme.corps) return 0;
    var c = couverture();
    if (c.armes[arme.name] || c.familles[arme.famille]) return 0;
    if (type === "Jet" && c.jet && arme.portee && arme.portee.indexOf("Jet") >= 0) return 0;
    if (type === "Tir" && c.projectiles && arme.famille === "Armes de trait") return 0;
    return c.pratiquees[arme.famille] ? -20 : -40;
  }
  function argentDepense() {
    var s = 0;
    state.inventaire.forEach(function (it) { s += it.prix || 0; });
    return s;
  }
  // Types d'attaque qu'une arme permet (manoeuvres.md : « parmi ceux que l'arme
  // permet », inférés de la portée et de la famille) et leur compétence.
  function armeTypes(a) {
    var out = [];
    if (/Mêlée|Allonge/.test(a.portee)) out.push({ label: "Mêlée", comp: "Armes de mêlée" });
    if (/Jet/.test(a.portee)) out.push({ label: "Jet", comp: "Armes de jet" });
    if (/Tir|Cône/.test(a.portee)) {
      var feu = /poudre|feu|explosifs/i.test(a.famille || "");
      out.push({ label: "Tir", comp: feu ? "Armes à feu" : "Armes de trait" });
    }
    return out;
  }
  // Lourdeur (armes.md) : Force minimale 5/7/9 ; −20 à l'attaque par point manquant.
  function lourdeurMalus(a) {
    var min = /Extrêmement lourde/.test(a.props) ? 9 : /Très lourde/.test(a.props) ? 7 : /\bLourde\b/.test(a.props) ? 5 : 0;
    return min ? -20 * Math.max(0, min - caracVal("FOR")) : 0;
  }
  // Modificateur de dégâts (armes.md) : « ×N FOR » = N × mod de Force (de
  // Dextérité avec Finesse) ; « +X » = propulsion fixe ; une seule source.
  function modDegatsArme(a) {
    var mm = /×(\d)\s*FOR/.exec(a.mod || "");
    if (mm) {
      var useDex = /Finesse/.test(a.props);
      var carac = useDex ? "DEX" : "FOR";
      return { txt: "×" + mm[1] + " " + carac, val: +mm[1] * modOf(caracVal(carac)) };
    }
    var pm = /^\+(\d+)/.exec(a.mod || "");
    if (pm) return { txt: "propulsion", val: +pm[1] };
    return { txt: "", val: 0 };
  }

  // --- règles : arts ------------------------------------------------------------
  var PALIERS = ["Basique", "Avancé", "Expert"];
  function artByName(name) {
    for (var i = 0; i < DATA.arts.length; i++) if (DATA.arts[i].name === name) return DATA.arts[i];
    return null;
  }
  function frappeTxt(art, palier) {
    if (!art.frappe) return null;
    var key = palier === "Expert" ? "expert" : palier === "Avancé" ? "avance" : "basique";
    var f = art.frappe[key];
    var mod = modOf(caracVal("FOR"));
    return f[0] + " + ×" + f[1] + " FOR = " + (f[0] + f[1] * mod);
  }

  // --- lanceur de dés et journal de jets -------------------------------------------
  // Jet = dé (configurable, défaut 1d100 : le seul dé que nomment les règles,
  // dans critique-blessures.md) + valeur de compétence + modificateur global.
  // Le journal vit en mémoire de session, il n'est pas exporté avec le personnage.
  var rollHistory = [];
  var rollPanel = null;
  function parseDice(expr) {
    var m = /^(\d{1,2})d(\d{1,4})([+-]\d{1,4})?$/.exec(String(expr || "").replace(/\s/g, ""));
    if (!m) return { n: 1, faces: 100, plus: 0 };
    return { n: clamp(+m[1], 1, 20), faces: clamp(+m[2], 2, 1000), plus: +(m[3] || 0) };
  }
  function bestDifficulty(total) {
    var best = null;
    DATA.difficultes.forEach(function (d) { if (total >= d.seuil && (!best || d.seuil > best.seuil)) best = d; });
    return best;
  }
  var spendSel = null;   // « se dépasser » : points de fatigue consommés sur le prochain jet
  function doRoll(label, value) {
    var d = parseDice(state.de);
    var dice = [];
    for (var i = 0; i < d.n; i++) dice.push(1 + Math.floor(Math.random() * d.faces));
    var sum = dice.reduce(function (a, b) { return a + b; }, 0) + d.plus;
    var global = modsGlobaux();   // avant dépense : le malus ne touche pas le jet qui crée les points
    var depense = spendSel ? clamp(num(spendSel.value, 0), 0, 5) : 0;
    var total = sum + value + global + 15 * depense;
    if (depense) {
      state.fatigue = fatiguePts() - depense;
      spendSel.value = "0";
    }
    rollHistory.unshift({
      label: label, dice: dice, sum: sum, plus: d.plus, value: value, global: global,
      depense: depense, total: total, palier: bestDifficulty(total)
    });
    if (rollHistory.length > 30) rollHistory.pop();
    renderRolls(true);
    if (depense) refresh();
  }
  function renderRolls(open) {
    if (!rollPanel) return;
    if (open) rollPanel.classList.add("open");
    var list = rollPanel.querySelector(".pc-rolls-list");
    list.innerHTML = "";
    if (!rollHistory.length) {
      list.appendChild(el("div", "pc-empty", "Aucun jet. Cliquer une valeur de compétence ou de combat pour lancer."));
      return;
    }
    rollHistory.forEach(function (r) {
      var row = el("div", "pc-roll");
      var head = el("div", "pc-roll-head");
      head.appendChild(el("span", "lbl", r.label));
      head.appendChild(el("span", "tot", String(r.total)));
      row.appendChild(head);
      var det = "dé " + r.dice.join(" + ") + (r.plus ? " " + signed(r.plus) : "") +
        (r.dice.length > 1 || r.plus ? " = " + r.sum : "") +
        " · valeur " + signed(r.value) +
        (r.global ? " · toutes actions " + signed(r.global) : "") +
        (r.depense ? " · dépassement +" + 15 * r.depense + " (" + r.depense + " pt" + (r.depense > 1 ? "s" : "") + ")" : "") +
        (r.palier ? " — atteint " + r.palier.name + " (" + r.palier.seuil + ")" : " — sous Triviale (0)");
      row.appendChild(el("div", "pc-roll-det", det));
      list.appendChild(row);
    });
  }
  var ROLL_HINT = "Cliquer pour lancer les dés.";
  function rollable(elm, labelFn, valueFn) {
    elm.classList.add("pc-rollable");
    elm.title = (elm.title ? elm.title + "\n" : "") + ROLL_HINT;
    elm.addEventListener("click", function () { doRoll(labelFn(), valueFn()); });
  }

  // --- avertissements -----------------------------------------------------------
  function warnings() {
    var w = [];
    if (caracSpent() > CARAC_POINTS) w.push("Le budget de caractéristiques est dépassé (" + caracSpent() + " / " + CARAC_POINTS + " points).");
    var cap = caracMax();
    var over = [];
    for (var k in state.caracs) if (state.caracs[k] > cap) over.push(k);
    if (over.length) w.push("Au-dessus du plafond de création (" + cap + ") : " + over.join(", ") + ".");
    if (pfSpent() > state.pfTotal) w.push("Les PF dépensés (" + pfSpent() + ") dépassent le capital (" + state.pfTotal + ").");
    var capPf = compPfMax(), overC = [];
    for (var n in state.comps) if (state.comps[n] > capPf) overC.push(n);
    state.customComps.forEach(function (c) { if ((c.pf || 0) > capPf) overC.push(c.name); });
    if (overC.length) w.push("Plus de " + capPf + " PF (5 par niveau) dans : " + overC.join(", ") + ".");
    var nAtk = formationCount("Attaque supplémentaire");
    if (nAtk > tranchesAttaque()) w.push("Attaque supplémentaire exige 100 points dans une même compétence d'attaque par achat (" + nAtk + " achat(s), " + tranchesAttaque() + " tranche(s) atteinte(s)).");
    // Arme proche exige une famille déjà pratiquée ; Arme étrangère, une famille
    // qui ne l'est pas encore. Le socle des familles pratiquées vient de l'arme
    // de départ, des Familles entières et des formations de famille ; les achats
    // s'y ajoutent ensuite dans l'ordre.
    var socle = {};
    var ad = armeByName(state.armeDepart);
    if (ad && ad.famille) socle[ad.famille] = 1;
    state.formations.forEach(function (f) {
      if (f.name === "Famille entière" && f.choix) socle[f.choix] = 1;
    });
    var vus = {};   // choix déjà pris (armes et familles)
    if (state.armeDepart) vus[state.armeDepart] = "l'arme de départ";
    state.formations.forEach(function (f) {
      var achat = f.name === "Arme proche" || f.name === "Arme étrangère" || f.name === "Famille entière";
      if (achat && !f.choix) { w.push(f.name + " : précisez l'arme ou la famille apprise."); return; }
      if (!achat || !f.choix) return;
      if (vus[f.choix]) w.push(f.name + " : « " + f.choix + " » est déjà " + vus[f.choix] + " (arme différente à chaque fois).");
      else vus[f.choix] = "apprise par une autre formation";
      var fam = null;
      if (f.name === "Famille entière") fam = f.choix;
      else { var a = armeByName(f.choix); fam = a && a.famille; }
      if (f.name === "Arme proche" && fam && !socle[fam]) w.push("Arme proche : « " + f.choix + " » (" + fam + ") vient d'une famille non pratiquée, il faut Arme étrangère (20 PF).");
      if (f.name === "Arme étrangère" && fam && socle[fam]) w.push("Arme étrangère : « " + f.choix + " » (" + fam + ") vient d'une famille déjà pratiquée, Arme proche suffit (10 PF).");
      if (fam) socle[fam] = 1;
    });
    if (argentDepense() > state.argent) w.push("L'équipement (" + fmt(argentDepense()) + " Ɉ) dépasse la bourse (" + fmt(state.argent) + " Ɉ).");
    if (state.eclatA !== state.eclatN) w.push("Éclat actuel ≠ Éclat de Naissance : réservé aux bascules rares en cours de vie.");
    if (caracVal("END") > 0 && fatiguePts() <= -caracVal("END")) w.push("Points de fatigue à −" + caracVal("END") + " : le personnage s'effondre d'épuisement (Inconscience).");
    if (pvCourant() <= 0) w.push("PV courants à 0 ou moins.");
    return w;
  }

  // --- rafraîchissement global ---------------------------------------------------
  var warnBox = null, meterBox = null, libSelect = null;
  function refresh() {
    updaters.forEach(function (u) { u(); });

    if (meterBox) {
      meterBox.innerHTML = "";
      [["Caractéristiques", caracSpent(), CARAC_POINTS, "pts"],
       ["Points de formation", pfSpent(), state.pfTotal, "PF"]].forEach(function (m) {
        var box = el("span", "pc-meter");
        box.appendChild(el("span", null, m[0]));
        var v = el("b", m[1] > m[2] ? "over" : "");
        v.textContent = fmt(m[1]) + " / " + fmt(m[2]) + " " + m[3];
        box.appendChild(v);
        var bar = el("span", "bar");
        var fill = el("i", m[1] > m[2] ? "over" : "");
        fill.style.width = clamp(m[2] ? (m[1] / m[2]) * 100 : 0, 0, 100) + "%";
        bar.appendChild(fill);
        box.appendChild(bar);
        meterBox.appendChild(box);
      });
    }

    if (warnBox) {
      warnBox.innerHTML = "";
      warnings().forEach(function (m) { warnBox.appendChild(el("div", "pc-warn", m)); });
    }

    if (libSelect) {
      var cur = libSelect.value;
      libSelect.innerHTML = "";
      var persos = loadPersos();
      var o0 = el("option"); o0.value = "";
      o0.textContent = "Personnages enregistrés (" + persos.length + ")";
      libSelect.appendChild(o0);
      persos.forEach(function (p) {
        var o = el("option"); o.value = p.id; o.textContent = p.name;
        libSelect.appendChild(o);
      });
      libSelect.value = cur && libSelect.querySelector('option[value="' + cur + '"]') ? cur : "";
    }

    save();
  }

  // --- fabriques ----------------------------------------------------------------
  function block(parent, title, sub, note) {
    var b = el("div", "pc-block");
    var t = el("div", "pc-block-title");
    t.appendChild(el("span", null, title));
    if (sub) t.appendChild(el("small", null, sub));
    b.appendChild(t);
    if (note) b.appendChild(el("div", "pc-block-note", note));
    parent.appendChild(b);
    return b;
  }
  function idField(box, span, label, value, onInput, opts) {
    opts = opts || {};
    var f = el("div", "pc-f " + span);
    var lb = el("label", null, label);
    if (opts.tip) { lb.title = opts.tip; f.title = opts.tip; }
    f.appendChild(lb);
    var input;
    if (opts.ro) {
      input = el("span", "pc-ro", value == null ? "" : String(value));
    } else if (opts.options) {
      input = el("select");
      opts.options.forEach(function (o) {
        var e = el("option"); e.value = o[0]; e.textContent = o[1];
        if (String(o[0]) === String(value)) e.selected = true;
        input.appendChild(e);
      });
      input.addEventListener("change", function () { onInput(input.value); refresh(); });
    } else {
      input = el("input");
      input.type = opts.type || "text";
      if (opts.min != null) input.min = opts.min;
      if (opts.placeholder) input.placeholder = opts.placeholder;
      input.value = value == null ? "" : value;
      input.addEventListener("input", function () { onInput(input.value); refresh(); });
    }
    f.appendChild(input);
    box.appendChild(f);
    return input;
  }
  function stepper(parent, get, set, min, max) {
    var box = el("span", "pc-step");
    var minus = el("button", null, "−"); minus.type = "button";
    var val = el("span", "v", String(get()));
    var plus = el("button", null, "+"); plus.type = "button";
    function sync() {
      val.textContent = String(get()).replace("-", "−");
      minus.disabled = get() <= min();
      plus.disabled = get() >= max();
    }
    minus.addEventListener("click", function () { if (get() > min()) { set(get() - 1); sync(); refresh(); } });
    plus.addEventListener("click", function () { if (get() < max()) { set(get() + 1); sync(); refresh(); } });
    box.appendChild(minus); box.appendChild(val); box.appendChild(plus);
    parent.appendChild(box);
    updaters.push(sync);
    return box;
  }

  // --- en-tête d'identité ---------------------------------------------------------
  function buildHead(sheet) {
    var head = el("div", "pc-head");
    var brand = el("div", "pc-brand");
    function syncBrand() {
      brand.innerHTML = "";
      if (state.portrait) {
        var img = el("img", "pc-portrait");
        img.src = state.portrait;
        img.alt = state.name || "Portrait";
        img.addEventListener("error", function () { img.style.display = "none"; });
        brand.appendChild(img);
      } else {
        brand.appendChild(el("span", "b1", "HxH"));
        brand.appendChild(el("span", "b2", "Système JDR"));
      }
      var pb = el("button", "pc-portrait-btn", state.portrait ? "changer" : "portrait…");
      pb.type = "button";
      pb.title = "Image du personnage (adresse d'une image en ligne).";
      pb.addEventListener("click", function () {
        var url = prompt("Adresse (URL) de l'image du personnage — vide pour retirer :", state.portrait || "");
        if (url === null) return;
        url = url.trim();
        if (url.length > 2000) { alert("Adresse trop longue : héberger l'image et coller son URL (pas l'image elle-même)."); return; }
        if (url && !/^https?:\/\//i.test(url)) { alert("L'adresse doit commencer par http:// ou https://."); return; }
        state.portrait = url;
        syncBrand(); refresh();
      });
      brand.appendChild(pb);
    }
    syncBrand();
    head.appendChild(brand);

    var grid = el("div", "pc-id");
    idField(grid, "c6", "Nom", state.name, function (v) { state.name = v; });
    idField(grid, "c3", "Classe", state.classe, function (v) { state.classe = v; },
      { tip: "Les classes sont en chantier dans les règles : champ libre." });
    idField(grid, "c3", "Genre", state.genre, function (v) { state.genre = v; });

    idField(grid, "c2", "Âge", state.age, function (v) { state.age = v; });
    idField(grid, "c2", "Taille (m)", state.tailleCm, function (v) { state.tailleCm = v; }, { placeholder: "1.75" });
    idField(grid, "c2", "Poids (kg)", state.poids, function (v) { state.poids = v; }, { placeholder: "70" });
    idField(grid, "c3", "Catégorie", state.tailleCat, function (v) { state.tailleCat = v; }, {
      options: DATA.tailles.map(function (t) {
        return [t.name, t.name + (t.pvMod ? " (" + signed(t.pvMod) + " PV/niv)" : "")];
      }),
      tip: "La taille fixe l'espace, l'allonge et le modificateur de PV. Moyenne = référence humaine (1.4 à 2.5 m)."
    });
    idField(grid, "c3", "Bourse (Ɉ)", state.argent, function (v) { state.argent = num(v, 0); },
      { type: "number", min: 0, tip: "Argent de départ, au choix du MJ. 1 Ɉ = 1 yen." });

    idField(grid, "c4", "Éclat de Naissance", state.eclatN, function (v) {
      var suit = state.eclatA === state.eclatN;   // l'actuel suit la naissance tant qu'on n'y a pas touché
      state.eclatN = num(v, 0);
      if (suit) state.eclatA = state.eclatN;
    }, {
      options: DATA.eclat.map(function (t) {
        return [t.val, "Éclat " + t.val + (t.plus ? " et au-delà" : "") + (t.naissance ? " — " + t.naissance : "")];
      }),
      tip: "Le MJ le fixe : 10 ou 15 pour la plupart, 20-25 pour les prodiges."
    });
    var eclatAIn = idField(grid, "c2", "Éclat actuel", state.eclatA, function (v) { state.eclatA = Math.max(0, num(v, 0)); },
      { type: "number", min: 0, tip: "Il part de l'Éclat de Naissance ; seules de rares bascules l'en écartent. Entre deux paliers, on retient le palier inférieur." });
    idField(grid, "c2", "Capital PF", state.pfTotal, function (v) { state.pfTotal = num(v, 0); },
      { type: "number", min: 0, tip: "Capital de points de formation, au choix du MJ. Niveau = ⌈PF ÷ 100⌉." });
    idField(grid, "c2", "PV / niveau", state.pvParNiveau, function (v) { state.pvParNiveau = num(v, 0); },
      { type: "number", min: 0, tip: "Viendra des classes (en chantier) : champ réglable." });
    var nivRo = idField(grid, "c2", "Niveau", niveau(), null, { ro: true });
    updaters.push(function () {
      nivRo.textContent = String(niveau());
      if (document.activeElement !== eclatAIn) eclatAIn.value = state.eclatA;
    });

    head.appendChild(grid);
    sheet.appendChild(head);

    meterBox = el("div", "pc-meters");
    sheet.appendChild(meterBox);
  }

  // --- onglets ---------------------------------------------------------------------
  function buildTabs(sheet) {
    var defs = [
      ["general", "Général"],
      ["formations", "Formations & Arts"],
      ["nen", "Nen"]
    ];
    var bar = el("div", "pc-tabs");
    var panes = {};
    var btns = {};
    defs.forEach(function (d) {
      var t = el("div", "pc-tab", d[1]);
      t.setAttribute("data-tab", d[0]);
      t.addEventListener("click", function () { show(d[0]); });
      bar.appendChild(t);
      btns[d[0]] = t;
      panes[d[0]] = el("div", "pc-pane");
    });
    sheet.appendChild(bar);
    warnBox = el("div", "pc-warns");
    sheet.appendChild(warnBox);
    defs.forEach(function (d) { sheet.appendChild(panes[d[0]]); });
    function show(id) {
      defs.forEach(function (d) {
        btns[d[0]].classList.toggle("on", d[0] === id);
        panes[d[0]].classList.toggle("on", d[0] === id);
      });
      setTab(id);
    }
    show(panes[curTab()] ? curTab() : "general");
    return panes;
  }

  // --- onglet Général -----------------------------------------------------------
  // Trois colonnes façon fiche Anima : deux colonnes étroites (caractéristiques,
  // éclat, combat, capacités, sens) et une colonne LARGE pour les compétences,
  // comme la colonne Secondary Abilities de la fiche de référence.
  function buildGeneral(pane) {
    var cols = el("div", "pc-cols3 pc-cols-gen");
    var colA = el("div", "pc-col"), colB = el("div", "pc-col"), colC = el("div", "pc-col pc-col-comps");
    cols.appendChild(colA); cols.appendChild(colB); cols.appendChild(colC);
    pane.appendChild(cols);

    // ----- colonne A : caractéristiques + éclat + notes -----
    var bC = block(colA, "Caractéristiques", null,
      "60 points à répartir · chaque caractéristique de 3 à 9 · 1 point par point");
    [["physique", "Physiques"], ["mentale", "Mentales"]].forEach(function (grp) {
      var head = el("div", "pc-trow pc-carac-row head");
      head.appendChild(el("span", null, ""));
      head.appendChild(el("span", null, grp[1]));
      head.appendChild(el("span", "pc-cell-num", "Valeur"));
      head.appendChild(el("span", "pc-cell-num", "Mod"));
      head.appendChild(el("span", "pc-cell-dim", "Coût"));
      bC.appendChild(head);
      DATA.caracs.filter(function (k) { return k.groupe === grp[0]; }).forEach(function (k) {
        var row = el("div", "pc-trow pc-carac-row");
        row.appendChild(el("span", "pc-abbr", k.abbr));
        var nm = el("span", null, k.name);
        nm.title = k.desc;
        row.appendChild(nm);
        stepper(row,
          function () { return caracVal(k.abbr); },
          function (v) { state.caracs[k.abbr] = v; },
          function () { return CARAC_MIN; },
          function () { return caracMax(); });
        var mod = el("span", "mod");
        var cost = el("span", "pc-cell-dim");
        updaters.push(function () {
          mod.textContent = signed(modOf(caracVal(k.abbr)));
          cost.textContent = caracVal(k.abbr) + " pts";
        });
        row.appendChild(mod); row.appendChild(cost);
        bC.appendChild(row);
      });
    });

    var bE = block(colA, "Éclat");
    var desc = el("div", "pc-eclat-desc");
    var info = el("div", "pc-eclat-info");
    var note = el("div", "pc-block-note");
    bE.appendChild(info); bE.appendChild(desc); bE.appendChild(note);
    updaters.push(function () {
      var palier = Math.floor(clamp(state.eclatA, 0, 999) / 5) * 5;
      info.innerHTML = "";
      [["Palier", String(palier)]].forEach(function (kv) {
        var s = el("span"); s.appendChild(document.createTextNode(kv[0] + " "));
        s.appendChild(el("b", null, kv[1])); info.appendChild(s);
      });
      var t = null;
      for (var i = 0; i < DATA.eclat.length; i++)
        if (DATA.eclat[i].val <= state.eclatN) t = DATA.eclat[i];
      desc.innerHTML = "";
      if (t) {
        desc.appendChild(document.createTextNode(t.desc));
        if (t.naissance) desc.appendChild(el("span", "n", "Naissance : " + t.naissance + "."));
      }
      note.textContent = state.eclatA > 50
        ? "Au-delà de 50, le livre ne fixe plus de répartition de création : l'outil reprend la ligne 45-50, au cadre du MJ."
        : "";
    });

    // Avantages et handicaps : lignes libres (avantages.md est en chantier)
    var bAv = block(colA, "Avantages et handicaps", null,
      "La page du livre est en chantier : lignes libres, à valider avec le MJ.");
    var avList = el("div", "pc-forma-buys");
    bAv.appendChild(avList);
    function renderAv() {
      avList.innerHTML = "";
      state.avantages.forEach(function (av) {
        var line = el("div", "pc-forma-buy");
        var nmIn = el("input"); nmIn.type = "text"; nmIn.placeholder = "Nom";
        nmIn.value = av.name || ""; nmIn.style.flex = "0 1 38%"; nmIn.style.fontWeight = "700";
        nmIn.addEventListener("input", function () { av.name = nmIn.value; save(); });
        line.appendChild(nmIn);
        var ntIn = el("input"); ntIn.type = "text"; ntIn.placeholder = "Effet, note";
        ntIn.value = av.note || "";
        ntIn.addEventListener("input", function () { av.note = ntIn.value; save(); });
        line.appendChild(ntIn);
        var db = el("button", "pc-mini danger", "×"); db.type = "button"; db.title = "Retirer";
        db.addEventListener("click", function () {
          var i = state.avantages.indexOf(av);
          if (i >= 0) state.avantages.splice(i, 1);
          renderAv(); save();
        });
        line.appendChild(db);
        avList.appendChild(line);
      });
      var add = el("button", "pc-mini", "+ Ajouter une ligne"); add.type = "button";
      add.addEventListener("click", function () { state.avantages.push({ name: "", note: "" }); renderAv(); save(); });
      avList.appendChild(add);
    }
    renderAv();

    var bN = block(colA, "Notes et histoire");
    var ta = el("textarea", "pc-notes");
    ta.value = state.notes;
    ta.addEventListener("input", function () { state.notes = ta.value; save(); });
    bN.appendChild(ta);

    // ----- colonne B : capacités physiques + combat + sens -----
    // étiquettes compactes pour les colonnes longues du livre
    var SHORT = {
      "Activité intermédiaire": "Act. inter.", "Activité lourde": "Act. lourde",
      "Avant de pouvoir redormir": "Redormir", "Avant d'être fatigué": "Fatigué"
    };
    var capDefs = [
      ["mouvement", "Mouvement", ["Marche", "Course", "Sprint"], "Distance par round (~6 s), mouvement passif."],
      ["port", "Port", ["Sans fatigue", "Vrai effort", "Pleine puiss."], "Charge portée, maniée, soulevée."],
      ["apnee", "Apnée", null, "Souffle retenu, selon l'activité du moment."],
      ["sommeil", "Sommeil et activité", null, "Sommeil requis et durées d'activité par jour ; puis veille minimale avant de redormir et durée avant d'être fatigué."]
    ];
    capDefs.forEach(function (d) {
      var cap = DATA.capacites[d[0]];
      if (!cap) return;
      var b = block(colB, d[1], "");
      b.title = d[3];
      var sub = b.querySelector(".pc-block-title small");
      var labels = d[2] || cap.cols.map(function (c) { return SHORT[c] || c; });
      var row = el("div", "pc-cap3" + (labels.length > 3 ? " pc-cap5" : ""));
      var cells = [];
      labels.forEach(function (lbl) {
        var c = el("div", "c");
        c.appendChild(el("span", "k", lbl));
        var v = el("span", "v", "");
        c.appendChild(v);
        cells.push(v);
        row.appendChild(c);
      });
      b.appendChild(row);
      updaters.push(function () {
        var val = caracVal(cap.carac);
        if (sub) sub.textContent = cap.carac + " " + val;
        var r = capRow(d[0], val) || [];
        cells.forEach(function (cell, i) { cell.textContent = r[i] || "—"; });
      });
    });

    var bF = block(colB, "Combat", null, "Valeurs = base + modificateur de carac + divers, et le modificateur à toutes les actions");
    var bigrow = el("div", "pc-bigrow");
    [["Initiative", "Initiative"], ["Esquive", "Esquive"], ["Parade", "Parade"]].forEach(function (d) {
      var box = el("div", "pc-big");
      box.appendChild(el("span", "k", d[0]));
      var v = el("span", "v", "");
      box.appendChild(v);
      updaters.push(function () {
        v.textContent = signed(compTotal(d[1]) + modsGlobaux());
        box.title = "Compétence " + signed(compTotal(d[1])) +
          (modsGlobaux() ? " · toutes actions " + signed(modsGlobaux()) : "") + "\n" + ROLL_HINT;
      });
      rollable(box, function () { return d[0]; }, function () { return compTotal(d[1]); });
      bigrow.appendChild(box);
    });
    bF.appendChild(bigrow);
    // modificateur à toutes les actions (blessures, circonstances, décision du MJ)
    var gm = el("div", "pc-kv");
    gm.appendChild(el("span", "k", "Mod. à toutes les actions"));
    var gmIn = el("input", "pc-comp-div");
    gmIn.type = "number"; gmIn.placeholder = "±";
    gmIn.value = state.modGlobal || "";
    gmIn.title = "S'ajoute à tous les jets (Initiative, Esquive, Parade et le reste) : malus de blessures, circonstances, décision du MJ.";
    gmIn.addEventListener("input", function () { state.modGlobal = num(gmIn.value, 0); refresh(); });
    gm.appendChild(gmIn);
    bF.appendChild(gm);

    // PV courants (suivi en jeu)
    var pvKv = el("div", "pc-kv");
    pvKv.appendChild(el("span", "k", "PV courants"));
    var pvIn = el("input", "pc-comp-div");
    pvIn.type = "number";
    pvIn.title = "PV du moment ; vide ou « max » = au maximum.";
    pvIn.addEventListener("input", function () {
      state.pv = pvIn.value === "" ? null : num(pvIn.value, 0);
      refresh();
    });
    pvKv.appendChild(pvIn);
    var pvMaxB = el("button", "pc-mini", "max"); pvMaxB.type = "button";
    pvMaxB.title = "Remettre les PV au maximum";
    pvMaxB.addEventListener("click", function () { state.pv = null; pvIn.value = ""; refresh(); });
    pvKv.appendChild(pvMaxB);
    bF.appendChild(pvKv);
    updaters.push(function () {
      if (document.activeElement !== pvIn) pvIn.value = state.pv == null ? "" : state.pv;
    });

    // Points de fatigue : réserve (max = Endurance), consommables +15/point sur
    // un jet (5 max) ; sous zéro, −10 par point ; effondrement à −Endurance.
    var ftKv = el("div", "pc-kv");
    var ftLbl = el("span", "k", "Points de fatigue");
    ftLbl.title = "Réserve : maximum = Endurance. Se dépasser : +15 au jet par point consommé (5 max par jet, via le panneau Jets). Sous zéro : −10 à tous les jets par point. À −Endurance : effondrement.";
    ftKv.appendChild(ftLbl);
    stepper(ftKv,
      function () { return fatiguePts(); },
      function (v) { state.fatigue = v; },
      function () { return -caracVal("END"); },
      function () { return caracVal("END"); });
    var ftMax = el("span", "pc-cell-dim");
    updaters.push(function () { ftMax.textContent = "/ " + caracVal("END"); });
    ftKv.appendChild(ftMax);
    bF.appendChild(ftKv);

    // Armes portées : attaque par type d'emploi, parade, dégâts ; familiarité
    // (−20/−40) et Lourdeur comptées dans l'attaque, familiarité dans la parade.
    var bA = block(colB, "Armes", null,
      "Attaque par type d'emploi et parade, familiarité et Lourdeur comptées ; cliquer une valeur pour lancer. Les trois armes de corps sont toujours disponibles.");
    var listA = el("div");
    bA.appendChild(listA);
    var addWrap = el("div");
    bA.appendChild(addWrap);
    function buildAddArme() {
      addWrap.innerHTML = "";
      var s = armeSelect("", function (v) {
        if (!v) return;
        state.armes.push({ name: v, forge: !armeByName(v) });
        buildAddArme(); refresh();
      });
      s.querySelector("option").textContent = "— porter une arme —";
      addWrap.appendChild(s);
    }
    buildAddArme();
    function armeRow(a, entry) {
      var box = el("div", "pc-arme");
      var head = el("div", "pc-arme-head");
      var nm = el("span", "nm", entry ? entry.name : a.name);
      head.appendChild(nm);
      head.appendChild(el("span", "fam", a ? (a.corps ? "arme de corps · " : "") + (a.famille || "") + (a.am ? " · AM " + a.am : "")
        : (entry && entry.forge ? "arme forgée (Forge)" : "hors barème")));
      if (entry) {
        var db = el("button", "pc-mini danger", "×"); db.type = "button"; db.title = "Ne plus porter cette arme";
        db.addEventListener("click", function () {
          var i = state.armes.indexOf(entry);
          if (i >= 0) state.armes.splice(i, 1);
          refresh();
        });
        head.appendChild(db);
      }
      box.appendChild(head);
      if (!a) {
        box.appendChild(el("div", "pc-arme-line", entry && entry.forge
          ? "Valeurs à l'appréciation du MJ : la fiche de cette arme vit dans la Forge."
          : "Arme absente du barème actuel (renommée ou retirée des règles)."));
        return box;
      }
      var line = el("div", "pc-arme-line");
      var lourd = lourdeurMalus(a);
      armeTypes(a).forEach(function (t) {
        var fam = malusArme(a, t.label);
        var val = compTotal(t.comp) + fam + lourd + modsGlobaux();
        var chip = el("span", "pc-wchip");
        chip.textContent = t.label + " " + signed(val);
        chip.title = t.comp + " " + signed(compTotal(t.comp)) +
          (fam ? " · familiarité " + signed(fam) : "") +
          (lourd ? " · Lourdeur " + signed(lourd) : "") +
          (modsGlobaux() ? " · toutes actions " + signed(modsGlobaux()) : "");
        rollable(chip, function () { return (entry ? entry.name : a.name) + " (" + t.label + ")"; },
          function () { return compTotal(t.comp) + malusArme(a, t.label) + lourdeurMalus(a); });
        line.appendChild(chip);
      });
      if (/\bParade\b/.test(a.props)) {
        var famP = malusArme(a, "Parade");
        var pv = compTotal("Parade") + famP + modsGlobaux();
        var pchip = el("span", "pc-wchip");
        pchip.textContent = "Parade " + signed(pv);
        pchip.title = "Parade " + signed(compTotal("Parade")) + (famP ? " · familiarité " + signed(famP) : "") +
          (modsGlobaux() ? " · toutes actions " + signed(modsGlobaux()) : "");
        rollable(pchip, function () { return (entry ? entry.name : a.name) + " (Parade)"; },
          function () { return compTotal("Parade") + malusArme(a, "Parade"); });
        line.appendChild(pchip);
      }
      var md = modDegatsArme(a);
      var dmg = el("span", "dmg", "Dégâts " + a.degats + (md.val || md.txt ? " " + signed(md.val) + (md.txt ? " (" + md.txt + ")" : "") : ""));
      dmg.title = "Dégâts de l'arme, plus son modificateur (une seule source, armes.md). Blesser : dégâts × degré de touche ÷ 100.";
      line.appendChild(dmg);
      if (a.munitions) line.appendChild(el("span", "mun", "Munitions " + a.munitions));
      box.appendChild(line);
      var notes = [];
      var famGen = malusArme(a);
      if (famGen) notes.push("familiarité " + signed(famGen) + " (attaque et parade)");
      if (lourd) notes.push("Force insuffisante : " + signed(lourd) + " à l'attaque");
      if (notes.length) box.appendChild(el("div", "pc-arme-warn", notes.join(" · ")));
      return box;
    }
    function renderArmes() {
      listA.innerHTML = "";
      DATA.armes.filter(function (a) { return a.corps; }).forEach(function (a) {
        listA.appendChild(armeRow(a, null));
      });
      state.armes.forEach(function (entry) {
        listA.appendChild(armeRow(armeByName(entry.name), entry));
      });
    }
    updaters.push(renderArmes);

    // États (etats.md) : cocher pour mémoire ; la plupart des malus ne valent
    // que contre l'adversaire qui les cause, ils ne sont donc PAS appliqués
    // automatiquement aux jets.
    if (DATA.etats && DATA.etats.length) {
      var bEt = block(colB, "États", null,
        "Cliquer un état pour le noter (re-cliquer pour changer de palier ou l'ôter). Les Situations ne valent qu'en opposition à l'adversaire qui les cause ; les autres états s'appliquent à tous les jets concernés. Rien n'est appliqué automatiquement : reporter soi-même.");
      var chipBox = el("div", "pc-chips");
      var summary = el("div", "pc-etat-sum");
      function modsTxt(mods) {
        return mods.map(function (m) { return m.cible + " " + signed(m.val); }).join(" · ");
      }
      DATA.etats.forEach(function (e) {
        var chip = el("span", "pc-chip");
        function curPalier() {
          var v = state.etatsActifs[e.name];
          if (!v || v === true) return null;
          for (var i = 0; i < e.paliers.length; i++) if (e.paliers[i].name === v) return e.paliers[i];
          return null;
        }
        function sync() {
          var v = state.etatsActifs[e.name];
          chip.textContent = e.name + (v && v !== true ? " · " + v : "");
          chip.classList.toggle("on", !!v);
          var p = curPalier();
          var mods = p ? p.mods : e.mods;
          // la description générale porte souvent la règle d'application (ex.
          // Abri : le malus est subi par l'assaillant) : on la garde toujours
          chip.title = (p && p.desc ? p.desc + "\n" : "") + (e.desc || "") + (mods.length ? "\n" + modsTxt(mods) : "");
        }
        chip.addEventListener("click", function () {
          var v = state.etatsActifs[e.name];
          if (e.paliers.length) {
            var names = e.paliers.map(function (p) { return p.name; });
            var i = v && v !== true ? names.indexOf(v) : -1;
            if (i + 1 < names.length) state.etatsActifs[e.name] = names[i + 1];
            else delete state.etatsActifs[e.name];
          } else {
            if (v) delete state.etatsActifs[e.name]; else state.etatsActifs[e.name] = true;
          }
          sync(); refresh();
        });
        sync();
        chipBox.appendChild(chip);
      });
      bEt.appendChild(chipBox);
      bEt.appendChild(summary);
      updaters.push(function () {
        summary.innerHTML = "";
        DATA.etats.forEach(function (e) {
          var v = state.etatsActifs[e.name];
          if (!v) return;
          var p = null;
          if (v !== true) e.paliers.forEach(function (x) { if (x.name === v) p = x; });
          var mods = p ? p.mods : e.mods;
          var line = el("div", "pc-etat-line");
          line.appendChild(el("b", null, e.name + (p ? " (" + p.name + ")" : "") + " : "));
          // Abri inverse le sens : c'est l'assaillant qui subit les malus
          var prefix = e.name === "Abri" ? "subi par l'assaillant : " : "";
          var suffix = /situation/i.test(e.categorie || "") ? " — en opposition" : " — sur ses propres jets";
          line.appendChild(document.createTextNode(prefix + (mods.length ? modsTxt(mods) : "voir la règle") + suffix));
          summary.appendChild(line);
        });
      });
    }
    var pvRow = el("div", "pc-bigrow");
    pvRow.style.marginTop = ".55rem";
    var pvBox = el("div", "pc-big red");
    pvBox.appendChild(el("span", "k", "PV"));
    var pvV = el("span", "v", "");
    pvV.style.fontSize = "1.1rem"; pvV.style.paddingTop = ".18rem";
    pvBox.appendChild(pvV);
    pvRow.appendChild(pvBox);
    var mvBox = el("div", "pc-big");
    mvBox.appendChild(el("span", "k", "Mouvement"));
    var mvV = el("span", "v", "");
    mvV.style.fontSize = ".95rem"; mvV.style.paddingTop = ".28rem";
    mvBox.appendChild(mvV);
    pvRow.appendChild(mvBox);
    var adBox = el("div", "pc-big");
    adBox.appendChild(el("span", "k", "Arme de départ"));
    var adV = el("span", "v", "");
    adV.style.fontSize = ".8rem"; adV.style.paddingTop = ".34rem";
    adBox.appendChild(adV);
    pvRow.appendChild(adBox);
    bF.appendChild(pvRow);
    updaters.push(function () {
      pvV.textContent = fmt(pvCourant()) + " / " + fmt(pvMax());
      pvBox.title = "PV courants / PV max";
      var mv = capRow("mouvement", caracVal("AGI"));
      mvV.textContent = mv ? mv[0] + " · " + mv[1] : "—";
      adV.textContent = state.armeDepart || "—";
    });
    var pvNote = el("div", "pc-block-note");
    pvNote.style.marginTop = ".3rem";
    updaters.push(function () {
      var t = tailleCat();
      pvNote.textContent = "PV max = (PV par niveau " + (t && t.pvMod ? signed(t.pvMod) + " taille " : "") + ") × niveau " + niveau() +
        (t ? " · espace " + t.espace + " · allonge " + t.allonge : "");
    });
    bF.appendChild(pvNote);

    ["externe", "interne"].forEach(function (typ) {
      var b = block(colB, typ === "externe" ? "Sens externes" : "Sens internes", null,
        "Acuité de 0 à 10, départ 10 ; elle chute en jeu, pas à la création.");
      var head = el("div", "pc-trow pc-sens-row head");
      head.appendChild(el("span", null, "Sens"));
      head.appendChild(el("span", "niv", "Niveau"));
      head.appendChild(el("span", "pc-cell-num", "Acuité"));
      b.appendChild(head);
      var ordre = { "Primaire": 0, "Secondaire": 1, "Tertiaire": 2, "Latent": 3, "Inexistant": 4 };
      DATA.sens
        .filter(function (s) { return s.type === typ && s.niveau !== "Inexistant"; })
        .sort(function (x, y) { return (ordre[x.niveau] || 0) - (ordre[y.niveau] || 0); })
        .forEach(function (s) {
          var row = el("div", "pc-trow pc-sens-row");
          var latent = s.niveau === "Latent";
          var nm = el("span", "nm" + (latent ? " latent" : ""), s.name);
          nm.title = s.desc + (latent ? "\nFaculté endormie : s'éveille sous condition spéciale." : "");
          row.appendChild(nm);
          row.appendChild(el("span", "niv", s.niveau));
          if (latent) {
            row.appendChild(el("span", "niv", "endormi"));
          } else {
            stepper(row,
              function () { return state.acuite[s.name] != null ? state.acuite[s.name] : 10; },
              function (v) { if (v === 10) delete state.acuite[s.name]; else state.acuite[s.name] = v; },
              function () { return 0; },
              function () { return 10; });
          }
          b.appendChild(row);
        });
    });

    // ----- colonne C, la grande : compétences -----
    buildCompetences(colC);
  }

  // --- compétences (grande colonne de l'onglet Général) -----------------------------
  function buildCompetences(pane) {
    var b = block(pane, "Compétences", null,
      "5 PF = +20 de base · 5 PF max par compétence et par niveau · valeur = base + modificateur de carac + divers (colonne ±)");

    var tools = el("div", "pc-comp-tools");
    var search = el("input", "pc-comp-search");
    search.type = "search"; search.placeholder = "Filtrer les compétences…";
    tools.appendChild(search);
    var champs = [];
    DATA.competences.forEach(function (k) { if (champs.indexOf(k.champ) < 0) champs.push(k.champ); });
    var champSel = el("select", "pc-select");
    ["Tous les champs"].concat(champs).concat(["Personnalisé"]).forEach(function (ch) {
      var o = el("option"); o.value = ch === "Tous les champs" ? "" : ch; o.textContent = ch;
      champSel.appendChild(o);
    });
    tools.appendChild(champSel);
    var onlyChip = el("span", "pc-chip");
    onlyChip.textContent = "Investies seulement";
    var only = false;
    onlyChip.addEventListener("click", function () { only = !only; onlyChip.classList.toggle("on", only); render(); });
    tools.appendChild(onlyChip);
    b.appendChild(tools);

    var list = el("div", "pc-comp-list one");
    b.appendChild(list);

    // ajout d'une compétence personnalisée (hors règles, à valider avec le MJ)
    var addBar = el("div", "pc-comp-tools");
    addBar.style.marginTop = ".5rem";
    var addName = el("input", "pc-comp-search");
    addName.type = "text"; addName.placeholder = "Compétence personnalisée (nom)…";
    var addCarac = el("select", "pc-select");
    DATA.caracs.forEach(function (k) {
      var o = el("option"); o.value = k.abbr; o.textContent = k.abbr + " — " + k.name;
      addCarac.appendChild(o);
    });
    var addBtn = el("button", "pc-mini", "+ Ajouter"); addBtn.type = "button";
    addBtn.addEventListener("click", function () {
      var n = addName.value.trim();
      if (!n) return;
      state.customComps.push({ name: n, carac: addCarac.value, pf: 0, divers: 0 });
      addName.value = "";
      render();
    });
    addBar.appendChild(addName); addBar.appendChild(addCarac); addBar.appendChild(addBtn);
    b.appendChild(addBar);

    // Les lignes sont recréées à chaque filtre : leurs rafraîchisseurs vivent
    // dans rowSync (vidé au re-rendu) derrière un unique updater global, sinon
    // chaque recherche empilerait des rafraîchisseurs de nœuds détachés.
    var rowSync = [];
    updaters.push(function () { rowSync.forEach(function (f) { f(); }); });

    function pips(u) { return "●●●●●".slice(0, u) + "○○○○○".slice(0, 5 - u); }
    function render() {
      list.innerHTML = "";
      rowSync.length = 0;
      var q = search.value.trim().toLowerCase();
      var champ = champSel.value;
      var cur = null;
      DATA.competences.forEach(function (k) {
        if (champ && k.champ !== champ) return;
        if (q && k.name.toLowerCase().indexOf(q) < 0) return;
        if (only && !(state.comps[k.name] > 0) && !diversOf(k.name)) return;
        if (k.champ !== cur) { cur = k.champ; list.appendChild(el("div", "pc-comp-champ", "Champ " + cur)); }
        var row = el("div", "pc-comp-row");
        var nm = el("span", "pc-comp-name" + (k.accessible ? "" : " na"));
        nm.appendChild(document.createTextNode(k.name + (k.accessible ? " " : " * ")));
        nm.appendChild(el("span", "u", pips(k.utilite)));
        nm.title = k.desc + "\nGroupes : " + k.groupes.join(", ") + (k.accessible ? "" : "\nHors de portée d'un humain ordinaire.");
        row.appendChild(nm);
        var abbr = el("span", "pc-comp-carac", caracAbbr(k.carac));
        abbr.title = k.carac;
        row.appendChild(abbr);
        stepperPf(row, k.name);
        var div = el("input", "pc-comp-div");
        div.type = "number"; div.placeholder = "±";
        div.value = diversOf(k.name) || "";
        div.title = "Bonus ou malus divers (équipement, circonstance, décision du MJ)";
        div.addEventListener("input", function () {
          var v = num(div.value, 0);
          if (v) state.divers[k.name] = v; else delete state.divers[k.name];
          refresh();
        });
        row.appendChild(div);
        var tot = el("span", "pc-comp-total");
        rowSync.push(function () {
          var t = compTotal(k.name);
          tot.textContent = signed(t);
          tot.classList.toggle("zero", !(state.comps[k.name] > 0) && !diversOf(k.name));
          tot.title = "Base +" + compBase(k.name) + " · Carac " + signed(modOf(caracVal(caracAbbr(k.carac)))) +
            (diversOf(k.name) ? " · Divers " + signed(diversOf(k.name)) : "") + "\n" + ROLL_HINT;
        });
        rollable(tot, function () { return k.name; }, function () { return compTotal(k.name); });
        row.appendChild(tot);
        list.appendChild(row);
      });
      // compétences personnalisées (lignes ajoutées par le joueur)
      var customs = state.customComps.filter(function (c) {
        return (!q || c.name.toLowerCase().indexOf(q) >= 0) &&
               (!champ || champ === "Personnalisé") &&
               (!only || (c.pf || 0) > 0 || c.divers);
      });
      if (customs.length) {
        list.appendChild(el("div", "pc-comp-champ", "Champ Personnalisé"));
        customs.forEach(function (c) { list.appendChild(customRow(c)); });
      }
      refresh();
    }
    function customRow(c) {
      var row = el("div", "pc-comp-row");
      var nm = el("span", "pc-comp-name");
      var db = el("button", "pc-mini danger", "×"); db.type = "button";
      db.title = "Retirer cette compétence personnalisée";
      db.style.marginRight = ".35rem";
      db.addEventListener("click", function () {
        var i = state.customComps.indexOf(c);
        if (i >= 0) state.customComps.splice(i, 1);
        render();
      });
      nm.appendChild(db);
      nm.appendChild(document.createTextNode(c.name));
      nm.title = "Compétence personnalisée, hors des règles : à valider avec le MJ.";
      row.appendChild(nm);
      row.appendChild(el("span", "pc-comp-carac", c.carac));
      var box = el("span", "pc-step");
      var minus = el("button", null, "−"); minus.type = "button";
      var val = el("span", "v", "0");
      var plus = el("button", null, "+"); plus.type = "button";
      function sync() {
        val.textContent = c.pf ? "+" + ((c.pf / 5) * 20) : "0";
        val.title = (c.pf || 0) + " PF investis";
        minus.disabled = !(c.pf > 0);
        plus.disabled = (c.pf || 0) >= compPfMax();
      }
      minus.addEventListener("click", function () { c.pf = Math.max(0, (c.pf || 0) - 5); sync(); refresh(); });
      plus.addEventListener("click", function () { if ((c.pf || 0) < compPfMax()) { c.pf = (c.pf || 0) + 5; sync(); refresh(); } });
      box.appendChild(minus); box.appendChild(val); box.appendChild(plus);
      row.appendChild(box);
      var div = el("input", "pc-comp-div");
      div.type = "number"; div.placeholder = "±";
      div.value = c.divers || "";
      div.title = "Bonus ou malus divers";
      div.addEventListener("input", function () { c.divers = num(div.value, 0); refresh(); });
      row.appendChild(div);
      var tot = el("span", "pc-comp-total");
      rowSync.push(function () {
        tot.textContent = signed(customTotal(c));
        tot.classList.toggle("zero", !(c.pf > 0) && !c.divers);
        tot.title = "Base +" + ((c.pf || 0) / 5) * 20 + " · Carac " + signed(modOf(caracVal(c.carac))) +
          (c.divers ? " · Divers " + signed(c.divers) : "") + "\n" + ROLL_HINT;
      });
      rollable(tot, function () { return c.name; }, function () { return customTotal(c); });
      row.appendChild(tot);
      rowSync.push(sync);
      sync();
      return row;
    }
    function stepperPf(row, name) {   // stepper en pas de 5 PF
      var box = el("span", "pc-step");
      var minus = el("button", null, "−"); minus.type = "button";
      var val = el("span", "v", "0");
      var plus = el("button", null, "+"); plus.type = "button";
      function get() { return state.comps[name] || 0; }
      function sync() {
        val.textContent = get() ? "+" + compBase(name) : "0";
        val.title = get() + " PF investis";
        minus.disabled = get() <= 0;
        plus.disabled = get() >= compPfMax();
      }
      minus.addEventListener("click", function () {
        var v = get() - 5;
        if (v <= 0) delete state.comps[name]; else state.comps[name] = v;
        sync(); refresh();
      });
      plus.addEventListener("click", function () {
        if (get() < compPfMax()) { state.comps[name] = get() + 5; sync(); refresh(); }
      });
      box.appendChild(minus); box.appendChild(val); box.appendChild(plus);
      row.appendChild(box);
      rowSync.push(sync);
      sync();
    }
    search.addEventListener("input", render);
    champSel.addEventListener("change", render);
    render();
  }

  // --- onglet Formations ------------------------------------------------------------
  function buildFormations(pane) {
    var bD = block(pane, "Arme de départ", null,
      "Un personnage développe son attaque et sa défense avec une arme précise, choisie dès le départ. Les autres armes subissent −20 (même famille) ou −40 (famille étrangère) en attaque et parade.");
    bD.appendChild(armeSelect(state.armeDepart, function (v) { state.armeDepart = v; refresh(); }));

    var bF = block(pane, "Formations", null,
      "Payées en PF, acquises pour de bon ; seules les martiales sont écrites à ce jour.");
    var grid = el("div", "pc-arts3");
    bF.appendChild(grid);

    DATA.formations.forEach(function (f) {
      var box = el("div", "pc-forma");
      var head = el("div", "pc-forma-head");
      var nm = el("span", "nm", f.name);
      nm.title = f.desc;
      head.appendChild(nm);
      head.appendChild(el("span", "cost", f.cout + " PF"));
      box.appendChild(head);
      var body = el("div", "pc-forma-body");
      var noteInterp = f.name === "Attaque supplémentaire"
        ? " La valeur retenue ici est celle de la compétence (base + modificateur)." : "";
      body.appendChild(el("div", "pc-forma-hint",
        f.tagline + (f.prereq && f.prereq !== "aucun" ? " — Prérequis : " + f.prereq + "." + noteInterp : "")));
      var buys = el("div", "pc-forma-buys");
      body.appendChild(buys);
      box.appendChild(body);
      grid.appendChild(box);

      var needsChoix = f.name === "Arme proche" || f.name === "Arme étrangère" || f.name === "Famille entière";
      function render() {
        buys.innerHTML = "";
        state.formations.forEach(function (entry) {
          if (entry.name !== f.name) return;
          var line = el("div", "pc-forma-buy");
          if (needsChoix) {
            if (f.name === "Famille entière") {
              line.appendChild(familleSelect(entry.choix, function (v) { entry.choix = v; refresh(); }));
            } else {
              line.appendChild(armeSelect(entry.choix, function (v) { entry.choix = v; refresh(); }));
            }
          } else {
            var lbl = el("input"); lbl.type = "text"; lbl.value = entry.choix || "";
            lbl.placeholder = "Note (facultatif)";
            lbl.addEventListener("input", function () { entry.choix = lbl.value; save(); });
            line.appendChild(lbl);
          }
          var db = el("button", "pc-mini danger", "×"); db.type = "button"; db.title = "Retirer cet achat";
          db.addEventListener("click", function () {
            // par identité d'objet : un index capturé au rendu se périme dès
            // qu'une suppression a lieu dans une autre carte
            var i = state.formations.indexOf(entry);
            if (i >= 0) state.formations.splice(i, 1);
            render(); refresh();
          });
          line.appendChild(db);
          buys.appendChild(line);
        });
        var add = el("button", "pc-mini", formationCount(f.name) ? "+ Suivre encore (" + f.cout + " PF)" : "+ Suivre (" + f.cout + " PF)");
        add.type = "button";
        if (!f.repetable && formationCount(f.name) >= 1 && f.name !== "Famille entière") add.disabled = true;
        add.addEventListener("click", function () { state.formations.push({ name: f.name, choix: "" }); render(); refresh(); });
        buys.appendChild(add);
      }
      render();
    });
  }

  function armeSelect(cur, onPick) {
    var s = el("select", "pc-select");
    var none = el("option"); none.value = ""; none.textContent = "— choisir une arme —"; s.appendChild(none);
    var fam = null, group = null;
    DATA.armes.forEach(function (a) {
      if (a.corps) return;
      if (a.famille !== fam) { fam = a.famille; group = el("optgroup"); group.label = fam; s.appendChild(group); }
      var o = el("option"); o.value = a.name; o.textContent = a.name;
      if (a.name === cur) o.selected = true;
      group.appendChild(o);
    });
    forgedWeapons().forEach(function (w) {
      if (!group || group.label !== "Armes forgées") { group = el("optgroup"); group.label = "Armes forgées"; s.appendChild(group); }
      var o = el("option"); o.value = w.name; o.textContent = w.name;
      if (w.name === cur) o.selected = true;
      group.appendChild(o);
    });
    s.addEventListener("change", function () { onPick(s.value); });
    return s;
  }
  function familleSelect(cur, onPick) {
    var s = el("select", "pc-select");
    var none = el("option"); none.value = ""; none.textContent = "— choisir une famille —"; s.appendChild(none);
    var seen = {};
    DATA.armes.forEach(function (a) {
      if (a.corps || seen[a.famille]) return;
      seen[a.famille] = 1;
      var o = el("option"); o.value = a.famille; o.textContent = a.famille;
      if (a.famille === cur) o.selected = true;
      s.appendChild(o);
    });
    s.addEventListener("change", function () { onPick(s.value); });
    return s;
  }

  // --- onglet Arts --------------------------------------------------------------------
  function buildArts(pane) {
    var b = block(pane, "Arts", null,
      "Coûts et prérequis en chantier dans les règles : choix libre du palier, à valider avec le MJ.");
    var tools = el("div", "pc-comp-tools");
    var search = el("input", "pc-comp-search");
    search.type = "search"; search.placeholder = "Filtrer les arts…";
    tools.appendChild(search);
    var onlyChip = el("span", "pc-chip", "Choisis seulement");
    var only = false;
    onlyChip.addEventListener("click", function () { only = !only; onlyChip.classList.toggle("on", only); render(); });
    tools.appendChild(onlyChip);
    b.appendChild(tools);
    var wrap = el("div");
    b.appendChild(wrap);

    // même mécanique que les compétences : rafraîchisseurs locaux vidés au re-rendu
    var artSync = [];
    updaters.push(function () { artSync.forEach(function (f) { f(); }); });

    function render() {
      wrap.innerHTML = "";
      artSync.length = 0;
      var q = search.value.trim().toLowerCase();
      var cats = [];
      DATA.arts.forEach(function (a) { if (cats.indexOf(a.categorie) < 0) cats.push(a.categorie); });
      cats.forEach(function (cat) {
        var arts = DATA.arts.filter(function (a) {
          return a.categorie === cat &&
            (!q || a.name.toLowerCase().indexOf(q) >= 0) &&
            (!only || state.arts[a.name]);
        });
        if (!arts.length) return;
        wrap.appendChild(el("div", "pc-comp-champ", "Arts " + cat));
        var g = el("div", "pc-arts3");
        arts.forEach(function (a) { g.appendChild(artCard(a)); });
        wrap.appendChild(g);
      });
      refresh();
    }
    function artCard(a) {
      var box = el("div", "pc-art-card");
      var head = el("div", "pc-art-head");
      head.appendChild(el("span", "pc-art-name", a.name));
      head.appendChild(el("span", "pc-art-tag", a.tagline));
      box.appendChild(head);
      if (a.desc) { var d = el("div", "pc-art-effet", a.desc); d.style.color = "var(--ink-3)"; box.appendChild(d); }
      if (a.todo) box.appendChild(el("div", "pc-art-todo", "Fiche en chantier dans les règles."));
      var seg = el("div", "pc-seg");
      var effet = el("div", "pc-art-effet");
      var frappe = el("div", "pc-art-frappe");
      ["Aucun"].concat(PALIERS).forEach(function (p) {
        var cur = state.arts[a.name] || "Aucun";
        var btn = el("button", "pc-seg-btn" + (cur === p ? " on" : ""));
        btn.type = "button"; btn.textContent = p === "Aucun" ? "—" : p;
        if (p !== "Aucun") {
          var pd = paliersOf(a)[p];
          if (pd && (pd.effet || pd.flavor)) btn.title = (pd.flavor ? pd.flavor + "\n" : "") + (pd.effet ? "Effet : " + pd.effet : "");
        }
        btn.addEventListener("click", function () {
          seg.querySelectorAll(".pc-seg-btn").forEach(function (x) { x.classList.remove("on"); });
          btn.classList.add("on");
          if (p === "Aucun") delete state.arts[a.name]; else state.arts[a.name] = p;
          syncDetail(); refresh();
        });
        seg.appendChild(btn);
      });
      function syncDetail() {
        var p = state.arts[a.name];
        var pd = p ? paliersOf(a)[p] : null;
        effet.textContent = pd && pd.effet ? pd.effet : "";
        var f = p ? frappeTxt(a, p) : null;
        frappe.textContent = f ? "Frappe : " + f : "";
      }
      artSync.push(syncDetail);
      box.appendChild(seg); box.appendChild(frappe); box.appendChild(effet);
      syncDetail();
      return box;
    }
    function paliersOf(a) {
      var m = {};
      (a.paliers || []).forEach(function (p) { m[p.niveau] = p; });
      return m;
    }
    search.addEventListener("input", render);
    render();
  }

  // --- onglet Nen ---------------------------------------------------------------
  // Volontairement vide : le raccordement du Nen (capacités, développement
  // intérieur) viendra quand ses règles de création seront posées.
  function buildNen(pane) {
    var b = block(pane, "Nen", null,
      "Cette partie de la fiche est en chantier : le raccordement du Nen (développement intérieur, catégories, capacités) viendra plus tard.");
    b.appendChild(el("div", "pc-empty", "Rien à remplir pour l'instant."));
  }

  // --- fiche imprimable ---------------------------------------------------------
  function printSheet() {
    var old = document.getElementById("pc-print");
    if (old) old.remove();
    var p = el("div"); p.id = "pc-print";
    function h(tag, txt) { var e = el(tag, null, txt); p.appendChild(e); return e; }
    function table(head, rows) {
      var t = el("table"), tr = el("tr");
      head.forEach(function (x) { tr.appendChild(el("th", null, x)); });
      t.appendChild(tr);
      rows.forEach(function (r) {
        var row = el("tr");
        r.forEach(function (x) { row.appendChild(el("td", null, String(x))); });
        t.appendChild(row);
      });
      p.appendChild(t);
      return t;
    }
    h("h2", state.name || "Personnage sans nom");
    var t0 = tailleCat();
    h("p", ["Niveau " + niveau() + " (" + fmt(state.pfTotal) + " PF)",
            "Éclat " + state.eclatA + (state.eclatA !== state.eclatN ? " (naissance " + state.eclatN + ")" : ""),
            state.classe ? "Classe : " + state.classe : null,
            state.age ? state.age + " ans" : null, state.genre || null,
            state.tailleCm ? state.tailleCm + " m" : null, state.poids ? state.poids + " kg" : null,
            "Taille " + state.tailleCat + (t0 && t0.pvMod ? " (" + signed(t0.pvMod) + " PV/niv)" : "")
           ].filter(Boolean).join(" · "));

    h("h3", "Caractéristiques");
    var caracRows = DATA.caracs.map(function (k) {
      return [k.abbr, k.name, caracVal(k.abbr), signed(modOf(caracVal(k.abbr)))];
    });
    table(["", "Caractéristique", "Valeur", "Modificateur"], caracRows);

    h("h3", "Combat et capacités");
    var mv = capRow("mouvement", caracVal("AGI")) || [];
    var pt = capRow("port", caracVal("FOR")) || [];
    var ap = capRow("apnee", caracVal("END")) || [];
    var so = capRow("sommeil", caracVal("END")) || [];
    table(["PV (courants / max)", "Initiative", "Esquive", "Parade", "Points de fatigue"],
          [[fmt(pvCourant()) + " / " + fmt(pvMax()), signed(compTotal("Initiative") + modsGlobaux()), signed(compTotal("Esquive") + modsGlobaux()),
            signed(compTotal("Parade") + modsGlobaux()), fatiguePts() + " / " + caracVal("END")]]);
    h("p", "Points de fatigue : maximum = Endurance ; +15 au jet par point consommé (5 max par jet) ; −10 à tous les jets par point sous zéro ; effondrement à −" + caracVal("END") + ".");
    if (modsGlobaux()) h("p", "Modificateur à toutes les actions : " + signed(modsGlobaux()) +
      (fatiguePts() < 0 ? " (dont fatigue " + signed(10 * Math.min(0, fatiguePts())) + ")" : "") +
      " — déjà compté dans Initiative, Esquive et Parade ci-dessus, à reporter sur les autres jets (le tableau Armes ne le compte pas).");
    var etatLines = [];
    (DATA.etats || []).forEach(function (e) {
      var v = state.etatsActifs[e.name];
      if (!v) return;
      var p = null;
      if (v !== true) e.paliers.forEach(function (x) { if (x.name === v) p = x; });
      var mods = (p ? p.mods : e.mods).map(function (m) { return m.cible + " " + signed(m.val); }).join(" · ");
      etatLines.push([e.name + (p ? " (" + p.name + ")" : ""),
                      (e.name === "Abri" ? "subi par l'assaillant : " : "") + (mods || "voir la règle")]);
    });
    if (etatLines.length) { h("h3", "États en cours"); table(["État", "Effets"], etatLines); }
    var soCols = DATA.capacites.sommeil ? DATA.capacites.sommeil.cols.join(" · ") : "";
    table(["Mouvement (marche · course · sprint)", "Port (léger · effort · maximal)",
           "Apnée (légère · intermédiaire · lourde)", "Endurance (" + soCols + ")"],
          [[mv.join(" · "), pt.join(" · "), ap.join(" · "), so.join(" · ")]]);

    h("h3", "Compétences");
    var invested = DATA.competences.filter(function (k) { return state.comps[k.name] > 0 || diversOf(k.name); });
    var compRows = invested.map(function (k) {
      return [k.name, caracAbbr(k.carac), "+" + compBase(k.name),
              diversOf(k.name) ? signed(diversOf(k.name)) : "", signed(compTotal(k.name))];
    });
    state.customComps.forEach(function (c) {
      if (!(c.pf > 0) && !c.divers) return;
      compRows.push([c.name + " (perso)", c.carac, "+" + ((c.pf || 0) / 5) * 20,
                     c.divers ? signed(c.divers) : "", signed(customTotal(c))]);
    });
    if (compRows.length) {
      table(["Compétence", "Carac", "Base", "Divers", "Total"], compRows);
      h("p", "Toute autre compétence vaut le modificateur de sa caractéristique.");
    } else {
      h("p", "Aucun PF investi : chaque compétence vaut le modificateur de sa caractéristique.");
    }

    if (state.armeDepart || state.formations.length) {
      h("h3", "Formations");
      var lines = [];
      if (state.armeDepart) lines.push(["Arme de départ", state.armeDepart]);
      state.formations.forEach(function (f) {
        var d = formationByName(f.name);
        lines.push([f.name + (f.choix ? " (" + f.choix + ")" : ""), d ? d.cout + " PF" : ""]);
      });
      table(["Formation", ""], lines);
      h("p", "Arme inconnue : −20 (même famille qu'une arme connue) ou −40 (famille étrangère) en attaque et parade.");
    }

    h("h3", "Armes");
    var portees = DATA.armes.filter(function (a) { return a.corps; }).map(function (a) { return { a: a, name: a.name }; })
      .concat(state.armes.map(function (e) { return { a: armeByName(e.name), name: e.name }; }));
    table(["Arme", "Attaque", "Parade", "Dégâts", "Notes"], portees.map(function (x) {
      if (!x.a) return [x.name, "MJ", "MJ", "MJ", "arme forgée (Forge)"];
      var lourd = lourdeurMalus(x.a);
      var atk = armeTypes(x.a).map(function (t) { return t.label + " " + signed(compTotal(t.comp) + malusArme(x.a, t.label) + lourd); }).join(" · ");
      var famP = malusArme(x.a, "Parade");
      var par = /\bParade\b/.test(x.a.props) ? signed(compTotal("Parade") + famP) : "—";
      var md = modDegatsArme(x.a);
      var famGen = malusArme(x.a);
      var notes = [];
      if (famGen) notes.push("familiarité " + signed(famGen));
      if (lourd) notes.push("Lourdeur " + signed(lourd) + " à l'attaque");
      return [x.name, atk, par, String(x.a.degats) + (md.val || md.txt ? " " + signed(md.val) + (md.txt ? " (" + md.txt + ")" : "") : ""), notes.join(" · ")];
    }));
    h("p", "Le modificateur à toutes les actions n'est pas compté dans ce tableau.");

    var artNames = Object.keys(state.arts);
    if (artNames.length) {
      h("h3", "Arts");
      table(["Art", "Palier", "Frappe / effet"], artNames.map(function (n) {
        var a = artByName(n), pal = state.arts[n];
        var pd = null;
        (a && a.paliers || []).forEach(function (x) { if (x.niveau === pal) pd = x; });
        var extra = a && a.frappe ? "Frappe " + frappeTxt(a, pal) : (pd && pd.effet ? pd.effet : "");
        return [n, pal, extra];
      }));
    }

    if (state.inventaire.length) {
      h("h3", "Équipement (" + fmt(argentDepense()) + " Ɉ · bourse " + fmt(state.argent) + " Ɉ)");
      table(["Objet", "Détail", "Prix", "Familiarité"], state.inventaire.map(function (it) {
        var a = it.arme && !it.forge ? armeByName(it.name) : null;
        var m = a ? malusArme(a) : 0;
        var fam = !it.arme ? "" : it.forge ? "au choix du MJ" : (m ? String(m).replace("-", "−") : "connue");
        return [it.name,
                a ? a.famille + " · Dégâts " + a.degats + " · " + a.portee : (it.forge ? "arme forgée" : ""),
                it.prix ? fmt(it.prix) + " Ɉ" : "—",
                fam];
      }));
    }

    var acRows = DATA.sens.filter(function (s) { return s.niveau !== "Inexistant" && s.niveau !== "Latent"; });
    h("h3", "Sens (acuité de départ 10)");
    table(["Sens", "Niveau", "Acuité"], acRows.map(function (s) {
      return [s.name, s.niveau, state.acuite[s.name] != null ? state.acuite[s.name] : 10];
    }));

    var avs = state.avantages.filter(function (a) { return (a.name || "").trim(); });
    if (avs.length) {
      h("h3", "Avantages et handicaps");
      table(["Nom", "Effet"], avs.map(function (a) { return [a.name, a.note || ""]; }));
    }

    if (state.notes) { h("h3", "Notes"); h("p", state.notes); }

    h("h3", "Échelle de difficulté");
    table(["Difficulté", "Seuil"], DATA.difficultes.map(function (d) { return [d.name, d.seuil]; }));

    document.body.appendChild(p);
    document.documentElement.classList.add("pc-printing");
    var done = function () {
      document.documentElement.classList.remove("pc-printing");
      window.removeEventListener("afterprint", done);
    };
    window.addEventListener("afterprint", done);
    setTimeout(done, 3000);   // filet si afterprint ne se déclenche pas
    window.print();
  }

  // --- export / import ------------------------------------------------------------
  function exportJson() {
    var blob = new Blob([JSON.stringify(state, null, 2)], { type: "application/json" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = (state.name.trim() || "personnage") + ".json";
    a.click();
  }

  // --- montage ---------------------------------------------------------------
  function mount(root) {
    rootEl = root;
    updaters = [];
    warnBox = meterBox = libSelect = null;
    root.innerHTML = "";
    var app = el("div", "perso-atelier");

    // barre d'outils (chrome du site, hors de la feuille)
    var top = el("div", "pc-top");
    top.appendChild(el("span", "pc-top-title", "Création"));
    top.appendChild(el("span", "pc-top-hint", "Un personnage de A à Z, sans le Nen."));
    var saveB = el("button", "pc-btn primary"); saveB.type = "button"; saveB.textContent = "Enregistrer";
    saveB.addEventListener("click", saveCurrentPerso);
    top.appendChild(saveB);
    var printB = el("button", "pc-btn"); printB.type = "button"; printB.textContent = "Imprimer la fiche";
    printB.addEventListener("click", printSheet);
    top.appendChild(printB);
    var expB = el("button", "pc-btn"); expB.type = "button"; expB.textContent = "Exporter";
    expB.addEventListener("click", exportJson);
    top.appendChild(expB);
    var impIn = el("input"); impIn.type = "file"; impIn.accept = "application/json"; impIn.style.display = "none";
    var impB = el("button", "pc-btn"); impB.type = "button"; impB.textContent = "Importer";
    impB.addEventListener("click", function () { impIn.click(); });
    impIn.addEventListener("change", function () {
      var f = impIn.files && impIn.files[0];
      if (!f) return;
      var rd = new FileReader();
      rd.onload = function () {
        try {
          var s = normalize(JSON.parse(rd.result));
          if (!s) { alert("Format de personnage non reconnu."); return; }
          state = s; mount(root);
        } catch (e) { alert("Fichier illisible : " + e.message); }
      };
      rd.readAsText(f);
      impIn.value = "";   // permet de re-sélectionner le même fichier
    });
    top.appendChild(impB); top.appendChild(impIn);
    var reset = el("button", "pc-btn"); reset.type = "button"; reset.textContent = "Réinitialiser";
    reset.addEventListener("click", function () {
      if (confirm("Repartir d'un personnage vierge ?")) { state = blank(); mount(root); }
    });
    top.appendChild(reset);

    // bibliothèque : menu + charger / supprimer
    var lib = el("span", "pc-lib");
    libSelect = el("select");
    lib.appendChild(libSelect);
    var loadB = el("button", "pc-btn"); loadB.type = "button"; loadB.textContent = "Charger";
    loadB.addEventListener("click", function () {
      var p = loadPersos().filter(function (x) { return x.id === libSelect.value; })[0];
      if (p) loadPersoInto(p);
    });
    lib.appendChild(loadB);
    var delB = el("button", "pc-btn"); delB.type = "button"; delB.textContent = "Supprimer";
    delB.addEventListener("click", function () {
      var p = loadPersos().filter(function (x) { return x.id === libSelect.value; })[0];
      if (p && confirm("Supprimer « " + p.name + " » ?")) deletePerso(p.id);
    });
    lib.appendChild(delB);
    top.appendChild(lib);
    app.appendChild(top);

    // la feuille
    var sheet = el("div", "pc-sheet");
    app.appendChild(sheet);

    // journal de jets (panneau flottant)
    rollPanel = el("div", "pc-rolls");
    var rHead = el("div", "pc-rolls-head");
    var rTitle = el("span", "t", "Jets");
    rTitle.addEventListener("click", function () { rollPanel.classList.toggle("open"); });
    rHead.appendChild(rTitle);
    var deIn = el("input", "de");
    deIn.type = "text"; deIn.value = state.de || "1d100";
    deIn.title = "Dé des jets (le livre ne nomme que le 1d100, dans les critiques) : 1d100, 3d20, 1d100+5…";
    deIn.addEventListener("input", function () {
      var v = deIn.value.trim();
      state.de = v || "1d100";
      deIn.classList.toggle("bad", !!v && !/^\d{1,2}d\d{1,4}([+-]\d{1,4})?$/.test(v));
      save();
    });
    rHead.appendChild(deIn);
    // se dépasser : consommer des points de fatigue sur le prochain jet (+15/point, 5 max)
    spendSel = el("select", "spend");
    spendSel.title = "Se dépasser : points de fatigue consommés sur le prochain jet, +15 chacun (5 au plus par jet).";
    for (var si = 0; si <= 5; si++) {
      var so = el("option"); so.value = String(si);
      so.textContent = si ? si + " pt" + (si > 1 ? "s" : "") + " (+" + 15 * si + ")" : "se dépasser";
      spendSel.appendChild(so);
    }
    rHead.appendChild(spendSel);
    var rClear = el("button", "pc-mini", "Vider"); rClear.type = "button";
    rClear.addEventListener("click", function () { rollHistory = []; renderRolls(); });
    rHead.appendChild(rClear);
    var rTog = el("button", "pc-mini", "▾"); rTog.type = "button"; rTog.title = "Réduire / déployer";
    rTog.addEventListener("click", function () { rollPanel.classList.toggle("open"); });
    rHead.appendChild(rTog);
    rollPanel.appendChild(rHead);
    rollPanel.appendChild(el("div", "pc-rolls-list"));
    app.appendChild(rollPanel);
    renderRolls();

    root.appendChild(app);

    buildHead(sheet);
    var panes = buildTabs(sheet);
    buildGeneral(panes.general);
    buildFormations(panes.formations);
    buildArts(panes.formations);
    buildNen(panes.nen);
    refresh();
  }

  function init() {
    var root = document.getElementById("perso-atelier");
    if (!root || root.getAttribute("data-ready")) return;
    root.setAttribute("data-ready", "1");
    if (DATA) { state = load() || blank(); mount(root); return; }
    fetch(siteBase() + "creation.json", { cache: "no-cache" })
      .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
      .then(function (d) { DATA = d; state = load() || blank(); mount(root); })
      .catch(function (e) { root.innerHTML = '<p style="padding:2rem;color:#b0402c">Le créateur n\'a pas pu charger ses données (' + e.message + ").</p>"; });
  }

  if (window.document$ && typeof window.document$.subscribe === "function") window.document$.subscribe(init);
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
