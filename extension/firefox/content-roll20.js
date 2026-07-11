/* Content script sur Roll20 : VRAI onglet « Fiche HxH » dans le dialogue d'un
 * personnage, entre « Feuille de personnage » et « Bio & Info ».
 *
 * Comme les onglets natifs de Roll20, l'onglet ÉCHANGE le contenu de #tab-content
 * (il masque les panes natifs et affiche la fiche HxH en flux, aucun chevauchement).
 * Un clic sur un onglet natif restaure la zone et laisse Roll20 afficher sa page
 * (interception en phase capture, avant le gestionnaire de Roll20). Détection
 * robuste : onglets repérés par texte normalisé, ré-injection si Roll20 re-rend la
 * barre. Si aucun onglet ne peut être placé, un bouton de secours flottant ouvre la
 * fiche en plein écran. Les valeurs lançables postent un jet dans le tchat.
 */
// compat : Chrome expose `chrome.*`, Firefox `browser.*` (les deux rendent des promesses).
if (typeof browser === "undefined") { var browser = chrome; }
(function () {
  "use strict";

  var cards = {};
  var names = {};
  var assoc = {};

  function el(tag, cls, txt) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (txt != null) e.textContent = txt;
    return e;
  }
  function norm(s) { return (s || "").replace(/ /g, " ").replace(/\s+/g, " ").trim().toLowerCase(); }

  function loadState() {
    return browser.storage.local.get(["hxhCards", "hxhNames", "hxhAssoc"]).then(function (r) {
      cards = r.hxhCards || {};
      names = r.hxhNames || {};
      assoc = r.hxhAssoc || {};
    });
  }
  function saveAssoc() { try { browser.storage.local.set({ hxhAssoc: assoc }); } catch (e) {} }

  function orderedIds() {
    var ids = Object.keys(cards);
    var cur = ids.indexOf("_current") >= 0 ? ["_current"] : [];
    var rest = ids.filter(function (i) { return i !== "_current"; })
      .sort(function (a, b) { return labelFor(a).localeCompare(labelFor(b)); });
    return cur.concat(rest);
  }
  function labelFor(id) {
    if (id === "_current") return (cards._current && cards._current.name || "Brouillon") + " (en cours)";
    return names[id] || (cards[id] && cards[id].name) || id;
  }

  // Le tchat vit dans la page principale ; la fiche peut être injectée dans une
  // iframe (feuille de perso). On tente le document courant puis la page du haut.
  function roll(c, label, value) {
    var cmd = HxHRender.rollCommand(c.de, value, label);
    if (HxHRender.sendToChat(document, cmd)) return;
    try { if (window.top !== window && HxHRender.sendToChat(window.top.document, cmd)) return; } catch (e) {}
    alert("Tchat Roll20 introuvable : ouvrez d'abord une partie (l'éditeur de jeu).");
  }

  // Polices du livre embarquées (sheet-fonts.css). IMPORTANT : un @font-face
  // déclaré DANS un shadow root est ignoré (Chromium ne l'enregistre pas). Les
  // polices doivent donc être déclarées dans le DOCUMENT (light DOM) pour être
  // utilisables par la fiche du shadow (les polices sont globales au document).
  // On les injecte une seule fois dans <head> ; ces déclarations n'altèrent pas
  // l'affichage de Roll20 (il n'appelle ni « Alegreya » ni « EB Garamond »).
  var fontsDone = false;
  function ensureBookFonts() {
    if (fontsDone || document.getElementById("hxh-book-fonts")) { fontsDone = true; return; }
    fontsDone = true;
    var url; try { url = browser.runtime.getURL("sheet-fonts.css"); } catch (e) { url = "sheet-fonts.css"; }
    fetch(url).then(function (r) { return r.text(); }).then(function (css) {
      if (document.getElementById("hxh-book-fonts")) return;
      var st = document.createElement("style");
      st.id = "hxh-book-fonts";
      st.textContent = css;
      (document.head || document.documentElement).appendChild(st);
    }).catch(function () {});
  }

  // CSS de la fiche du SITE (creation.css) + appoint lecture seule (sheet-extra.css) :
  // chargés une fois depuis le paquet et injectés dans le SHADOW ROOT, pour un rendu
  // IDENTIQUE au site tout en restant isolés du CSS de Roll20. Chargement paresseux.
  var sheetCssPromise = null;
  function loadSheetCss() {
    if (sheetCssPromise) return sheetCssPromise;
    var files = ["creation.css", "sheet-extra.css"];
    sheetCssPromise = Promise.all(files.map(function (f) {
      var url; try { url = browser.runtime.getURL(f); } catch (e) { url = f; }
      return fetch(url).then(function (r) { return r.text(); }).catch(function () { return ""; });
    })).then(function (parts) { return parts.join("\n"); });
    return sheetCssPromise;
  }

  // Panneau (barre de choix + fiche). onClose facultatif pour le mode secours.
  // Le contenu vit dans un SHADOW ROOT : le CSS de Roll20 ne peut pas l'atteindre
  // (et le nôtre ne fuit pas dehors). L'hôte, en lumière, ne fait que se placer
  // dans la zone de contenu. Renvoie l'HÔTE.
  function buildPanel(key, opts) {
    opts = opts || {};
    ensureBookFonts();   // polices du livre dans le document (utilisables par le shadow)
    var host = el("div", "hxh-host" + (opts.floating ? " hxh-host-floating" : ""));
    var box;
    if (host.attachShadow) {
      box = host.attachShadow({ mode: "open" });
      var st = document.createElement("style");
      st.textContent = (window.HxHRender && HxHRender.paneCss) || "";
      box.appendChild(st);
      // 2e feuille : la vraie fiche du site + ses polices (chargement paresseux)
      var stSheet = document.createElement("style");
      box.appendChild(stSheet);
      loadSheetCss().then(function (css) { stSheet.textContent = css; });
    } else {
      box = host;   // repli : Shadow DOM indisponible (très vieux navigateur)
    }
    var panel = el("div", "hxh-panel" + (opts.floating ? " hxh-floating" : ""));
    box.appendChild(panel);
    var bar = el("div", "hxh-bar");
    bar.appendChild(el("span", "hxh-bar-title", "Fiche HxH"));
    var sel = el("select", "hxh-select");
    var refresh = el("button", "hxh-btn", "Actualiser"); refresh.type = "button";
    bar.appendChild(sel); bar.appendChild(refresh);
    if (opts.onClose) {
      var close = el("button", "hxh-btn hxh-close", "Fermer"); close.type = "button";
      close.addEventListener("click", opts.onClose);
      bar.appendChild(close);
    }
    panel.appendChild(bar);
    var body = el("div", "hxh-body hxh-body-sheet");
    panel.appendChild(body);

    function render(id) {
      body.innerHTML = "";
      var c = cards[id];
      if (!c) { body.appendChild(el("div", "hxh-empty", "Aucune fiche. Créez un personnage sur le site HxH puis rouvrez ce dialogue.")); return; }
      var build = (HxHRender.sheet || HxHRender.card);
      body.appendChild(build(c, function (label, value) { roll(c, label, value); }));
    }
    function apply(id) {
      if (id && cards[id] && key) { assoc[key] = id; saveAssoc(); }
      render(id);
    }
    function fill(keepId) {
      sel.innerHTML = "";
      var list = orderedIds();
      if (!list.length) { var e0 = el("option"); e0.value = ""; e0.textContent = "— aucune fiche synchronisée —"; sel.appendChild(e0); }
      list.forEach(function (id) { var o = el("option"); o.value = id; o.textContent = labelFor(id); sel.appendChild(o); });
      var chosen = keepId || (key && assoc[key]);
      sel.value = (chosen && cards[chosen]) ? chosen : (list[0] || "");
      apply(sel.value);
    }
    sel.addEventListener("change", function () { apply(sel.value); });
    refresh.addEventListener("click", function () { loadState().then(function () { fill(sel.value); }); });
    fill(null);
    return host;
  }

  // ------- pose de l'onglet dans la barre d'onglets d'un dialogue -------
  function labelEls(label) {
    var want = norm(label);
    var nodes = document.querySelectorAll("a, span, li");
    var raw = [];
    for (var i = 0; i < nodes.length; i++) {
      if (norm(nodes[i].textContent) === want) raw.push(nodes[i]);
    }
    // on ne garde que les plus internes (pas les conteneurs)
    return raw.filter(function (n) { return !raw.some(function (m) { return m !== n && n.contains(m); }); });
  }
  function siblingItems(a, b) {
    for (var pa = a; pa; pa = pa.parentNode) {
      for (var pb = b; pb; pb = pb.parentNode) {
        if (pb.parentNode && pb.parentNode === pa.parentNode) return [pa, pb];
      }
    }
    return null;
  }
  function dialogOf(node) {
    return node.closest(".ui-dialog") || node.closest("[class*='dialog']") || node.offsetParent || node.parentElement;
  }
  function characterKey(dialog) {
    var withId = dialog.querySelector && dialog.querySelector("[data-characterid]");
    if (withId && withId.getAttribute("data-characterid")) return "id:" + withId.getAttribute("data-characterid");
    var title = dialog.querySelector && (dialog.querySelector(".ui-dialog-title") || dialog.querySelector(".dialog-title"));
    if (!title && dialog.querySelectorAll) {
      var cands = dialog.querySelectorAll("[class*='title']");
      for (var i = 0; i < cands.length; i++) if (!/titlebar|title-bar/i.test(cands[i].className)) { title = cands[i]; break; }
    }
    var name = title ? (title.textContent || "").trim() : "";
    return "name:" + (name || "?");
  }
  // Conteneur de contenu du dialogue (là où vivent les panes natifs .tab-pane).
  function contentBoxOf(dialog, strip) {
    return (dialog.querySelector && dialog.querySelector(".tab-content")) || strip.nextElementSibling;
  }

  function placeTabs() {
    var placed = 0;
    labelEls("Feuille de personnage").forEach(function (feuille) {
      var bios = labelEls("Bio & Info");
      var items = null;
      for (var i = 0; i < bios.length && !items; i++) {
        var it = siblingItems(feuille, bios[i]);
        if (!it) continue;
        var parent = it[0].parentNode;
        if (parent === document.body || parent === document.documentElement) continue;
        if (parent.children.length > 24) continue;   // pas une barre d'onglets
        items = it;
      }
      if (!items) return;
      var feuilleItem = items[0], bioItem = items[1], strip = bioItem.parentNode;
      if (strip.querySelector(".hxh-tab")) { placed++; return; }   // déjà là

      var dialog = dialogOf(strip);
      var contentBox = contentBoxOf(dialog, strip);

      var tab = document.createElement(feuilleItem.tagName || "li");
      tab.className = ((feuilleItem.className || "").replace(/\b(active|ui-tabs-active|ui-state-active|chosen)\b/g, "").trim() + " hxh-tab").trim();
      var link = feuilleItem.querySelector("a, span, button");
      if (link) {
        var inner = document.createElement(link.tagName);
        if (link.className) inner.className = link.className;
        inner.textContent = "Fiche HxH";
        tab.appendChild(inner);
      } else { tab.textContent = "Fiche HxH"; }

      // Vrai onglet : on masque les panes natifs et on affiche la fiche à leur
      // place (en flux), on restaure tout dès qu'un onglet natif est cliqué.
      var pane = null, hidden = null;
      function showHxh() {
        if (!contentBox) return;
        if (!pane) { pane = buildPanel(characterKey(dialog)); contentBox.appendChild(pane); }
        hidden = [];
        for (var i = 0; i < contentBox.children.length; i++) {
          var ch = contentBox.children[i];
          if (ch === pane) continue;
          hidden.push([ch, ch.style.display]);
          ch.style.display = "none";
        }
        pane.style.display = "block";
        for (var j = 0; j < strip.children.length; j++) strip.children[j].classList.remove("active");
        tab.classList.add("active"); tab.classList.add("hxh-tab-active");
      }
      function hideHxh() {
        if (pane) pane.style.display = "none";
        if (hidden) { for (var k = 0; k < hidden.length; k++) hidden[k][0].style.display = hidden[k][1]; hidden = null; }
        tab.classList.remove("active"); tab.classList.remove("hxh-tab-active");
      }
      tab.addEventListener("click", function (ev) { ev.preventDefault(); ev.stopPropagation(); loadState().then(showHxh); });
      // capture : passe AVANT le gestionnaire d'onglets de Roll20, pour restaurer
      // la zone de contenu puis laisser Roll20 afficher sa propre page.
      strip.addEventListener("click", function (ev) {
        var a = ev.target.closest && ev.target.closest("a[data-tab]");
        if (a && strip.contains(a)) hideHxh();
      }, true);

      strip.insertBefore(tab, bioItem);
      placed++;
    });
    return placed;
  }

  // ------- bouton de secours flottant (si l'onglet ne peut pas être posé) -------
  var floatOverlay = null;
  function openFloating() {
    if (floatOverlay) { floatOverlay.remove(); floatOverlay = null; }
    loadState().then(function () {
      floatOverlay = el("div", "hxh-overlay");
      var panel = buildPanel(null, { floating: true, onClose: function () { floatOverlay.remove(); floatOverlay = null; } });
      floatOverlay.appendChild(panel);
      document.body.appendChild(floatOverlay);
    });
  }
  function isTopFrame() { try { return window.top === window; } catch (e) { return true; } }
  // Le script tourne sur tout app.roll20.net (pour atteindre la frame de la feuille,
  // quelle que soit son URL) : le bouton de secours ne vaut que sur une page de jeu.
  function onGamePage() {
    var pth = ""; try { pth = location.pathname || ""; } catch (e) {}
    return pth.indexOf("/editor") === 0 || pth.indexOf("/campaigns") === 0;
  }
  function refreshFallback() {
    if (!isTopFrame()) return;   // un seul bouton de secours, dans la page principale
    var stray = document.getElementById("hxh-fallback");
    if (!onGamePage()) { if (stray) stray.remove(); return; }
    // l'onglet peut avoir été posé dans une iframe : on le cherche partout
    var hasTab = !!document.querySelector(".hxh-tab");
    if (!hasTab) {
      try {
        var frames = document.querySelectorAll("iframe");
        for (var i = 0; i < frames.length && !hasTab; i++) {
          try { if (frames[i].contentDocument && frames[i].contentDocument.querySelector(".hxh-tab")) hasTab = true; } catch (e) {}
        }
      } catch (e) {}
    }
    var btn = document.getElementById("hxh-fallback");
    if (hasTab || !Object.keys(cards).length) { if (btn) btn.remove(); return; }
    if (btn) return;
    btn = el("button", "hxh-launcher", "Fiche HxH");
    btn.id = "hxh-fallback";
    btn.title = "Afficher une fiche HxH (l'onglet n'a pas pu être placé dans le dialogue)";
    btn.addEventListener("click", openFloating);
    (document.body || document.documentElement).appendChild(btn);
  }

  function scan() { placeTabs(); refreshFallback(); }

  loadState().then(function () {
    scan();
    var pending = false;
    var obs = new MutationObserver(function () {
      if (pending) return;
      pending = true;
      setTimeout(function () { pending = false; scan(); }, 300);
    });
    obs.observe(document.documentElement, { childList: true, subtree: true });
    // quelques passes pendant le chargement de l'éditeur
    var n = 0, iv = setInterval(function () { scan(); if (++n > 12) clearInterval(iv); }, 1000);
  });
})();
