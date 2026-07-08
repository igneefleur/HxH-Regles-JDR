// Glossaire au survol : affiche la carte d'une valeur (poids / vitesse) quand on
// la survole dans un tableau .gloss-source. Les cartes sont définies, masquées,
// par le glossaire auto-append (.gloss-defs .gloss-card[data-key]).
// Le survol est limité aux tableaux .gloss-source pour ne pas toucher les autres
// occurrences (portées d'armes, tailles…). Compatible navigation.instant.
(function () {
  function init() {
    const cards = document.querySelectorAll(".gloss-defs .gloss-card");
    if (!cards.length) return;
    const defs = {};
    cards.forEach((c) => { defs[c.dataset.key] = c.outerHTML; });

    let tip = document.getElementById("gloss-tip");
    if (!tip) {
      tip = document.createElement("div");
      tip.id = "gloss-tip";
      tip.className = "gloss-tip md-typeset";
      document.body.appendChild(tip);
    }

    function hide() { tip.style.display = "none"; }
    function show(td, key) {
      tip.innerHTML = defs[key];
      tip.style.display = "block";
      const r = td.getBoundingClientRect();
      const w = tip.offsetWidth;
      const h = tip.offsetHeight;
      let top = window.scrollY + r.top - h - 8;        // au-dessus de la cellule
      if (r.top - h - 8 < 0) top = window.scrollY + r.bottom + 8;  // sinon en dessous
      let left = window.scrollX + r.left + r.width / 2 - w / 2;
      const min = window.scrollX + 6;
      const max = window.scrollX + document.documentElement.clientWidth - w - 6;
      left = Math.max(min, Math.min(left, max));
      tip.style.top = top + "px";
      tip.style.left = left + "px";
    }

    document.querySelectorAll(".gloss-source td").forEach((td) => {
      const key = td.textContent.trim();
      if (!defs[key] || td.dataset.gloss) return;
      td.dataset.gloss = "1";
      td.classList.add("gloss-trigger");
      td.addEventListener("mouseenter", () => show(td, key));
      td.addEventListener("mouseleave", hide);
    });
  }

  if (window.document$) document$.subscribe(init);
  else document.addEventListener("DOMContentLoaded", init);
})();
