/* Correspondance fiche HxH <-> Attributes Roll20 (natifs par valeur).
 *
 * Le créateur (creation.js, réutilisé tel quel) travaille sur un objet `state`
 * imbriqué. Roll20 stocke des Attributes plats {name, current, max}. Ce module
 * fait la traduction, DANS LES DEUX SENS et SANS PERTE :
 *   - stateToAttrs(state, card) : décompose l'état en attributs Roll20.
 *   - attrsToState(attrs)       : reconstruit l'état depuis les attributs.
 *
 * TOUS les attributs produits commencent par « hxh_ » (consigne). Trois familles :
 *   - SOURCE DE VÉRITÉ : `hxh_state` porte l'état ENTIER en JSON. C'est lui qu'on
 *     relit pour reconstruire la fiche : il ne dérive JAMAIS quand creation.js gagne
 *     un champ (Nen, forme, rayon de l'En, divers/override…). attrsToState le préfère
 *     à tout le reste ; la reconstruction champ par champ n'est qu'un repli legacy.
 *   - NATIFS (round-trip legacy + macros) : un attribut par valeur/collection
 *     (scalaires, 12 caractéristiques, collections en JSON) ; utiles aux macros
 *     (@{perso|FOR}) et au repli pour les fiches d'avant `hxh_state`.
 *   - MIROIR (écrits seulement si `card` fourni) : valeurs DÉRIVÉES pour les
 *     macros et barres de jetons Roll20 — modificateurs de carac (dans le `max`
 *     de la carac : @{perso|FOR} = valeur, @{perso|FOR|max} = mod), PV courant/max,
 *     fatigue, Initiative/Esquive/Parade, niveau. Non relus (recalculés par le créateur).
 *
 * Logique PURE, sans API navigateur : testable en node, chargée telle quelle
 * dans l'iframe du créateur.
 */
(function (root) {
  "use strict";

  var PREFIX = "hxh_";

  // clé interne du créateur -> suffixe d'attribut natif (macro-friendly, ASCII)
  var CARACS = [
    ["FOR", "for"], ["DEX", "dex"], ["AGI", "agi"], ["END", "end"],
    ["PER", "per"], ["PRÉ", "pre"], ["VOL", "vol"], ["LOG", "log"],
    ["INS", "ins"], ["ÉRU", "eru"], ["IMA", "ima"], ["CHA", "cha"]
  ];

  // champ d'état scalaire -> [suffixe, type] (n = nombre, s = chaîne libre)
  var SCALARS = [
    ["name", "nom", "s"], ["classe", "classe", "s"], ["genre", "genre", "s"],
    ["age", "age", "s"], ["tailleCm", "taille", "s"], ["poids", "poids", "s"],
    ["tailleCat", "categorie", "s"], ["notes", "notes", "s"], ["de", "de", "s"],
    ["portrait", "portrait", "s"], ["armeDepart", "arme_depart", "s"],
    ["pfTotal", "pf_total", "n"], ["pvParNiveau", "pv_par_niveau", "n"],
    ["argent", "bourse", "n"], ["eclatN", "eclat_naissance", "n"],
    ["eclatA", "eclat_actuel", "n"], ["modGlobal", "mod_global", "n"],
    ["v", "version", "n"]
  ];

  // champ d'état collection (objet/tableau) -> suffixe (stocké en JSON)
  var COLLECTIONS = [
    ["comps", "competences"], ["customComps", "comp_perso"], ["divers", "comp_divers"],
    ["formations", "formations"], ["arts", "arts"], ["armes", "armes"],
    ["inventaire", "inventaire"], ["acuite", "acuite"], ["etatsActifs", "etats"],
    ["avantages", "avantages"]
  ];

  // état par défaut (miroir de blank() de creation.js ; sert de socle à la
  // reconstruction : un attribut absent laisse la valeur par défaut).
  function blank() {
    return {
      v: 1,
      name: "", age: "", genre: "", tailleCm: "", poids: "", classe: "", notes: "",
      tailleCat: "Moyenne",
      pfTotal: 100, pvParNiveau: 100, argent: 0,
      eclatN: 10, eclatA: 10,
      caracs: { FOR: 3, DEX: 3, AGI: 3, END: 3, PER: 3, "PRÉ": 3, VOL: 3, LOG: 3, INS: 3, "ÉRU": 3, IMA: 3, CHA: 3 },
      comps: {}, customComps: [], divers: {}, modGlobal: 0,
      formations: [], arts: {}, armeDepart: "", armes: [], inventaire: [],
      acuite: {}, de: "1d100", pv: null, fatigue: null,
      etatsActifs: {}, avantages: [], portrait: ""
    };
  }

  function num(v) { var n = parseFloat(v); return isFinite(n) ? n : 0; }
  function str(v) { return v == null ? "" : String(v); }

  // { fullAttrName -> {current, max} }
  function stateToAttrs(state, card) {
    state = state || blank();
    var out = {};
    function put(suffix, current, max) {
      out[PREFIX + suffix] = { current: str(current), max: str(max == null ? "" : max) };
    }

    // ROUND-TRIP COMPLET : l'état entier en un attribut, source de vérité pour la
    // reconstruction. Il NE DÉRIVE JAMAIS quand la fiche du site gagne des champs
    // (Nen, forme, rayon de l'En, divers/override…) : tout ce que creation.js met
    // dans `state` revient tel quel. Les attributs natifs ci-dessous ne servent plus
    // qu'aux MACROS et barres de jetons Roll20 (@{perso|FOR}, PV, Initiative…).
    put("state", JSON.stringify(state));

    SCALARS.forEach(function (d) { put(d[1], state[d[0]]); });
    CARACS.forEach(function (d) { put(d[1], (state.caracs || {})[d[0]]); });
    COLLECTIONS.forEach(function (d) { put(d[1], JSON.stringify(state[d[0]] == null ? blank()[d[0]] : state[d[0]])); });
    // PV/fatigue courants nullable : conservés à l'exact (null = « au maximum »)
    put("etat_courant", JSON.stringify({ pv: state.pv == null ? null : state.pv, fatigue: state.fatigue == null ? null : state.fatigue }));

    // ---- miroir dérivé (macros / barres de jetons), seulement si la carte est fournie ----
    if (card) {
      var suf = {};
      CARACS.forEach(function (d) { suf[d[0]] = d[1]; });
      (card.caracs || []).forEach(function (k) {
        var a = out[PREFIX + suf[k.abbr]];
        if (a) a.max = str(k.mod);   // @{perso|FOR|max} = modificateur
      });
      var cb = card.combat || {};
      put("pv", cb.pv == null ? "" : cb.pv, cb.pvMax);           // barre de jeton : PV courant / max
      put("fatigue", cb.fatigue == null ? "" : cb.fatigue, cb.fatigueMax);
      put("init", cb.init);
      put("esquive", cb.esquive);
      put("parade", cb.parade);
      if (card.identity && card.identity.niveau != null) put("niveau", card.identity.niveau);
    }
    return out;
  }

  // attrs : { fullAttrName -> {current, max} } ou { fullAttrName -> current }.
  // Reconstruit l'état (round-trip). Les attributs miroir sont ignorés.
  function attrsToState(attrs) {
    attrs = attrs || {};
    function cur(suffix) {
      var a = attrs[PREFIX + suffix];
      if (a == null) return undefined;
      return (typeof a === "object" && a !== null) ? a.current : a;
    }
    // Priorité : l'état complet round-trip (hxh_state), qui porte TOUS les champs de
    // la fiche du site. Repli sur la reconstruction champ par champ ci-dessous pour
    // les fiches enregistrées avant hxh_state (creation.js re-normalise dans tous les cas).
    var full = cur("state");
    if (full !== undefined && full !== "") {
      try { var fs = JSON.parse(full); if (fs && typeof fs === "object") return fs; } catch (e) {}
    }
    var s = blank();

    SCALARS.forEach(function (d) {
      var v = cur(d[1]);
      if (v === undefined) return;
      if (d[2] === "n") { if (v !== "" && isFinite(parseFloat(v))) s[d[0]] = num(v); }
      else s[d[0]] = str(v);
    });
    CARACS.forEach(function (d) {
      var v = cur(d[1]);
      if (v !== undefined && v !== "" && isFinite(parseFloat(v))) s.caracs[d[0]] = num(v);
    });
    COLLECTIONS.forEach(function (d) {
      var v = cur(d[1]);
      if (v === undefined || v === "") return;
      try { var o = JSON.parse(v); if (o != null) s[d[0]] = o; } catch (e) {}
    });
    var ec = cur("etat_courant");
    if (ec !== undefined && ec !== "") {
      try {
        var o = JSON.parse(ec);
        s.pv = (o && o.pv != null) ? o.pv : null;
        s.fatigue = (o && o.fatigue != null) ? o.fatigue : null;
      } catch (e) {}
    }
    return s;
  }

  function isHxhAttr(name) { return typeof name === "string" && name.indexOf(PREFIX) === 0; }
  // une fiche HxH existe si l'attribut de version est présent
  function hasSheet(names) {
    if (!names) return false;
    var list = Array.isArray(names) ? names : Object.keys(names);
    return list.indexOf(PREFIX + "version") >= 0;
  }
  // liste des noms d'attributs round-trip (pour lecture ciblée si besoin)
  function roundTripNames() {
    var out = SCALARS.map(function (d) { return PREFIX + d[1]; })
      .concat(CARACS.map(function (d) { return PREFIX + d[1]; }))
      .concat(COLLECTIONS.map(function (d) { return PREFIX + d[1]; }));
    out.push(PREFIX + "etat_courant");
    out.push(PREFIX + "state");
    return out;
  }

  var api = {
    PREFIX: PREFIX,
    stateToAttrs: stateToAttrs,
    attrsToState: attrsToState,
    isHxhAttr: isHxhAttr,
    hasSheet: hasSheet,
    roundTripNames: roundTripNames,
    blank: blank
  };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.HxHAttrMap = api;
})(typeof window !== "undefined" ? window : this);
