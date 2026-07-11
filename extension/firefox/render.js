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

  // ---------------------------------------------------------------------------
  // Jumeau LECTURE SEULE de la fiche du site : mêmes classes pc-* et même CSS
  // (creation.css est injecté tel quel dans le shadow root, avec les polices du
  // livre embarquées), pour un rendu IDENTIQUE au site. Les seules différences
  // avec la fiche du site sont l'absence des contrôles d'édition (pas/steppers,
  // champs) : les lignes concernées sont réagencées par sheet-extra.css
  // (.pc-ro-mode). onRoll(label, value) est appelé au clic sur une valeur.
  // ---------------------------------------------------------------------------
  function sheet(c, onRoll) {
    c = c || {};
    var root = el("div", "perso-atelier pc-ro-mode");
    var sh = el("div", "pc-sheet");
    root.appendChild(sh);

    function rollEl(node, label, value) {
      node.classList.add("pc-rollable");
      node.title = "Cliquer pour lancer les dés (" + (c.de || "1d100") + ").";
      node.addEventListener("click", function () { if (onRoll) onRoll(label, value); });
      return node;
    }
    function block(title, small, note) {
      var b = el("div", "pc-block");
      var t = el("div", "pc-block-title");
      t.appendChild(document.createTextNode(title));
      if (small) { t.appendChild(document.createTextNode(" ")); t.appendChild(el("small", null, small)); }
      b.appendChild(t);
      if (note) b.appendChild(el("div", "pc-block-note", note));
      return b;
    }

    // ---- en-tête d'identité (grille pc-id) ----
    var head = el("div", "pc-head");
    var brand = el("div", "pc-brand");
    if (c.portrait) {
      var img = el("img", "pc-portrait");
      img.src = c.portrait; img.alt = c.name || "Portrait";
      img.addEventListener("error", function () { img.style.display = "none"; });
      brand.appendChild(img);
    } else {
      brand.appendChild(el("span", "b1", "HxH"));
      brand.appendChild(el("span", "b2", "Système JDR"));
    }
    head.appendChild(brand);
    var grid = el("div", "pc-id");
    function roField(cls, label, value) {
      var f = el("div", "pc-f " + cls);
      f.appendChild(el("label", null, label));
      f.appendChild(el("span", "pc-ro", value === "" || value == null ? "—" : String(value)));
      grid.appendChild(f);
    }
    var id = c.identity || {};
    var eclatTxt = id.eclatA != null ? (id.eclatA + (id.eclatN != null && id.eclatN !== id.eclatA ? " (naissance " + id.eclatN + ")" : "")) : "—";
    roField("c6", "Nom", id.nom || c.name);
    roField("c3", "Niveau", id.niveau != null ? id.niveau + (id.pf != null ? " (" + id.pf + " PF)" : "") : "—");
    roField("c3", "Classe", id.classe);
    roField("c3", "Genre", id.genre);
    roField("c2", "Âge", id.age ? id.age + " ans" : "");
    roField("c2", "Taille", id.taille ? id.taille + " m" : "");
    roField("c2", "Poids", id.poids ? id.poids + " kg" : "");
    roField("c3", "Catégorie", id.categorie);
    roField("c3", "Bourse", (id.bourse || 0) + " Ɉ");
    roField("c4", "Éclat", eclatTxt);
    head.appendChild(grid);
    sh.appendChild(head);

    // ---- trois colonnes (comme l'onglet Général du site) ----
    var cols = el("div", "pc-cols3 pc-cols-gen");
    var colA = el("div", "pc-col");
    var colB = el("div", "pc-col");
    var colC = el("div", "pc-col pc-col-comps");
    cols.appendChild(colA); cols.appendChild(colB); cols.appendChild(colC);
    sh.appendChild(cols);

    // ===== colonne A : caractéristiques + capacités =====
    var bCar = block("Caractéristiques");
    [["physique", "Physiques"], ["mentale", "Mentales"]].forEach(function (grp) {
      var caracs = (c.caracs || []).filter(function (k) { return k.groupe === grp[0]; });
      if (!caracs.length) return;
      var h = el("div", "pc-trow pc-carac-row head");
      h.appendChild(el("span", null, ""));
      h.appendChild(el("span", null, grp[1]));
      h.appendChild(el("span", "pc-cell-num", "Valeur"));
      h.appendChild(el("span", "pc-cell-num", "Mod"));
      bCar.appendChild(h);
      caracs.forEach(function (k) {
        var row = el("div", "pc-trow pc-carac-row");
        row.appendChild(el("span", "pc-abbr", k.abbr));
        row.appendChild(el("span", null, k.name));
        row.appendChild(el("span", "val", String(k.val)));
        row.appendChild(el("span", "mod", signed(k.mod)));
        bCar.appendChild(row);
      });
    });
    // repli si les caracs n'ont pas de groupe (ancienne carte)
    if (!bCar.querySelector(".pc-carac-row")) {
      (c.caracs || []).forEach(function (k) {
        var row = el("div", "pc-trow pc-carac-row");
        row.appendChild(el("span", "pc-abbr", k.abbr));
        row.appendChild(el("span", null, k.name));
        row.appendChild(el("span", "val", String(k.val)));
        row.appendChild(el("span", "mod", signed(k.mod)));
        bCar.appendChild(row);
      });
    }
    colA.appendChild(bCar);

    var cap = c.capacites || {};
    function cap3(labels, values) {
      var row = el("div", "pc-cap3" + (labels.length > 3 ? " pc-cap5" : ""));
      labels.forEach(function (lbl, i) {
        var cell = el("div", "c");
        cell.appendChild(el("span", "k", lbl));
        cell.appendChild(el("span", "v", (values && values[i]) || "—"));
        row.appendChild(cell);
      });
      return row;
    }
    if ((cap.mouvement || []).length) {
      var bMov = block("Mouvement", "par round");
      bMov.appendChild(cap3(["Marche", "Course", "Sprint"], cap.mouvement));
      colA.appendChild(bMov);
    }
    if ((cap.port || []).length) {
      var bPort = block("Port");
      bPort.appendChild(cap3(["Sans fatigue", "Vrai effort", "Pleine puiss."], cap.port));
      colA.appendChild(bPort);
    }
    if ((cap.apnee || []).length || (cap.sommeil || []).length) {
      var bSouf = block("Souffle et sommeil");
      bSouf.appendChild(kvRO([
        ["Apnée", (cap.apnee || []).join(" · ") || "—"],
        ["Sommeil et activité", (cap.sommeil || []).join(" · ") || "—"]
      ]));
      colA.appendChild(bSouf);
    }

    // ===== colonne B : combat + armes + états + sens =====
    var cb = c.combat || {};
    var bCom = block("Combat");
    var bigrow = el("div", "pc-bigrow");
    [["Initiative", cb.init], ["Esquive", cb.esquive], ["Parade", cb.parade]].forEach(function (d) {
      var box = el("div", "pc-big");
      box.appendChild(el("span", "k", d[0]));
      box.appendChild(el("span", "v", signed(d[1] || 0)));
      rollEl(box, d[0], d[1] || 0);
      bigrow.appendChild(box);
    });
    bCom.appendChild(bigrow);
    bCom.appendChild(kvRO(
      [["PV", (cb.pv != null ? cb.pv : "—") + " / " + (cb.pvMax != null ? cb.pvMax : "—")],
       ["Points de fatigue", (cb.fatigue != null ? cb.fatigue : "—") + " / " + (cb.fatigueMax != null ? cb.fatigueMax : "—")]]
      .concat(cb.modGlobal ? [["Mod. à toutes les actions", signed(cb.modGlobal)]] : [])));
    colB.appendChild(bCom);

    if ((c.armes || []).length) {
      var bArm = block("Armes");
      (c.armes).forEach(function (a) {
        var box = el("div", "pc-arme");
        var ah = el("div", "pc-arme-head");
        ah.appendChild(el("span", "nm", a.name));
        ah.appendChild(el("span", "fam", (a.corps ? "arme de corps · " : "") + (a.famille || (a.forge ? "arme forgée (Forge)" : "")) + (a.am ? " · AM " + a.am : "")));
        box.appendChild(ah);
        if (a.unknown) {
          box.appendChild(el("div", "pc-arme-line", a.forge
            ? "Valeurs à l'appréciation du MJ : la fiche de cette arme vit dans la Forge."
            : "Arme absente du barème actuel."));
        } else {
          var line = el("div", "pc-arme-line");
          (a.attaques || []).forEach(function (t) {
            var chip = el("span", "pc-wchip");
            chip.textContent = t.label + " " + signed(t.roll);
            rollEl(chip, a.name + " (" + t.label + ")", t.roll);
            line.appendChild(chip);
          });
          if (a.parade != null) {
            var pchip = el("span", "pc-wchip");
            pchip.textContent = "Parade " + signed(a.parade);
            rollEl(pchip, a.name + " (Parade)", a.parade);
            line.appendChild(pchip);
          }
          line.appendChild(el("span", "dmg", "Dégâts " + a.degats +
            (a.mod || a.modTxt ? " " + signed(a.mod || 0) + (a.modTxt ? " (" + a.modTxt + ")" : "") : "")));
          if (a.munitions) line.appendChild(el("span", "mun", "Munitions " + a.munitions));
          box.appendChild(line);
        }
        bArm.appendChild(box);
      });
      colB.appendChild(bArm);
    }

    if ((c.etats || []).length) {
      var bEt = block("États");
      var sum = el("div", "pc-etat-sum");
      c.etats.forEach(function (e) {
        var line = el("div", "pc-etat-line");
        line.appendChild(el("b", null, e.name));
        line.appendChild(document.createTextNode(" " + (e.effet || "")));
        sum.appendChild(line);
      });
      bEt.appendChild(sum);
      colB.appendChild(bEt);
    }

    if ((c.sens || []).length) {
      var bSens = block("Sens");
      var sh2 = el("div", "pc-trow pc-sens-row head");
      sh2.appendChild(el("span", null, "Sens"));
      sh2.appendChild(el("span", "niv", "Niveau"));
      sh2.appendChild(el("span", "pc-cell-num", "Acuité"));
      bSens.appendChild(sh2);
      c.sens.forEach(function (s) {
        var row = el("div", "pc-trow pc-sens-row");
        row.appendChild(el("span", "nm", s.name));
        row.appendChild(el("span", "niv", s.niveau));
        row.appendChild(el("span", "acu", String(s.acuite)));
        bSens.appendChild(row);
      });
      colB.appendChild(bSens);
    }

    // ===== colonne C : compétences + formations + arts + avantages + notes =====
    var bComp = block("Compétences", null,
      "Compétences investies (les autres valent le modificateur de leur caractéristique). Cliquer un total pour lancer.");
    var list = el("div", "pc-comp-list");
    var champ = null, listed = 0;
    (c.competences || []).forEach(function (k) {
      if (!k.invested) return;
      listed++;
      if (k.champ !== champ) { champ = k.champ; list.appendChild(el("div", "pc-comp-champ", "Champ " + champ)); }
      var row = el("div", "pc-comp-row");
      row.appendChild(el("span", "pc-comp-name", k.name));
      row.appendChild(el("span", "pc-comp-carac", k.carac));
      var tot = el("span", "pc-comp-total");
      tot.textContent = signed(k.total);
      rollEl(tot, k.name, k.roll);
      row.appendChild(tot);
      list.appendChild(row);
    });
    if (!listed) list.appendChild(el("div", "pc-empty", "Aucun point investi ; chaque compétence vaut le modificateur de sa caractéristique."));
    bComp.appendChild(list);
    colC.appendChild(bComp);

    if ((c.formations || []).length) {
      var bForm = block("Formations");
      c.formations.forEach(function (f) {
        var line = el("div", "pc-av");
        line.appendChild(el("b", null, f.name));
        if (f.info) line.appendChild(el("span", "note", " — " + f.info));
        bForm.appendChild(line);
      });
      colC.appendChild(bForm);
    }

    if ((c.arts || []).length) {
      var bArts = block("Arts");
      var wrap3 = el("div", "pc-arts3");
      c.arts.forEach(function (a) {
        var ac = el("div", "pc-art-card");
        var ah2 = el("div", "pc-art-head");
        ah2.appendChild(el("span", "pc-art-name", a.name));
        if (a.palier) ah2.appendChild(el("span", "pc-art-tag", a.palier));
        ac.appendChild(ah2);
        if (a.frappe) ac.appendChild(el("div", "pc-art-frappe", "Frappe " + a.frappe));
        if (a.effet) ac.appendChild(el("div", "pc-art-effet", a.effet));
        wrap3.appendChild(ac);
      });
      bArts.appendChild(wrap3);
      colC.appendChild(bArts);
    }

    if ((c.avantages || []).length) {
      var bAv = block("Avantages et handicaps");
      c.avantages.forEach(function (a) {
        var line = el("div", "pc-av");
        line.appendChild(el("b", null, a.name));
        if (a.note) line.appendChild(el("span", "note", " — " + a.note));
        bAv.appendChild(line);
      });
      colC.appendChild(bAv);
    }

    if (c.notes) {
      var bN = block("Notes et histoire");
      bN.appendChild(el("div", "pc-ro-notes", c.notes));
      colC.appendChild(bN);
    }

    return root;
  }

  // petites lignes label / valeur (pc-kv), en lecture seule
  function kvRO(rows) {
    var t = el("div", "pc-kv-list");
    rows.forEach(function (r) {
      var row = el("div", "pc-kv");
      row.appendChild(el("span", "k", r[0]));
      row.appendChild(el("span", "v", r[1]));
      t.appendChild(row);
    });
    return t;
  }

  // CSS de la fiche, injecté DANS le shadow root du pane par le content script
  // Roll20 : le shadow isole totalement le CSS de Roll20 (ses règles n'atteignent
  // pas le shadow, les nôtres n'en sortent pas). On neutralise en plus, sur la
  // racine, les propriétés HÉRITÉES (police, couleur, alignement…) qui, seules,
  // traverseraient la frontière depuis l'hôte Roll20.
  var paneCss = [
    ":host { display: block; }",
    ":host, .hxh-panel, .hxh-panel * { box-sizing: border-box; }",
    ".hxh-panel { display:flex; flex-direction:column; background:#fff; color:#1c1c1c; font:13px/1.35 'Segoe UI',Arial,sans-serif; text-align:left; letter-spacing:normal; word-spacing:normal; text-transform:none; text-indent:0; white-space:normal; font-variant:normal; }",
    ":host(.hxh-host-floating) .hxh-panel { height:100%; border:2px solid #111; }",
    ".hxh-bar { display:flex; align-items:center; gap:10px; padding:8px 12px; background:#111; color:#fff; flex:0 0 auto; position:sticky; top:0; z-index:2; }",
    ".hxh-bar-title { font-weight:700; letter-spacing:.04em; font-size:15px; color:#fff; }",
    ".hxh-select { min-width:220px; padding:5px 8px; border:1px solid #555; border-radius:4px; background:#fff; color:#111; font:inherit; }",
    ".hxh-btn { margin-left:4px; padding:5px 12px; border:1px solid #555; border-radius:4px; background:#f5f5f5; color:#111; font:inherit; cursor:pointer; }",
    ".hxh-btn:hover { background:#fff; }",
    ".hxh-close { margin-left:auto; background:#a11212; color:#fff; border-color:#7c0e0e; }",
    ".hxh-close:hover { background:#7c0e0e; }",
    ".hxh-body { flex:1 1 auto; padding:14px 18px 24px; background:#fff; overflow:visible; }",
    // la fiche pc-* apporte son propre fond (parchemin) et ses marges : pas de cadre blanc
    ".hxh-body-sheet { padding:0; background:transparent; }",
    ":host(.hxh-host-floating) .hxh-body { overflow:auto; }",
    ".hxh-card { max-width:1180px; margin:0 auto; }",
    ".hxh-head { display:flex; align-items:flex-start; gap:12px; border-bottom:3px double #555; padding-bottom:8px; margin-bottom:12px; }",
    ".hxh-portrait { width:66px; height:66px; object-fit:cover; border:2px solid #111; }",
    ".hxh-name { font-size:22px; font-weight:700; color:#7c0e0e; }",
    ".hxh-sub { font-size:12px; color:#555; margin-top:3px; }",
    ".hxh-cols { display:grid; grid-template-columns:1fr 1fr 1.5fr; gap:18px; align-items:start; }",
    "@media (max-width:900px) { .hxh-cols { grid-template-columns:1fr; } }",
    ".hxh-col { display:flex; flex-direction:column; gap:14px; min-width:0; }",
    ".hxh-sec-title { margin:0 0 6px; font-size:15px; font-weight:700; color:#111; border-bottom:1px solid #bbb; padding-bottom:3px; }",
    ".hxh-kvs { display:flex; flex-direction:column; }",
    ".hxh-kv { display:grid; grid-template-columns:minmax(0,10rem) 1fr; gap:8px; padding:2px 0; border-bottom:1px dotted #ddd; }",
    ".hxh-k { color:#555; font-size:12px; }",
    ".hxh-v { font-variant-numeric:tabular-nums; }",
    ".hxh-carac-grid { display:flex; flex-direction:column; }",
    ".hxh-carac { display:grid; grid-template-columns:2.4rem 1fr 2.4rem 2.6rem; gap:6px; align-items:baseline; padding:2px 3px; }",
    ".hxh-carac:nth-child(even) { background:#f2f2f2; }",
    ".hxh-abbr { font-weight:700; color:#7c0e0e; font-size:12px; }",
    ".hxh-cn { overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }",
    ".hxh-cv { text-align:center; font-weight:700; font-variant-numeric:tabular-nums; }",
    ".hxh-cm { text-align:right; color:#7c0e0e; font-variant-numeric:tabular-nums; }",
    ".hxh-big-row { display:grid; grid-template-columns:repeat(3,1fr); gap:8px; margin-bottom:8px; }",
    ".hxh-big { border:2px solid #111; text-align:center; padding:6px 4px; }",
    ".hxh-big-k { display:block; font-size:11px; font-weight:700; text-transform:uppercase; color:#333; letter-spacing:.04em; }",
    ".hxh-big-v { display:block; font-size:22px; font-weight:700; font-variant-numeric:tabular-nums; }",
    ".hxh-arme { border-bottom:1px dotted #ccc; padding:5px 2px; }",
    ".hxh-arme-h { display:flex; align-items:baseline; gap:8px; }",
    ".hxh-arme-n { font-weight:700; }",
    ".hxh-arme-f { font-size:11px; color:#777; }",
    ".hxh-arme-line { display:flex; flex-wrap:wrap; align-items:baseline; gap:6px 8px; margin-top:4px; }",
    ".hxh-wchip { border:1px solid #555; background:#f2f2f2; padding:2px 7px; font-weight:700; font-size:12px; font-variant-numeric:tabular-nums; }",
    ".hxh-dmg { font-weight:700; }",
    ".hxh-champ { font-weight:700; text-transform:uppercase; font-size:12px; letter-spacing:.06em; color:#111; margin:8px 0 2px; border-bottom:1px solid #ddd; }",
    ".hxh-comp { display:grid; grid-template-columns:1fr 2.6rem 3rem; gap:8px; align-items:baseline; padding:2px 3px; }",
    ".hxh-comp:nth-child(even) { background:#f7f7f7; }",
    ".hxh-comp-n { overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }",
    ".hxh-comp-c { font-size:11px; color:#7c0e0e; font-weight:700; text-align:right; }",
    ".hxh-comp-t { text-align:right; font-weight:700; font-variant-numeric:tabular-nums; }",
    ".hxh-note { font-size:11px; color:#777; font-style:italic; margin-top:6px; }",
    ".hxh-empty { font-size:12px; color:#777; font-style:italic; padding:8px 2px; }",
    ".hxh-notes { white-space:pre-wrap; font-size:12px; }",
    ".hxh-roll { cursor:pointer; }",
    ".hxh-roll:hover { color:#a11212; text-decoration:underline; }",
    ".hxh-big.hxh-roll:hover { text-decoration:none; border-color:#a11212; }",
    ".hxh-big.hxh-roll:hover .hxh-big-v { color:#a11212; }",
    ".hxh-wchip.hxh-roll:hover { border-color:#a11212; color:#a11212; }"
  ].join("\n");

  root.HxHRender = { card: card, sheet: sheet, rollCommand: rollCommand, sendToChat: sendToChat, signed: signed, paneCss: paneCss };
})(typeof window !== "undefined" ? window : this);
