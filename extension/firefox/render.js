/* HxH — rendu partagé d'une carte de personnage (lecture seule) et jets Roll20.
 *
 * Logique PURE (aucune API navigateur) : le site HxH calcule tout et écrit une
 * « carte » structurée dans son localStorage ; l'extension ne fait qu'afficher
 * cette carte et transmettre les jets au tchat Roll20. Aucune règle n'est
 * dupliquée ici. Ce fichier est chargé tel quel par le content script Roll20 et
 * par le popup ; il expose window.HxHRender.
 */
(function (root) {
  "use strict";

  function el(tag, cls, txt) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (txt != null) e.textContent = txt;
    return e;
  }
  function signed(n) { return n > 0 ? "+" + n : n < 0 ? "−" + (-n) : "+0"; }

  // Commande de jet Roll20 : un template par défaut avec un jet en ligne.
  // Les valeurs négatives passent par « - N » (et non « +-N ») pour rester
  // valides dans [[ … ]].
  function rollCommand(die, value, label) {
    die = String(die || "1d100").trim() || "1d100";
    var v = value >= 0 ? "+ " + value : "- " + (-value);
    var name = String(label || "Jet").replace(/[{}]/g, "");
    return "&{template:default} {{name=" + name + "}} {{Jet=[[" + die + " " + v + "]]}}";
  }

  // Localise le champ de saisie du tchat Roll20 en tolérant les variantes de
  // structure : id standard, id contenant « textchat », ou textarea nommée.
  function findChatInput(doc) {
    var sels = [
      "#textchat-input textarea",
      "[id*='textchat-input'] textarea",
      "[id*='textchat'] textarea",
      "textarea#textchat-textarea",
      "textarea[name='chat']"
    ];
    for (var i = 0; i < sels.length; i++) {
      var ta = doc.querySelector(sels[i]);
      if (ta) return ta;
    }
    return null;
  }

  // Pose la valeur via le setter natif de HTMLTextAreaElement (Roll20 s'appuie
  // sur des frameworks qui peuvent surveiller la propriété) puis notifie.
  function setValue(ta, text) {
    try {
      var proto = Object.getPrototypeOf(ta);
      var desc = Object.getOwnPropertyDescriptor(proto, "value") ||
                 Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value");
      if (desc && desc.set) desc.set.call(ta, text); else ta.value = text;
    } catch (e) { ta.value = text; }
    ta.dispatchEvent(new Event("input", { bubbles: true }));
    ta.dispatchEvent(new Event("change", { bubbles: true }));
  }

  function fireEnter(ta) {
    ["keydown", "keypress", "keyup"].forEach(function (type) {
      ta.dispatchEvent(new KeyboardEvent(type, {
        bubbles: true, cancelable: true, key: "Enter", code: "Enter", keyCode: 13, which: 13
      }));
    });
  }

  // Injecte un message dans le tchat Roll20 et l'envoie. Renvoie false si le
  // tchat est introuvable (page pas encore prête, ou hors éditeur). L'envoi
  // essaie d'abord le bouton dédié, sinon la touche Entrée.
  function sendToChat(doc, text) {
    var ta = findChatInput(doc);
    if (!ta) return false;
    ta.focus();
    setValue(ta, text);
    var container = ta.closest("[id*='textchat-input'], [id*='textchat']") || ta.parentElement || doc;
    var btn = container.querySelector(".btn, button, [role='button']");
    if (btn) btn.click(); else fireEnter(ta);
    // on remet à zéro pour ne pas laisser la commande dans le champ
    setValue(ta, "");
    return true;
  }

  // Section à titre gravé (repris de la fiche du site).
  function section(title) {
    var s = el("section", "hxh-sec");
    s.appendChild(el("h3", "hxh-sec-title", title));
    return s;
  }
  function kvTable(rows) {
    var t = el("div", "hxh-kvs");
    rows.forEach(function (r) {
      var row = el("div", "hxh-kv");
      row.appendChild(el("span", "hxh-k", r[0]));
      row.appendChild(el("span", "hxh-v", r[1]));
      t.appendChild(row);
    });
    return t;
  }

  // Construit le nœud DOM de la fiche. onRoll(label, rollValue) est appelé au
  // clic sur toute valeur lançable.
  function card(c, onRoll) {
    c = c || {};
    var wrap = el("div", "hxh-card");

    // ---- en-tête ----
    var head = el("div", "hxh-head");
    if (c.portrait) {
      var img = el("img", "hxh-portrait");
      img.src = c.portrait; img.alt = c.name || "";
      img.addEventListener("error", function () { img.style.display = "none"; });
      head.appendChild(img);
    }
    var hid = el("div", "hxh-head-id");
    hid.appendChild(el("div", "hxh-name", c.name || "Personnage"));
    hid.appendChild(el("div", "hxh-sub", (c.header || []).join(" · ")));
    head.appendChild(hid);
    wrap.appendChild(head);

    var cols = el("div", "hxh-cols");
    var colA = el("div", "hxh-col");
    var colB = el("div", "hxh-col");
    var colC = el("div", "hxh-col hxh-col-wide");
    cols.appendChild(colA); cols.appendChild(colB); cols.appendChild(colC);
    wrap.appendChild(cols);

    function rollEl(node, label, value) {
      node.classList.add("hxh-roll");
      node.title = "Cliquer pour lancer les dés (" + (c.de || "1d100") + ").";
      node.addEventListener("click", function () { if (onRoll) onRoll(label, value); });
      return node;
    }

    // ---- colonne A : caractéristiques ----
    var sc = section("Caractéristiques");
    var ct = el("div", "hxh-carac-grid");
    (c.caracs || []).forEach(function (k) {
      var row = el("div", "hxh-carac");
      row.appendChild(el("span", "hxh-abbr", k.abbr));
      row.appendChild(el("span", "hxh-cn", k.name));
      row.appendChild(el("span", "hxh-cv", String(k.val)));
      row.appendChild(el("span", "hxh-cm", signed(k.mod)));
      ct.appendChild(row);
    });
    sc.appendChild(ct);
    colA.appendChild(sc);

    // capacités physiques
    var cap = c.capacites || {};
    var scap = section("Capacités");
    scap.appendChild(kvTable([
      ["Mouvement", (cap.mouvement || []).join(" · ") || "—"],
      ["Port", (cap.port || []).join(" · ") || "—"],
      ["Apnée", (cap.apnee || []).join(" · ") || "—"],
      ["Sommeil / activité", (cap.sommeil || []).join(" · ") || "—"]
    ]));
    colA.appendChild(scap);

    // ---- colonne B : combat + états + sens ----
    var cb = c.combat || {};
    var scb = section("Combat");
    var big = el("div", "hxh-big-row");
    [["Initiative", cb.init], ["Esquive", cb.esquive], ["Parade", cb.parade]].forEach(function (d) {
      var box = el("div", "hxh-big");
      box.appendChild(el("span", "hxh-big-k", d[0]));
      box.appendChild(el("span", "hxh-big-v", signed(d[1] || 0)));
      rollEl(box, d[0], d[1] || 0);
      big.appendChild(box);
    });
    scb.appendChild(big);
    scb.appendChild(kvTable([
      ["PV", (cb.pv != null ? cb.pv : "—") + " / " + (cb.pvMax != null ? cb.pvMax : "—")],
      ["Points de fatigue", (cb.fatigue != null ? cb.fatigue : "—") + " / " + (cb.fatigueMax != null ? cb.fatigueMax : "—")]
    ].concat(cb.modGlobal ? [["Mod. à toutes les actions", signed(cb.modGlobal)]] : [])));
    colB.appendChild(scb);

    if ((c.armes || []).length) {
      var sar = section("Armes");
      (c.armes).forEach(function (a) {
        var box = el("div", "hxh-arme");
        var h = el("div", "hxh-arme-h");
        h.appendChild(el("span", "hxh-arme-n", a.name));
        if (a.famille || a.am) h.appendChild(el("span", "hxh-arme-f", [a.corps ? "corps" : a.famille, a.am ? "AM " + a.am : null].filter(Boolean).join(" · ")));
        box.appendChild(h);
        if (a.unknown) {
          box.appendChild(el("div", "hxh-arme-line", a.forge ? "arme forgée — valeurs au MJ" : "hors barème"));
        } else {
          var line = el("div", "hxh-arme-line");
          (a.attaques || []).forEach(function (t) {
            var chip = el("span", "hxh-wchip", t.label + " " + signed(t.roll));
            rollEl(chip, a.name + " (" + t.label + ")", t.roll);
            line.appendChild(chip);
          });
          if (a.parade != null) {
            var pchip = el("span", "hxh-wchip", "Parade " + signed(a.parade));
            rollEl(pchip, a.name + " (Parade)", a.parade);
            line.appendChild(pchip);
          }
          var dtxt = "Dégâts " + a.degats + (a.mod || a.modTxt ? " " + signed(a.mod || 0) + (a.modTxt ? " (" + a.modTxt + ")" : "") : "");
          line.appendChild(el("span", "hxh-dmg", dtxt));
          box.appendChild(line);
        }
        sar.appendChild(box);
      });
      colB.appendChild(sar);
    }

    if ((c.etats || []).length) {
      var set = section("États");
      set.appendChild(kvTable(c.etats.map(function (e) { return [e.name, e.effet]; })));
      colB.appendChild(set);
    }

    var ssens = section("Sens");
    ssens.appendChild(kvTable((c.sens || []).map(function (s) { return [s.name + " (" + s.niveau + ")", "acuité " + s.acuite]; })));
    colB.appendChild(ssens);

    // ---- colonne C (large) : compétences ----
    var scomp = section("Compétences");
    var champ = null;
    var listed = 0;
    (c.competences || []).forEach(function (k) {
      if (!k.invested) return;   // on n'affiche que les compétences investies (les autres = mod de carac)
      listed++;
      if (k.champ !== champ) { champ = k.champ; scomp.appendChild(el("div", "hxh-champ", "Champ " + champ)); }
      var row = el("div", "hxh-comp");
      row.appendChild(el("span", "hxh-comp-n", k.name));
      row.appendChild(el("span", "hxh-comp-c", k.carac));
      var tot = el("span", "hxh-comp-t", signed(k.total));
      rollEl(tot, k.name, k.roll);
      row.appendChild(tot);
      scomp.appendChild(row);
    });
    if (!listed) scomp.appendChild(el("div", "hxh-empty", "Aucun point investi ; chaque compétence vaut le modificateur de sa caractéristique. Les autres jets se lancent depuis le site."));
    scomp.appendChild(el("div", "hxh-note", "Toute compétence non listée vaut le modificateur de sa caractéristique."));
    colC.appendChild(scomp);

    if ((c.formations || []).length) {
      var sf = section("Formations");
      sf.appendChild(kvTable(c.formations.map(function (f) { return [f.name, f.info]; })));
      colC.appendChild(sf);
    }
    if ((c.arts || []).length) {
      var sart = section("Arts");
      sart.appendChild(kvTable(c.arts.map(function (a) {
        return [a.name + " · " + a.palier, [a.frappe ? "Frappe " + a.frappe : null, a.effet].filter(Boolean).join(" — ")];
      })));
      colC.appendChild(sart);
    }
    if ((c.avantages || []).length) {
      var sav = section("Avantages et handicaps");
      sav.appendChild(kvTable(c.avantages.map(function (a) { return [a.name, a.note]; })));
      colC.appendChild(sav);
    }
    if (c.notes) {
      var sn = section("Notes");
      sn.appendChild(el("div", "hxh-notes", c.notes));
      colC.appendChild(sn);
    }

    return wrap;
  }

  root.HxHRender = { card: card, rollCommand: rollCommand, sendToChat: sendToChat, signed: signed };
})(typeof window !== "undefined" ? window : this);
