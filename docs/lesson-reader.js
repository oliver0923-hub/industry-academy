/* Industry Academy: render lessons 00–02 inside the existing #lesson/N route.
   The previous standalone HTML files are read-only content sources, not navigation destinations. */
"use strict";
window.IndustryInlineReader = (() => {
  const sourceFiles = {
    0: "./lesson-00-reading-v2.html",
    1: "./lesson-01.html",
    2: "./lesson-02-reading.html"
  };
  const storagePrefix = "industry-academy-inline-reading-";
  let generation = 0;
  let cleanup = () => {};

  const get = key => { try { return localStorage.getItem(key); } catch (_) { return null; } };
  const put = (key, value) => { try { localStorage.setItem(key, value); } catch (_) {} };
  const escapeHTML = s => String(s).replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[c]);

  function leave() { generation++; cleanup(); cleanup = () => {}; }

  async function mount(id, host, opts = {}) {
    leave();
    if (!sourceFiles[id] || !host) return;
    const myGeneration = generation;
    const controller = new AbortController();
    const subscriptions = [];
    cleanup = () => {
      controller.abort();
      for (const unbind of subscriptions) unbind();
    };
    const listen = (target, name, fn, options) => {
      target.addEventListener(name, fn, options);
      subscriptions.push(() => target.removeEventListener(name, fn, options));
    };
    host.innerHTML = '<div class="inline-reader-loading" role="status">正在載入完整課文…</div>';

    let response, raw, doc, source;
    try {
      response = await fetch(sourceFiles[id] + "?inline=20261108b", {
        signal: controller.signal, cache: "no-cache"
      });
      if (!response.ok) throw new Error("HTTP " + response.status);
      raw = await response.text();
      doc = new DOMParser().parseFromString(raw, "text/html");
      source = id === 0 ? doc.querySelector("main#lesson-content") :
               id === 1 ? doc.querySelector("article.reader") :
                          doc.querySelector("main.reading-main");
      if (!source) throw new Error("沒有找到課文主體");
    } catch (error) {
      if (controller.signal.aborted || myGeneration !== generation) return;
      host.innerHTML =
        '<div class="inline-reader-error"><h2>暫時無法載入課文</h2>' +
        '<p>檢查網站是否已發布此堂內容，或重新整理頁面。原因：' +
        escapeHTML(error.message || "讀取失敗") + '</p>' +
        '<button class="btn btn-primary" type="button" id="inline-retry">重新載入課文</button></div>';
      const retry = host.querySelector("#inline-retry");
      if (retry) retry.onclick = () => mount(id, host, opts);
      return;
    }
    if (controller.signal.aborted || myGeneration !== generation || !host.isConnected) return;

    const copy = source.cloneNode(true);
    // The lesson scripts manage separate HTML pages. Unified controls replace them here.
    copy.querySelectorAll("script, iframe, object, embed, .mobile-toc, .completion").forEach(el => el.remove());
    copy.querySelectorAll("#mark-read, #reader, #lesson-content, #read-label").forEach(el => {
      if (el.id === "mark-read" || el.id === "read-label") el.remove();
      else el.removeAttribute("id");
    });
    // The Lesson 00 footer has a link to an old standalone page; the router owns navigation.
    for (const a of copy.querySelectorAll('a[href]')) {
      const href = a.getAttribute("href") || "";
      const match = href.match(/(?:^|\/)lesson-(0[012])(?:-reading(?:-v2)?)?\.html(?:[#?].*)?$/);
      if (match) a.setAttribute("href", "./lesson.html?lesson=" + String(Number(match[1])).padStart(2, "0"));
      if (/^\.\/index\.html#lesson\/[012]$/.test(href)) {
        a.setAttribute("href", "./lesson.html?lesson=" + href.at(-1).padStart(2, "0"));
      }
      if (/^#lesson\/[012]$/.test(href)) a.setAttribute("href", "./lesson.html?lesson=0" + href.at(-1));
      if (id === 1 && a.textContent.includes("返回第 01 堂課程頁")) { a.setAttribute("href", "./index.html#catalog"); a.textContent = "← 返回課程目錄"; }
      if (/^javascript:/i.test(href.trim())) a.removeAttribute("href");
    }
    for (const h of copy.querySelectorAll("h2")) {
      if (!h.id && h.parentElement?.matches("section[id]")) continue;
      if (!h.id) h.id = "inline-section-" + [...copy.querySelectorAll("h2")].indexOf(h);
    }
    const headings = [...copy.querySelectorAll("h2")].filter(h => h.closest("article, .lesson-text, .article"));
    const targetFor = h => h.id || h.closest("section[id]")?.id || "";
    const chapters = headings.map(h => ({ id: targetFor(h), label: h.textContent.trim().replace(/\s+/g, " ") }))
      .filter(x => x.id && x.label);
    const optionsHTML = chapters.map((x, i) =>
      '<option value="' + escapeHTML(x.id) + '">' + escapeHTML((i + 1) + " · " + x.label) + "</option>"
    ).join("");
    const tocHTML = chapters.map(x =>
      '<button type="button" data-chapter="' + escapeHTML(x.id) + '">' + escapeHTML(x.label) + "</button>"
    ).join("");
    const prior = (() => { try { return JSON.parse(get(storagePrefix + id) || "null"); } catch (_) { return null; } })();
    const priorLabel = prior && prior.percent > 1 ? "接續閱讀 (" + Math.round(prior.percent) + "%)" : "接續閱讀";
    host.innerHTML =
      '<div class="inline-reader-shell" data-lesson="' + id + '">' +
      '<div class="inline-reader-actions">' +
      '<a href="#catalog" class="inline-reader-back">← 返回全部課程</a>' +
      '<span class="inline-reader-draft">教材候選稿・編輯審查中</span>' +
      '<div class="inline-reader-spacer"></div>' +
      '<button id="inline-resume" type="button"' + (!prior || !prior.percent ? " disabled" : "") +
        '>' + escapeHTML(priorLabel) + '</button>' +
      '<button id="inline-font" type="button" aria-pressed="false">字級 A+</button>' +
      '<button id="inline-mark" type="button" aria-pressed="' + !!opts.isMarked + '">' +
         (opts.isMarked ? "✓ 已自行標記完成" : "自行標記完成") + '</button>' +
      '</div><div class="inline-reader-progress" aria-label="課程閱讀進度"><span id="inline-progress-bar"></span></div>' +
      '<div class="inline-reader-layout">' +
      '<aside class="inline-reader-toc" aria-label="本堂課章節目錄"><div class="inline-reader-toc-card">' +
      '<strong>本堂課章節</strong><nav>' + tocHTML + '</nav>' +
      '<p id="inline-percent">閱讀進度 0%</p></div></aside>' +
      '<div class="inline-reader-body">' +
      '<label class="inline-reader-mobile-toc">跳至本堂章節' +
      '<select id="inline-jump"><option value="">選擇章節…</option>' + optionsHTML + '</select></label>' +
      '<div class="inline-reader-prose">' + copy.innerHTML + '</div>' +
      '<p class="inline-reader-endnote">閱讀位置會儲存在目前瀏覽器；只有自行標記才計入學習進度。本文仍在編輯審查中。</p>' +
      '</div></div>' +
      '<dialog class="inline-reader-zoom" id="inline-zoom" aria-label="放大教學圖表">' +
      '<button type="button" id="inline-close-zoom">關閉 ✕</button><div id="inline-zoom-content"></div></dialog>' +
      '</div>';
    const shell = host.querySelector(".inline-reader-shell");

    const previousNext = document.createElement("nav");
    previousNext.className = "inline-reader-next";
    previousNext.setAttribute("aria-label", "上一堂與下一堂");
    const navigationItems = [
      id > 0 ? {target:id-1,label:"← 上一堂 · "+String(id-1).padStart(2,"0")} : null,
      id < 2 ? {target:id+1,label:"下一堂 · "+String(id+1).padStart(2,"0")+" →"} : {target:null,label:"返回全部課程 →"}
    ].filter(Boolean);
    for (const item of navigationItems) {
      const link = document.createElement("a");
      link.href = item.target === null ? "./index.html#catalog" : "./lesson.html?lesson="+String(item.target).padStart(2,"0");
      link.textContent = item.label;
      previousNext.append(link);
    }
    host.querySelector(".inline-reader-endnote")?.before(previousNext);

    const prose = shell.querySelector(".inline-reader-prose");
    const jump = shell.querySelector("#inline-jump");
    const progressBar = shell.querySelector("#inline-progress-bar");
    const percent = shell.querySelector("#inline-percent");
    const dialog = shell.querySelector("#inline-zoom");
    const tocButtons = [...shell.querySelectorAll("[data-chapter]")];
    let lastPersist = 0;
    let hasScrolled = false;

    const scrollToChapter = (key, behavior = "smooth") => {
      const elem = [...prose.querySelectorAll("[id]")].find(x => x.id === key);
      if (!elem) return;
      const y = window.scrollY + elem.getBoundingClientRect().top - 92;
      window.scrollTo({ top: Math.max(0, y), behavior });
    };
    const readPercent = () => {
      const start = Math.max(0, window.scrollY + prose.getBoundingClientRect().top - 150);
      const length = Math.max(1, prose.offsetHeight - window.innerHeight * 0.55);
      return Math.max(0, Math.min(100, 100 * (window.scrollY - start) / length));
    };
    const update = () => {
      if (!host.isConnected) return;
      const pct = readPercent();
      progressBar.style.width = pct.toFixed(1) + "%";
      percent.textContent = "本堂閱讀進度 " + Math.round(pct) + "%";
      const current = chapters.filter(c => {
        const h = [...prose.querySelectorAll("[id]")].find(e => e.id === c.id);
        return h && h.getBoundingClientRect().top < 165;
      }).at(-1);
      for (const btn of tocButtons) {
        btn.classList.toggle("active", !!current && btn.dataset.chapter === current.id);
      }
      if (hasScrolled && Date.now() - lastPersist > 750) {
        const relative = Math.max(0, window.scrollY - (window.scrollY + prose.getBoundingClientRect().top));
        put(storagePrefix + id, JSON.stringify({
          percent: pct, offset: relative, chapter: current?.id || "", savedAt: Date.now()
        }));
        lastPersist = Date.now();
      }
    };
    listen(window, "scroll", () => { hasScrolled = true; update(); }, { passive: true });
    listen(window, "resize", update);
    listen(shell, "click", event => {
      const chapterBtn = event.target.closest("[data-chapter]");
      if (chapterBtn) { scrollToChapter(chapterBtn.dataset.chapter); return; }
      const link = event.target.closest('a[href^="#"]');
      if (link) {
        const value = link.getAttribute("href").substring(1);
        if (!value || value.startsWith("lesson/") || value === "catalog" || value === "home") return;
        if ([...prose.querySelectorAll("[id]")].some(x => x.id === decodeURIComponent(value))) {
          event.preventDefault(); scrollToChapter(decodeURIComponent(value));
        }
      }
      const figure = event.target.closest(".figure[data-zoom], .figure-expand");
      if (figure && !figure.closest("dialog")) {
        const clone = figure.cloneNode(true);
        clone.removeAttribute("data-zoom");
        clone.querySelectorAll("[data-zoom]").forEach(x => x.removeAttribute("data-zoom"));
        shell.querySelector("#inline-zoom-content").replaceChildren(clone);
        if (!dialog.open) dialog.showModal();
      }
    });
    listen(shell, "keydown", event => {
      const figure = event.target.closest(".figure[data-zoom]");
      if (figure && (event.key === "Enter" || event.key === " ")) {
        event.preventDefault(); figure.click();
      }
    });
    listen(jump, "change", () => {
      if (jump.value) scrollToChapter(jump.value);
    });
    listen(shell.querySelector("#inline-close-zoom"), "click", () => dialog.close());
    listen(dialog, "click", event => { if (event.target === dialog) dialog.close(); });
    listen(shell.querySelector("#inline-font"), "click", event => {
      const enlarged = shell.classList.toggle("large-font");
      event.currentTarget.setAttribute("aria-pressed", String(enlarged));
      event.currentTarget.textContent = enlarged ? "字級 A−" : "字級 A+";
      update();
    });
    listen(shell.querySelector("#inline-resume"), "click", () => {
      const state = (() => { try { return JSON.parse(get(storagePrefix + id) || "null"); } catch (_) { return null; } })();
      if (!state) return;
      if (Number.isFinite(state.offset)) {
        const start = window.scrollY + prose.getBoundingClientRect().top;
        window.scrollTo({ top: start + state.offset, behavior: "smooth" });
      } else if (state.chapter) scrollToChapter(state.chapter, "smooth");
      else if (Number.isFinite(state.percent)) {
        const start = window.scrollY + prose.getBoundingClientRect().top;
        window.scrollTo({ top: start + prose.offsetHeight * state.percent / 100, behavior: "smooth" });
      }
    });
    listen(shell.querySelector("#inline-mark"), "click", event => {
      const next = event.currentTarget.getAttribute("aria-pressed") !== "true";
      event.currentTarget.setAttribute("aria-pressed", String(next));
      event.currentTarget.textContent = next ? "✓ 已自行標記完成" : "自行標記完成";
      if (opts.onMark) opts.onMark(next);
    });
    update();
  }

  return { mount, leave };
})();
