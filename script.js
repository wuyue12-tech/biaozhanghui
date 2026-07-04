(function () {
  const data = window.EVENT_DATA;
  const stage = document.getElementById("stage");
  const progress = document.getElementById("progress");
  const blackout = document.getElementById("blackout");
  const menu = document.getElementById("menu");
  const menuList = document.getElementById("menuList");
  const menuClose = document.getElementById("menuClose");

  const state = {
    index: 0,
    gameStage: 0,
    black: false,
    menuOpen: false,
    transitioning: false
  };

  const transitionTiming = {
    leave: 380,
    enter: 700
  };

  const slides = buildSlides(data);

  renderMenu();
  renderSlide("is-active");
  bindEvents();

  function buildSlides(source) {
    const built = [];
    const gameSets = getGameSets(source);
    source.program.forEach((item) => {
      if (item.type === "award") {
        built.push({
          kind: "award-title",
          label: item.title,
          menuTitle: item.title,
          source: item
        });
        const listSlides = paginateAward(item);
        listSlides.forEach((page, pageIndex) => {
          built.push({
            kind: "award-list",
            label: listSlides.length > 1 ? `${item.title} 名单 ${pageIndex + 1}` : `${item.title} 名单`,
            menuTitle: listSlides.length > 1 ? `${item.title} 名单 ${pageIndex + 1}` : `${item.title} 名单`,
            source: item,
            page,
            pageIndex,
            pageTotal: listSlides.length
          });
        });
        return;
      }

      if (item.type === "game") {
        built.push({
          kind: "game-title",
          label: item.title,
          menuTitle: item.menuTitle || item.title,
          source: item
        });
        built.push({
          kind: "game-rule",
          label: "游戏规则",
          menuTitle: "游戏规则",
          source: item
        });
        gameSets.forEach((set) => {
          built.push({
            kind: "game-set",
            label: set.title,
            menuTitle: set.title,
            source: set
          });
          set.questions.forEach((question, idx) => {
            built.push({
              kind: "game-question",
              label: `${set.tag || set.title} ${idx + 1}`,
              menuTitle: `${set.tag || set.title} ${idx + 1}`,
              source: set,
              question,
              number: idx + 1,
              total: set.questions.length
            });
          });
        });
        return;
      }

      built.push({
        kind: item.type,
        label: item.menuTitle || item.title,
        menuTitle: item.menuTitle || item.title,
        source: item
      });
    });
    return built;
  }

  function getGameSets(source) {
    if (Array.isArray(window.GAME_DATA) && window.GAME_DATA.length) {
      return window.GAME_DATA;
    }
    return source.games || [];
  }

  function paginateAward(item) {
    if (item.groups) {
      return [{ groups: item.groups }];
    }
    const names = item.names || [];
    if (names.length === 0) {
      return [{ names: [] }];
    }
    const pageSize = names.length > 44 ? 32 : 44;
    const pages = [];
    for (let i = 0; i < names.length; i += pageSize) {
      pages.push({ names: names.slice(i, i + pageSize) });
    }
    return pages;
  }

  function renderSlide(motionClass = "is-entering") {
    const slide = slides[state.index];
    state.gameStage = slide.kind === "game-question" ? state.gameStage : 0;
    stage.className = `stage ${slide.kind} ${slide.kind === "game-question" ? `game-stage-${state.gameStage}` : ""} ${motionClass}`;
    stage.innerHTML = "";
    addAtmosphere();

    const renderers = {
      opening: renderOpening,
      warmup: renderWarmup,
      "award-title": renderAwardTitle,
      "award-list": renderAwardList,
      performance: renderPerformance,
      speech: renderSpeech,
      "game-title": renderGameTitle,
      "game-rule": renderGameRule,
      "game-set": renderGameSet,
      "game-question": renderGameQuestion,
      photo: renderPhoto,
      closing: renderClosing
    };
    renderers[slide.kind](slide);
    updateProgress();
    syncMenuActive();
    if (motionClass === "is-entering") {
      requestAnimationFrame(() => stage.classList.add("is-active"));
      window.setTimeout(() => stage.classList.remove("is-entering"), transitionTiming.enter);
    }
  }

  function addAtmosphere() {
    stage.appendChild(el("div", "cosmic-horizon"));
    stage.appendChild(el("div", "shooting-star"));
    stage.appendChild(el("div", "star-river"));
    const orbit = el("div", "orbit");
    stage.appendChild(orbit);
    for (let i = 0; i < 54; i += 1) {
      const star = el("i", "star");
      star.style.setProperty("--x", `${randomBetween(2, 98, i + 11)}%`);
      star.style.setProperty("--y", `${randomBetween(2, 96, i + 29)}%`);
      star.style.setProperty("--size", `${randomBetween(1.3, 4.2, i + 47)}px`);
      star.style.setProperty("--alpha", randomBetween(0.34, 0.96, i + 83).toFixed(2));
      star.style.setProperty("--speed", `${randomBetween(2.4, 6.2, i + 113).toFixed(2)}s`);
      stage.appendChild(star);
    }
  }

  function renderOpening(slide) {
    const item = slide.source;
    const safe = safeWrap();
    safe.appendChild(textEl("div", "topline", item.eyebrow));
    safe.appendChild(textEl("h1", "headline", item.title));
    safe.appendChild(textEl("p", "subhead", item.subtitle));
    if (data.eventDate) safe.appendChild(textEl("div", "event-date", data.eventDate));
    safe.appendChild(textEl("p", "opening-line", "每一颗星，都在成长。"));
    safe.appendChild(textEl("div", "hosts", data.hosts));
    stage.appendChild(el("div", "star-lights"));
  }

  function renderWarmup(slide) {
    const item = slide.source;
    const media = el("div", "warmup-media");
    const fallback = imgEl(item.fallbackImage || data.assets.signwall, "成长影像暖场");
    const video = document.createElement("video");
    video.muted = true;
    video.loop = true;
    video.autoplay = true;
    video.playsInline = true;
    video.src = item.video || data.assets.warmupVideo;
    video.addEventListener("loadeddata", () => {
      media.classList.add("has-video");
      video.play().catch(() => {});
    });
    media.appendChild(fallback);
    media.appendChild(video);
    media.appendChild(fallbackBox("将活动照片视频命名为 warmup.mp4 放入 video 文件夹后，会在这里自动播放。"));
    stage.appendChild(media);

    const safe = safeWrap();
    safe.appendChild(textEl("div", "topline", "开场暖场"));
    safe.appendChild(textEl("h1", "headline compact", item.title));
    safe.appendChild(textEl("p", "subhead", item.subtitle));
  }

  function renderAwardTitle(slide) {
    const item = slide.source;
    stage.appendChild(el("div", "award-glow"));
    stage.appendChild(el("div", "award-star"));
    const safe = safeWrap();
    safe.appendChild(textEl("div", "topline", item.category || "奖项"));
    safe.appendChild(textEl("h1", "headline", item.title));
    if (item.subtitle) safe.appendChild(textEl("p", "subhead", item.subtitle));
    stage.appendChild(el("div", "star-lights"));
  }

  function renderAwardList(slide) {
    const item = slide.source;
    const safe = safeWrap();
    const head = el("div", "list-head");
    const titleBlock = el("div");
    titleBlock.appendChild(textEl("p", "list-subtitle", item.category || "获奖名单"));
    titleBlock.appendChild(textEl("h1", "list-title", item.title));
    head.appendChild(titleBlock);
    const count = getAwardCount(slide.page);
    head.appendChild(textEl("div", "count-badge", count ? `${count} 人` : "名单待补充"));
    safe.appendChild(head);

    if (slide.page.groups) {
      renderGroups(safe, slide.page.groups);
      return;
    }

    const names = slide.page.names || [];
    if (!names.length) {
      safe.appendChild(textEl("div", "placeholder-list", "请在 data.js 中补充获奖者"));
      return;
    }

    const grid = el("div", "name-grid");
    grid.style.setProperty("--cols", getColumnCount(names.length));
    grid.style.setProperty("--name-size", getNameSize(names.length));
    names.forEach((name, index) => {
      const node = textEl("div", "name-chip", name);
      node.style.setProperty("--i", index);
      grid.appendChild(node);
    });
    safe.appendChild(grid);
  }

  function renderGroups(container, groups) {
    const grid = el("div", "group-grid");
    groups.forEach((group) => {
      const card = el("section", "group-card");
      card.appendChild(textEl("p", "group-label", group.label));
      card.appendChild(textEl("p", "group-names", group.names.join("、")));
      grid.appendChild(card);
    });
    container.appendChild(grid);
  }

  function renderPerformance(slide) {
    const item = slide.source;
    const safe = safeWrap();
    safe.appendChild(textEl("p", "section-label", item.subtitle || "表演节目"));
    safe.appendChild(textEl("h1", "program-title", `《${item.title}》`));
    safe.appendChild(textEl("div", "performer", item.performer));
    if (item.quiet) stage.appendChild(el("div", "quiet-mark"));
  }

  function renderSpeech(slide) {
    const item = slide.source;
    const safe = safeWrap();
    const card = el("section", "speech-card");
    card.appendChild(textEl("p", "section-label", item.title));
    card.appendChild(textEl("h1", "program-title", item.speaker));
    safe.appendChild(card);
  }

  function renderGameTitle(slide) {
    const item = slide.source;
    const safe = safeWrap();
    safe.appendChild(textEl("div", "topline", "互动小游戏"));
    safe.appendChild(textEl("h1", "headline", item.title));
    safe.appendChild(textEl("p", "subhead", item.subtitle));
    stage.appendChild(el("div", "star-lights"));
  }

  function renderGameRule() {
    const safe = safeWrap();
    safe.appendChild(textEl("div", "topline", "互动规则"));
    safe.appendChild(textEl("h1", "headline", "老师鉴定局"));
    const rules = el("div", "rule-lines");
    [
      "请每个导师班派一名同学上台抢答",
      "看局部，猜老师；看物品，猜主人；看照片，猜教室",
      "准备好了吗？"
    ].forEach((line) => rules.appendChild(textEl("p", "", line)));
    safe.appendChild(rules);
    stage.appendChild(el("div", "star-lights"));
  }

  function renderGameSet(slide) {
    const item = slide.source;
    const safe = safeWrap();
    safe.appendChild(textEl("div", "topline", "小游戏"));
    safe.appendChild(textEl("h1", "headline", item.title));
    safe.appendChild(textEl("p", "subhead", item.prompt));
    stage.appendChild(el("div", "star-lights"));
  }

  function renderGameQuestion(slide) {
    const set = slide.source;
    const answer = slide.question.answer || deriveAnswer(slide.question.image);
    const safe = safeWrap();
    const layout = el("div", "game-layout");

    const imageBox = el("div", "game-image");
    imageBox.appendChild(imgEl(slide.question.image, answer));
    imageBox.appendChild(fallbackBox("图片未找到"));
    layout.appendChild(imageBox);

    const copy = el("section", "game-copy");
    copy.appendChild(textEl("div", "game-tag", `${set.tag || set.title}｜${slide.number}/${slide.total}`));
    copy.appendChild(textEl("h1", "game-question", set.prompt));
    copy.appendChild(textEl("div", "game-step", gameStageText(state.gameStage)));
    const answerBox = el("div", "answer-box");
    answerBox.appendChild(textEl("p", "answer-label", "答案"));
    answerBox.appendChild(textEl("p", "answer-name", answer));
    copy.appendChild(answerBox);
    layout.appendChild(copy);

    safe.appendChild(layout);
  }

  function renderPhoto(slide) {
    const item = slide.source;
    const media = el("div", "photo-media");
    media.appendChild(imgEl(item.image || data.assets.signwall, item.title));
    media.appendChild(fallbackBox("合影背景未找到"));
    stage.appendChild(media);
    const safe = safeWrap();
    safe.appendChild(textEl("div", "topline", "合影"));
    safe.appendChild(textEl("h1", "headline", item.title));
    safe.appendChild(textEl("p", "subhead", item.subtitle));
  }

  function renderClosing(slide) {
    const item = slide.source;
    const safe = safeWrap();
    safe.appendChild(textEl("div", "topline", "谢幕"));
    safe.appendChild(textEl("h1", "headline", item.title));
    safe.appendChild(textEl("p", "subhead", item.subtitle));
    const lines = el("div", "closing-lines");
    (item.lines || []).forEach((line) => lines.appendChild(textEl("div", "", line)));
    safe.appendChild(lines);
    stage.appendChild(el("div", "star-lights"));
  }

  function safeWrap() {
    const safe = el("section", "safe");
    stage.appendChild(safe);
    return safe;
  }

  function bindEvents() {
    document.addEventListener("keydown", (event) => {
      if (event.key === "f" || event.key === "F") {
        event.preventDefault();
        toggleFullscreen();
        return;
      }
      if (event.key === "b" || event.key === "B") {
        event.preventDefault();
        toggleBlackout();
        return;
      }
      if (event.key === "m" || event.key === "M" || event.key === "Escape") {
        event.preventDefault();
        toggleMenu();
        return;
      }
      if (state.menuOpen || state.black) return;
      if (event.key === "ArrowRight" || event.key === " " || event.key === "PageDown") {
        event.preventDefault();
        next();
      }
      if (event.key === "ArrowLeft" || event.key === "PageUp") {
        event.preventDefault();
        prev();
      }
    });

    stage.addEventListener("click", () => {
      if (!state.menuOpen && !state.black) next();
    });
    menu.addEventListener("click", (event) => {
      if (event.target === menu) closeMenu();
    });
    menuClose.addEventListener("click", closeMenu);
  }

  function next() {
    if (state.transitioning) return;
    const slide = slides[state.index];
    if (slide.kind === "game-question" && state.gameStage < 2) {
      state.gameStage += 1;
      renderSlide("is-active");
      return;
    }
    if (state.index < slides.length - 1) {
      transitionTo(state.index + 1);
    }
  }

  function prev() {
    if (state.transitioning) return;
    const slide = slides[state.index];
    if (slide.kind === "game-question" && state.gameStage > 0) {
      state.gameStage -= 1;
      renderSlide("is-active");
      return;
    }
    if (state.index > 0) {
      transitionTo(state.index - 1);
    }
  }

  function transitionTo(nextIndex) {
    if (nextIndex === state.index || state.transitioning) return;
    state.transitioning = true;
    stage.classList.remove("is-entering", "is-active");
    stage.classList.add("is-leaving");
    window.setTimeout(() => {
      state.index = nextIndex;
      state.gameStage = 0;
      renderSlide("is-entering");
      window.setTimeout(() => {
        state.transitioning = false;
      }, transitionTiming.enter);
    }, transitionTiming.leave);
  }

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen?.();
    } else {
      document.exitFullscreen?.();
    }
  }

  function toggleBlackout() {
    state.black = !state.black;
    blackout.hidden = !state.black;
  }

  function toggleMenu() {
    state.menuOpen ? closeMenu() : openMenu();
  }

  function openMenu() {
    state.menuOpen = true;
    menu.hidden = false;
    syncMenuActive();
  }

  function closeMenu() {
    state.menuOpen = false;
    menu.hidden = true;
  }

  function renderMenu() {
    menuList.innerHTML = "";
    slides.forEach((slide, index) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "menu-item";
      button.dataset.index = String(index);
      button.innerHTML = `<span class="menu-index">${String(index + 1).padStart(2, "0")}</span><span class="menu-title">${escapeHtml(slide.menuTitle || slide.label)}</span>`;
      button.addEventListener("click", () => {
        closeMenu();
        transitionTo(index);
      });
      menuList.appendChild(button);
    });
  }

  function syncMenuActive() {
    menuList.querySelectorAll(".menu-item").forEach((button) => {
      button.classList.toggle("active", Number(button.dataset.index) === state.index);
    });
  }

  function updateProgress() {
    progress.textContent = `${state.index + 1} / ${slides.length}`;
  }

  function imgEl(src, alt) {
    const img = document.createElement("img");
    img.src = src;
    img.alt = alt || "";
    img.addEventListener("error", () => {
      img.classList.add("is-missing");
      img.closest(".game-image, .photo-media, .warmup-media")?.classList.add("has-missing");
    });
    img.addEventListener("load", () => {
      img.classList.remove("is-missing");
      img.closest(".game-image, .photo-media, .warmup-media")?.classList.remove("has-missing");
    });
    return img;
  }

  function fallbackBox(message) {
    return textEl("div", "image-fallback", message);
  }

  function el(tag, className) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    return node;
  }

  function textEl(tag, className, text) {
    const node = el(tag, className);
    node.textContent = text || "";
    return node;
  }

  function getAwardCount(page) {
    if (page.groups) return page.groups.reduce((sum, group) => sum + group.names.length, 0);
    return (page.names || []).length;
  }

  function getColumnCount(count) {
    if (count <= 1) return 1;
    if (count <= 6) return 2;
    if (count <= 18) return 3;
    return 4;
  }

  function getNameSize(count) {
    if (count <= 1) return "4.2vw";
    if (count <= 6) return "3.05vw";
    if (count <= 18) return "2.35vw";
    return "1.95vw";
  }

  function deriveAnswer(path) {
    const filename = decodeURIComponent(path.split("/").pop() || "");
    return filename
      .replace(/\.[^.]+$/, "")
      .replace(/^已移除背景的/, "")
      .replace(/\s+\d+$/, "")
      .replace(/老师的奖品$/, "老师")
      .replace(/的奖品$/, "")
      .trim();
  }

  function gameStageText(stageValue) {
    if (stageValue === 0) return "出题";
    if (stageValue === 1) return "聚焦";
    return "揭晓";
  }

  function randomBetween(min, max, seed) {
    const raw = Math.sin(seed * 999) * 10000;
    const value = raw - Math.floor(raw);
    return value * (max - min) + min;
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }
})();
