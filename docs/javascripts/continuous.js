// Lecture continue du livre + arbre de navigation custom (chargement paresseux).
//
//   - L'arbre de gauche (custom) liste TOUS les chapitres ; sous le chapitre
//     ACTIF, ses sous-sections (dès que la page est chargée).
//   - Les pages voisines se chargent à l'approche du haut / du bas (paresseux).
//     À l'ouverture, une page précédente est amorcée pour pouvoir remonter.
//   - Le chapitre/section actif est détecté à ~45 % de l'écran.
//   - Cliquer une section ne défile jamais au-delà du bas de sa page (la page
//     suivante n'apparaît pas, le surlignage reste sur la bonne page).
(function () {
  const SCOPE = "/content/livre/";
  const ACTIVE_LINE = "-45% 0px -55% 0px";
  let observers = [];
  let cleanups = [];

  function teardown() {
    observers.forEach(o => o.disconnect());
    cleanups.forEach(fn => fn());
    observers = [];
    cleanups = [];
  }

  function headerOffset() {
    const h = document.querySelector(".md-header");
    const t = document.querySelector(".md-tabs");
    return (h ? h.offsetHeight : 0) + (t ? t.offsetHeight : 0);
  }

  // Défile vers `target` sans dépasser le bas de sa page `page` : la page
  // suivante ne peut donc pas apparaître.
  function scrollToInPage(target, page, smooth) {
    const off = headerOffset() + 6;
    const pageTopY = page.getBoundingClientRect().top + window.scrollY - off;
    const pageBottomY = page.getBoundingClientRect().bottom + window.scrollY;
    let y = target.getBoundingClientRect().top + window.scrollY - off;
    const maxY = pageBottomY - window.innerHeight;
    if (maxY > pageTopY) y = Math.min(y, maxY);
    y = Math.max(y, pageTopY);
    window.scrollTo({ top: Math.max(0, y), behavior: smooth ? "smooth" : "auto" });
  }

  function sectionTitle(h) {
    const clone = h.cloneNode(true);
    clone.querySelectorAll(".headerlink").forEach(x => x.remove());
    return clone.textContent.trim();
  }

  async function fetchArticle(url) {
    const res = await fetch(url, { cache: "no-cache" });
    if (!res.ok) throw new Error("HTTP " + res.status);
    const doc = new DOMParser().parseFromString(await res.text(), "text/html");
    return { title: doc.title, article: doc.querySelector(".md-content__inner") };
  }

  function makeFrag(article) {
    const frag = document.createElement("div");
    frag.className = "cont-page";
    while (article.firstChild) frag.appendChild(article.firstChild);
    return frag;
  }

  // Surbrillance temporaire d'un titre (pour repérer où l'on a atterri).
  function flash(el) {
    if (!el) return;
    el.classList.remove("cont-flash");
    void el.offsetWidth; // reflow : relance l'animation même au reclic
    el.classList.add("cont-flash");
    setTimeout(() => el.classList.remove("cont-flash"), 1600);
  }

  function init() {
    teardown();
    const isBook = location.pathname.includes(SCOPE);
    document.body.classList.toggle("book-mode", isBook);
    if (!isBook) return;

    const inner = document.querySelector(".md-content__inner");
    if (!inner) return;
    inner.classList.add("cont-active");

    // On modifie l'URL via replaceState pendant le scroll : on fige donc les
    // liens de nav en absolu (résolus maintenant, avant tout replaceState),
    // sinon l'onglet Accueil — relatif — finirait par pointer vers /content/.
    document.querySelectorAll('.md-tabs__link, a.md-logo').forEach(a => {
      a.setAttribute('href', a.href);
    });

    const firstPage = document.createElement("div");
    firstPage.className = "cont-page";
    while (inner.firstChild) firstPage.appendChild(inner.firstChild);

    const bookPages = [...document.querySelectorAll('.md-sidebar--primary .md-nav__link[href]')]
      .map(el => ({ el, u: new URL(el.href) }))
      .filter(o => o.u.hash === "" && o.u.pathname.includes(SCOPE))
      .map(o => ({ path: o.u.pathname, url: o.u.href, title: o.el.textContent.trim() }));

    const curIdx = bookPages.findIndex(p => p.path === location.pathname);
    if (curIdx < 0) { inner.appendChild(firstPage); return; }

    const pageEls = {};
    const chapterEls = {};
    const sections = [];
    let loadedTop = curIdx, loadedBottom = curIdx;
    let loadingDown = false, loadingUp = false;

    // Verrou : un clic fige le chapitre actif jusqu'au prochain défilement.
    let suppressAuto = false;
    function release() { suppressAuto = false; }
    ["wheel", "touchmove", "keydown"].forEach(ev =>
      window.addEventListener(ev, release, { passive: true }));
    cleanups.push(() =>
      ["wheel", "touchmove", "keydown"].forEach(ev =>
        window.removeEventListener(ev, release)));

    // ----- Arbre custom -----
    const scrollwrap = document.querySelector(".md-sidebar--primary .md-sidebar__scrollwrap");
    const bookNav = document.createElement("nav");
    bookNav.className = "book-nav";
    const rootUl = document.createElement("ul");
    bookNav.appendChild(rootUl);

    function setActiveSection(rec) {
      sections.forEach(s => s.link.classList.toggle("active", s === rec));
    }
    function activate(el) {
      const path = el.dataset.path;
      if (!path) return;
      if (location.pathname !== path) {
        history.replaceState(history.state, "", el.dataset.url);
        if (el.dataset.title) document.title = el.dataset.title;
      }
      Object.keys(chapterEls).forEach(p =>
        chapterEls[p].classList.toggle("active", p === path));
    }

    bookPages.forEach(p => {
      const li = document.createElement("li");
      li.className = "book-chapter";
      const a = document.createElement("a");
      a.className = "book-link";
      a.textContent = p.title;
      a.href = p.url;
      a.addEventListener("click", ev => {
        const page = pageEls[p.path];
        if (!page) return; // pas chargé : on suit le lien (navigation)
        ev.preventDefault();
        suppressAuto = true;
        activate(page);
        scrollToInPage(page, page, true);
        flash(page.querySelector("h1") || page);
      });
      const secUl = document.createElement("ul");
      secUl.className = "book-sections";
      li.appendChild(a);
      li.appendChild(secUl);
      rootUl.appendChild(li);
      chapterEls[p.path] = li;
    });
    if (scrollwrap) {
      const old = scrollwrap.querySelector(".book-nav");
      if (old) old.remove();
      scrollwrap.appendChild(bookNav);
    }

    // ----- Observateurs de scroll (chapitre + section courants) -----
    const obsActive = new IntersectionObserver(
      entries => entries.forEach(e => {
        if (e.isIntersecting && !suppressAuto) activate(e.target);
      }),
      { rootMargin: ACTIVE_LINE }
    );
    const obsSection = new IntersectionObserver(
      entries => entries.forEach(e => {
        if (e.isIntersecting && !suppressAuto) {
          const rec = sections.find(s => s.h2 === e.target);
          if (rec) setActiveSection(rec);
        }
      }),
      { rootMargin: ACTIVE_LINE }
    );

    function registerPage(pageEl, meta) {
      pageEl.dataset.path = meta.path;
      pageEl.dataset.url = meta.url;
      if (meta.title) pageEl.dataset.title = meta.title;
      pageEls[meta.path] = pageEl;
      obsActive.observe(pageEl);
      const secUl = chapterEls[meta.path] &&
        chapterEls[meta.path].querySelector(".book-sections");
      if (secUl && !secUl.childElementCount) {
        pageEl.querySelectorAll("h2").forEach(h => {
          const item = document.createElement("li");
          const a = document.createElement("a");
          a.className = "book-sec";
          a.textContent = sectionTitle(h);
          a.href = "#" + (h.id || "");
          const rec = { h2: h, link: a, path: meta.path };
          a.addEventListener("click", ev => {
            ev.preventDefault();
            suppressAuto = true;
            activate(pageEl);
            setActiveSection(rec);
            scrollToInPage(h, pageEl, true);
            flash(h);
          });
          item.appendChild(a);
          secUl.appendChild(item);
          sections.push(rec);
          obsSection.observe(h);
        });
      }
    }

    // ----- Sentinelles + chargement paresseux -----
    inner.appendChild(firstPage);
    registerPage(firstPage, { ...bookPages[curIdx], title: document.title });

    const bottom = document.createElement("div");
    bottom.className = "cont-sentinel";
    inner.appendChild(bottom);
    const top = document.createElement("div");
    top.className = "cont-sentinel";
    inner.insertBefore(top, inner.firstChild);

    async function loadNext() {
      if (loadingDown || loadedBottom >= bookPages.length - 1) return;
      loadingDown = true;
      try {
        const i = loadedBottom + 1;
        const t = bookPages[i];
        const res = await fetchArticle(t.url);
        if (res.article) {
          const el = makeFrag(res.article);
          inner.insertBefore(el, bottom);
          registerPage(el, { ...t, title: res.title });
        }
        loadedBottom = i;
      } catch (_) {
        loadedBottom = bookPages.length;
      } finally {
        loadingDown = false;
      }
    }

    async function loadPrev() {
      if (loadingUp || loadedTop <= 0) return;
      loadingUp = true;
      try {
        const i = loadedTop - 1;
        const t = bookPages[i];
        const res = await fetchArticle(t.url);
        if (res.article) {
          const el = makeFrag(res.article);
          const before = document.documentElement.scrollHeight;
          inner.insertBefore(el, top.nextSibling);
          const after = document.documentElement.scrollHeight;
          window.scrollBy(0, after - before);
          registerPage(el, { ...t, title: res.title });
        }
        loadedTop = i;
      } catch (_) {
        loadedTop = 0;
      } finally {
        loadingUp = false;
      }
    }

    const obsDown = new IntersectionObserver(
      e => { if (e[0].isIntersecting) loadNext(); },
      { rootMargin: "600px 0px" }
    );
    obsDown.observe(bottom);
    const obsTop = new IntersectionObserver(
      e => { if (e[0].isIntersecting) loadPrev(); },
      { rootMargin: "600px 0px" }
    );
    obsTop.observe(top);

    observers.push(obsActive, obsSection, obsDown, obsTop);
  }

  if (window.document$) {
    document$.subscribe(init);
  } else {
    document.addEventListener("DOMContentLoaded", init);
  }
})();
