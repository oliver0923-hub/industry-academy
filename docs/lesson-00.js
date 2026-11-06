"use strict";
(() => {
  const key = "industry-academy-lesson00-candidate-position-v1";
  let previous = {};
  try { previous = JSON.parse(localStorage.getItem(key) || "{}"); } catch (_) {}
  if (!previous || typeof previous !== "object") previous = {};
  let marked = previous.selfMarked === true;
  const label = document.getElementById("position-label");
  const resume = document.getElementById("resume-reading");
  const mark = document.getElementById("mark-read");
  const toc = document.getElementById("lesson-toc");
  toc.open = window.matchMedia("(min-width: 881px)").matches;
  function position() {
    const max = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
    return max ? Math.max(0, Math.min(100, Math.round(window.scrollY / max * 100))) : 0;
  }
  function persist() {
    try { localStorage.setItem(key, JSON.stringify({ scrollY: window.scrollY, percent: position(), selfMarked: marked })); } catch (_) {}
  }
  function display() {
    const percent = position();
    document.getElementById("reading-bar").style.width = percent + "%";
    label.textContent = "目前位置 " + percent + "%";
    mark.textContent = marked ? "已自行標記已讀・取消" : "自行標記已讀";
    mark.setAttribute("aria-pressed", String(marked));
  }
  if (Number.isFinite(previous.scrollY) && previous.scrollY > 100) {
    resume.hidden = false;
    resume.textContent = "回到上次位置（" + Math.min(100, Math.max(0, Number(previous.percent) || 0)) + "%）";
    resume.addEventListener("click", () => { window.scrollTo({ top: previous.scrollY, behavior: "instant" }); resume.hidden = true; });
  }
  mark.addEventListener("click", () => { marked = !marked; persist(); display(); });
  let scheduled = false;
  window.addEventListener("scroll", () => {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(() => { display(); persist(); scheduled = false; });
  }, { passive: true });
  window.addEventListener("resize", display);
  window.addEventListener("pagehide", persist);
  const viewer = document.getElementById("figure-viewer");
  document.querySelectorAll(".figure-expand").forEach(button => {
    button.addEventListener("click", () => {
      const image = button.querySelector("img");
      const zoom = document.getElementById("zoom-image");
      zoom.src = image.src; zoom.alt = image.alt;
      document.getElementById("figure-title").textContent = image.alt;
      viewer.showModal();
    });
  });
  display();
})();
