/* Amorce de l'iframe du créateur HxH (page d'extension chargée dans l'onglet Roll20).
 *
 * Rôle : faire tourner le VRAI creation.js du site, mais rediriger sa persistance
 * (localStorage) vers les Attributes Roll20 du personnage — SANS toucher son code.
 *
 * Mécanique :
 *  1. On installe window.__hxhLocalStorage : un shim SYNCHRONE adossé à un cache
 *     mémoire. creation-embed.js (creation.js enveloppé) utilise ce shim à la place
 *     du localStorage réel de l'extension.
 *  2. On demande au parent (content-script Roll20) les Attributes du perso ; à la
 *     réception, HxHAttrMap.attrsToState() reconstruit l'état -> on l'écrit dans le
 *     cache sous « creation-perso ».
 *  3. SEULEMENT ALORS on injecte creation-embed.js : son init()/load() lit l'état
 *     déjà hydraté et monte la fiche.
 *  4. À chaque sauvegarde du créateur (setItem « creation-perso »/« creation-cards »),
 *     HxHAttrMap.stateToAttrs() redécompose l'état ; on n'envoie au parent QUE les
 *     attributs CHANGÉS (le parent throttlera les écritures d20).
 *
 * Le pont est en postMessage (l'iframe est d'origine extension, le parent d'origine
 * Roll20 : origines croisées, on tague les messages par ns:"hxh").
 */
(function () {
  "use strict";
  var M = window.HxHAttrMap;

  // id du personnage Roll20, passé par le content-script dans le hash (#c=<id>).
  var CHAR_ID = (function () {
    var m = /[#&]c=([^&]+)/.exec(location.hash || "");
    return m ? decodeURIComponent(m[1]) : "";
  })();

  var mem = {};                 // cache localStorage
  var SAVE_KEYS = { "creation-perso": 1, "creation-cards": 1 };
  var lastAttrs = {};           // dernier jeu d'attributs connu (base du diff)
  var ready = false;            // les sauvegardes ne partent qu'après hydratation + montage
  var saveTimer = null;

  window.__hxhLocalStorage = {
    getItem: function (k) { return Object.prototype.hasOwnProperty.call(mem, k) ? mem[k] : null; },
    setItem: function (k, v) { mem[k] = String(v); if (ready && SAVE_KEYS[k]) scheduleSave(); },
    removeItem: function (k) { delete mem[k]; },
    clear: function () { mem = {}; },
    key: function (i) { return Object.keys(mem)[i] || null; },
    get length() { return Object.keys(mem).length; }
  };

  // Le pont d20 (roll20-page.js) vit dans le MONDE PRINCIPAL de la frame Roll20 du
  // haut : on lui parle donc via window.top (l'iframe du créateur est imbriquée sous
  // le dialogue du perso). En test à un seul niveau d'iframe, window.top === parent.
  function post(msg) { msg.ns = "hxh"; msg.charId = CHAR_ID; try { window.top.postMessage(msg, "*"); } catch (e) {} }

  function scheduleSave() {
    if (saveTimer) clearTimeout(saveTimer);
    saveTimer = setTimeout(doSave, 400);
  }
  function doSave() {
    saveTimer = null;
    var state;
    try { state = JSON.parse(mem["creation-perso"] || "null"); } catch (e) { return; }
    if (!state) return;
    var card = null;
    try { var cards = JSON.parse(mem["creation-cards"] || "{}"); card = cards && cards._current; } catch (e) {}
    var attrs = M.stateToAttrs(state, card);
    var changed = diff(lastAttrs, attrs);
    lastAttrs = attrs;
    var names = Object.keys(changed);
    if (names.length) post({ type: "save", attrs: changed });
  }
  function val(a, key) { return a && typeof a === "object" ? a[key] : (key === "current" ? a : ""); }
  function diff(oldA, newA) {
    var out = {};
    Object.keys(newA).forEach(function (k) {
      var o = oldA[k], n = newA[k];
      if (!o || String(val(o, "current")) !== n.current || String(val(o, "max")) !== n.max) out[k] = n;
    });
    return out;
  }

  var hydrated = false;
  function hydrate(attrs) {
    if (hydrated) return;         // une seule hydratation par vie d'iframe
    hydrated = true;
    attrs = attrs || {};
    var state = M.attrsToState(attrs);
    mem["creation-perso"] = JSON.stringify(state);
    mem["creation-cards"] = "{}";
    mem["creation-persos"] = "[]";     // pas de bibliothèque multi-perso dans Roll20
    lastAttrs = attrs;                 // base du diff = ce qui est réellement en base
    // charger le vrai creation.js APRÈS hydratation (son init lit creation-perso)
    var s = document.createElement("script");
    s.src = "creation-embed.js";
    s.onload = function () { ready = true; post({ type: "mounted" }); };
    s.onerror = function () { post({ type: "error", error: "creation-embed.js" }); };
    document.body.appendChild(s);
  }

  window.addEventListener("message", function (ev) {
    var d = ev.data;
    if (!d || d.ns !== "hxh") return;
    // on n'accepte que l'hydratation de NOTRE personnage (plusieurs fiches peuvent être ouvertes)
    if (d.type === "hydrate" && (!d.charId || d.charId === CHAR_ID)) hydrate(d.attrs);
  });

  // prêt : on réclame au pont d20 les Attributes hxh_* de ce personnage
  post({ type: "load" });
})();
