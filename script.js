(function () {
  const data = window.EVENT_DATA;
  const stage = document.getElementById("stage");
  const transitionTrail = document.getElementById("transitionTrail");
  const progress = document.getElementById("progress");
  const musicToggle = document.getElementById("musicToggle");
  const blackout = document.getElementById("blackout");
  const menu = document.getElementById("menu");
  const menuList = document.getElementById("menuList");
  const menuClose = document.getElementById("menuClose");

  const state = {
    index: 0,
    gameStage: 0,
    black: false,
    menuOpen: false,
    transitioning: false,
    autoTimer: null,
    performanceVideoStarted: false,
    musicMuted: false,
    playedRevealEffects: new Set()
  };

  const transitionTiming = {
    leave: 650,
    enter: 980
  };

  const audioManager = {
    enabled: false,
    mode: null,
    pendingMode: null,
    tracks: {},
    effects: {},
    fadeTimers: {}
  };

  const bgmProfiles = {
    seatMap: { asset: "seatMapBgm", volume: 0.22, fadeIn: 2000 },
    award: { asset: "awardBgm", volume: 0.18, fadeIn: 1800 },
    game: { asset: "gameBgm", volume: 0.14, fadeIn: 1700 },
    closing: { asset: "closingBgm", volume: 0.18, fadeIn: 2000 }
  };

  const effectProfiles = {
    reveal: { asset: "revealSfx", volume: 0.58 }
  };

  const slides = buildSlides(data);

  renderMenu();
  renderSlide("is-active");
  bindEvents();
  updateMusicToggle();

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

      if (item.type === "speech-slides") {
        const images = item.images || [];
        if (!images.length) {
          built.push({
            kind: "speech",
            label: item.menuTitle || item.title,
            menuTitle: item.menuTitle || item.title,
            source: item
          });
          return;
        }
        images.forEach((image, imageIndex) => {
          built.push({
            kind: "speech-image",
            label: `${item.title} ${imageIndex + 1}`,
            menuTitle: imageIndex === 0 ? item.menuTitle || item.title : `${item.title} ${imageIndex + 1}`,
            source: item,
            image,
            imageIndex: imageIndex + 1,
            imageTotal: images.length
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
    clearAutoAdvance();
    const gameClass = slide.kind === "game-question" ? getGameClass(slide) : "";
    stage.className = `stage ${slide.kind} ${gameClass} ${motionClass}`;
    stage.innerHTML = "";
    if (slide.kind !== "warmup") addAtmosphere();

    const renderers = {
      "seat-map": renderSeatMap,
      opening: renderOpening,
      warmup: renderWarmup,
      breath: renderBreath,
      "award-title": renderAwardTitle,
      "award-list": renderAwardList,
      performance: renderPerformance,
      speech: renderSpeech,
      "speech-image": renderSpeechImage,
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
    scheduleMusicForSlide(slide);
    if (motionClass === "is-entering") {
      requestAnimationFrame(() => stage.classList.add("is-active"));
      window.setTimeout(() => stage.classList.remove("is-entering"), transitionTiming.enter);
    }
    if (slide.kind === "breath") {
      state.autoTimer = window.setTimeout(() => {
        if (!state.menuOpen && !state.black && !state.transitioning && slides[state.index]?.kind === "breath") {
          next();
        }
      }, 1450);
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

  function renderSeatMap(slide) {
    const item = slide.source;
    const safe = safeWrap();
    const frame = el("section", "seat-map-frame");
    frame.appendChild(imgEl(item.image || data.assets.seatMap, item.title));
    frame.appendChild(fallbackBox("座位表图片未找到"));
    safe.appendChild(frame);
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
  }

  function renderBreath(slide) {
    const item = slide.source;
    const safe = safeWrap();
    safe.appendChild(textEl("div", "topline", "章节"));
    safe.appendChild(textEl("h1", "headline", item.title));
    if (item.subtitle) safe.appendChild(textEl("p", "subhead", item.subtitle));
    stage.appendChild(el("div", "star-lights"));
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
      if (item.title === "飞跃奖与学科突破奖") {
        renderBreakthroughGroups(safe, slide.page.groups);
      } else {
        renderGroups(safe, slide.page.groups);
      }
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

  function renderBreakthroughGroups(container, groups) {
    const layout = el("section", "breakthrough-layout");
    const leap = groups.find((group) => group.label === "飞跃奖");
    const subjects = groups.filter((group) => group.label !== "飞跃奖");
    if (leap) {
      const block = el("div", "breakthrough-leap");
      block.appendChild(textEl("h2", "", "飞跃奖"));
      block.appendChild(textEl("p", "", leap.names.join("、")));
      layout.appendChild(block);
    }
    const subjectBlock = el("div", "breakthrough-subjects");
    subjectBlock.appendChild(textEl("h2", "", "学科突破奖"));
    subjects.forEach((group) => {
      const row = el("div", "breakthrough-row");
      row.appendChild(textEl("span", "breakthrough-subject", `${group.label.replace("学科突破奖（", "").replace("）", "")}：`));
      row.appendChild(textEl("span", "breakthrough-name", group.names.join("、")));
      subjectBlock.appendChild(row);
    });
    layout.appendChild(subjectBlock);
    container.appendChild(layout);
  }

  function renderPerformance(slide) {
    const item = slide.source;
    const safe = safeWrap();
    if (item.video) {
      stage.classList.add("has-performance-video");
      const videoWrap = el("div", "performance-video-wrap");
      const video = document.createElement("video");
      video.className = "performance-video";
      video.src = item.video;
      video.preload = "metadata";
      video.playsInline = true;
      video.addEventListener("error", () => videoWrap.classList.add("has-missing"));
      video.addEventListener("ended", () => {
        if (slides[state.index] === slide && !state.transitioning && state.index < slides.length - 1) {
          transitionTo(state.index + 1);
        }
      });
      videoWrap.appendChild(video);
      videoWrap.appendChild(fallbackBox(`视频未找到，请检查 ${item.video}`));
      stage.appendChild(videoWrap);
      safe.classList.add("performance-intro");
    }
    safe.appendChild(textEl("p", "section-label", item.subtitle || "表演节目"));
    safe.appendChild(textEl("h1", "program-title", `《${item.title}》`));
    safe.appendChild(textEl("div", "performer", item.performer));
    if (item.video) safe.appendChild(textEl("p", "video-hint", "按一次键开始播放"));
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

  function renderSpeechImage(slide) {
    const item = slide.source;
    const safe = safeWrap();
    const frame = el("section", "speech-slide-frame");
    frame.appendChild(imgEl(slide.image, item.title));
    frame.appendChild(fallbackBox("学生发言图片未找到"));
    const meta = el("div", "speech-slide-meta");
    meta.appendChild(textEl("span", "", item.title));
    meta.appendChild(textEl("span", "", `${slide.imageIndex}/${slide.imageTotal}`));
    frame.appendChild(meta);
    safe.appendChild(frame);
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
      "先看教室局部，再看物品线索，最后看老师照片",
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
    const mode = getGameMode(slide);
    const safe = safeWrap();
    const layout = el("div", "game-layout");

    const imageBox = el("div", "game-image");
    imageBox.appendChild(imgEl(slide.question.image, answer));
    imageBox.appendChild(fallbackBox("图片未找到"));
    layout.appendChild(imageBox);

    const copy = el("section", "game-copy");
    copy.appendChild(textEl("div", "game-tag", `${set.tag || set.title}｜${slide.number}/${slide.total}`));
    copy.appendChild(textEl("h1", "game-question", set.prompt));
    copy.appendChild(textEl("div", "game-step", gameStageText(state.gameStage, mode)));
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
    const gather = el("div", "closing-star-gather");
    for (let i = 0; i < 28; i += 1) {
      const star = el("i", "");
      star.style.setProperty("--x", `${randomBetween(8, 92, i + 301)}%`);
      star.style.setProperty("--y", `${randomBetween(10, 86, i + 617)}%`);
      star.style.setProperty("--delay", `${randomBetween(0.2, 2.3, i + 911).toFixed(2)}s`);
      gather.appendChild(star);
    }
    stage.appendChild(gather);
    const safe = safeWrap();
    safe.appendChild(textEl("div", "topline", "谢幕"));
    safe.appendChild(textEl("h1", "headline closing-thanks", item.title));
    const lines = el("div", "closing-lines");
    (item.lines || []).forEach((line) => lines.appendChild(textEl("div", "", line)));
    safe.appendChild(lines);
    if (item.staff?.length) {
      const staffBlock = el("div", "closing-staff");
      staffBlock.appendChild(textEl("p", "closing-staff-title", "演职人员名单"));
      const staffGrid = el("div", "closing-staff-grid");
      item.staff.forEach((group) => {
        const card = el("div", "closing-staff-item");
        card.appendChild(textEl("p", "closing-staff-role", group.role));
        card.appendChild(textEl("p", "closing-staff-names", (group.names || []).join("、")));
        staffGrid.appendChild(card);
      });
      staffBlock.appendChild(staffGrid);
      safe.appendChild(staffBlock);
    }
    safe.appendChild(textEl("h2", "closing-final", item.subtitle));
    stage.appendChild(el("div", "star-lights"));
    stage.appendChild(el("div", "closing-blackout"));
  }

  function safeWrap() {
    const safe = el("section", "safe");
    stage.appendChild(safe);
    return safe;
  }

  function bindEvents() {
    document.addEventListener("keydown", (event) => {
      unlockAudio();
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
      unlockAudio();
      if (!state.menuOpen && !state.black) next();
    });
    menu.addEventListener("click", (event) => {
      if (event.target === menu) closeMenu();
    });
    menuClose.addEventListener("click", closeMenu);
    musicToggle?.addEventListener("click", (event) => {
      event.stopPropagation();
      unlockAudio();
      toggleMusicMute();
    });
  }

  function next() {
    if (state.transitioning) return;
    const slide = slides[state.index];
    if (isVideoPerformance(slide) && !state.performanceVideoStarted) {
      startPerformanceVideo();
      return;
    }
    if (slide.kind === "game-question" && state.gameStage < getMaxGameStage(slide)) {
      state.gameStage += 1;
      playRevealEffectOnce(slide);
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
    clearAutoAdvance();
    stopActiveVideo();
    state.transitioning = true;
    transitionTrail.classList.remove("is-running");
    void transitionTrail.offsetWidth;
    transitionTrail.classList.add("is-running");
    stage.classList.remove("is-entering", "is-active");
    stage.classList.add("is-leaving");
    window.setTimeout(() => {
      state.index = nextIndex;
      state.gameStage = 0;
      renderSlide("is-entering");
      window.setTimeout(() => {
        state.transitioning = false;
      }, 140);
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
    clearAutoAdvance();
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
    const cleanVideo = slides[state.index]?.kind === "warmup";
    progress.hidden = cleanVideo;
    if (musicToggle) musicToggle.hidden = cleanVideo;
    progress.textContent = `${state.index + 1} / ${slides.length}`;
  }

  function toggleMusicMute() {
    state.musicMuted = !state.musicMuted;
    updateMusicToggle();
    if (!audioManager.enabled) return;
    if (state.musicMuted) {
      Object.keys(bgmProfiles).forEach((trackName) => fadeBgmTrack(trackName, 0, 900));
      return;
    }
    audioManager.mode = null;
    switchMusic(getMusicMode(slides[state.index]));
  }

  function updateMusicToggle() {
    if (!musicToggle) return;
    musicToggle.textContent = state.musicMuted ? "🔇" : "🔊";
    musicToggle.setAttribute("aria-pressed", state.musicMuted ? "true" : "false");
    musicToggle.setAttribute("aria-label", state.musicMuted ? "恢复背景音乐" : "关闭背景音乐");
  }

  function clearAutoAdvance() {
    if (state.autoTimer) {
      window.clearTimeout(state.autoTimer);
      state.autoTimer = null;
    }
  }

  function getGameMode(slide) {
    return slide.source.mode === "focus" ? "focus" : "direct";
  }

  function getMaxGameStage(slide) {
    return getGameMode(slide) === "focus" ? 1 : 1;
  }

  function getGameClass(slide) {
    const mode = getGameMode(slide);
    const maxStage = getMaxGameStage(slide);
    return `game-mode-${mode} game-stage-${state.gameStage} ${state.gameStage >= maxStage ? "game-revealed" : ""}`;
  }

  function imgEl(src, alt) {
    const img = document.createElement("img");
    img.src = src;
    img.alt = alt || "";
    // 汤涛涛老师的照片需要旋转180度摆正
    if (src.includes("汤涛涛老师")) {
      img.style.transform = "rotate(180deg)";
    }
    img.addEventListener("error", () => {
      img.classList.add("is-missing");
      img.closest(".game-image, .photo-media, .warmup-media, .speech-slide-frame, .seat-map-frame")?.classList.add("has-missing");
    });
    img.addEventListener("load", () => {
      img.classList.remove("is-missing");
      img.closest(".game-image, .photo-media, .warmup-media, .speech-slide-frame, .seat-map-frame")?.classList.remove("has-missing");
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

  function gameStageText(stageValue, mode) {
    if (stageValue === 0) return mode === "focus" ? "局部" : "猜测";
    return "揭晓";
  }

  function getMusicMode(slide) {
    if (slide.kind === "seat-map") return "seatMap";
    if (slide.kind === "breath") return "silent";
    if (slide.kind === "speech" || slide.kind === "speech-image") return "silent";
    if (slide.kind === "performance" && slide.source.video) return "silent";
    if (slide.kind.startsWith("game")) return "game";
    if (slide.kind === "closing") return "closing";
    if (slide.kind === "photo") return "silent";
    if (slide.kind === "award-list") return "award";
    return "silent";
  }

  function scheduleMusicForSlide(slide) {
    const mode = getMusicMode(slide);
    audioManager.pendingMode = mode;
    if (audioManager.enabled) {
      switchMusic(mode);
    } else if (mode !== "silent") {
      tryAutoplayMusic(mode);
    }
  }

  function unlockAudio() {
    if (audioManager.enabled) return;
    audioManager.enabled = true;
    const targetMode = audioManager.pendingMode || getMusicMode(slides[state.index]);
    switchMusic(targetMode);
  }

  function switchMusic(mode) {
    if (audioManager.mode === mode) return;
    Object.keys(bgmProfiles).forEach((trackName) => {
      const profile = bgmProfiles[trackName];
      const targetVolume = !state.musicMuted && trackName === mode ? profile.volume : 0;
      const duration = targetVolume > 0 ? profile.fadeIn : 1500;
      fadeBgmTrack(trackName, targetVolume, duration);
    });
    audioManager.mode = mode;
    if (mode === "closing") {
      window.setTimeout(() => {
        if (!state.musicMuted && audioManager.mode === "closing") {
          fadeBgmTrack("closing", 0.34, 6000);
        }
      }, 220);
    }
  }

  function tryAutoplayMusic(mode) {
    if (state.musicMuted || audioManager.enabled || !bgmProfiles[mode]) return;
    const audio = ensureBgmTrack(mode);
    const profile = bgmProfiles[mode];
    if (!audio || !profile) return;
    audio.volume = 0;
    audio
      .play()
      .then(() => {
        audioManager.enabled = true;
        audioManager.mode = null;
        switchMusic(mode);
      })
      .catch(() => {
        audio.pause();
      });
  }

  function ensureBgmTrack(trackName) {
    if (audioManager.tracks[trackName]) return audioManager.tracks[trackName];
    const profile = bgmProfiles[trackName];
    const src = profile ? data.assets?.[profile.asset] : "";
    if (!src) return null;
    const audio = new Audio(src);
    audio.loop = true;
    audio.preload = "auto";
    audio.volume = 0;
    audioManager.tracks[trackName] = audio;
    return audio;
  }

  function fadeBgmTrack(trackName, targetVolume, duration) {
    const audio = ensureBgmTrack(trackName);
    if (!audio) return;
    if (audioManager.fadeTimers[trackName]) {
      window.clearInterval(audioManager.fadeTimers[trackName]);
      audioManager.fadeTimers[trackName] = null;
    }
    const start = audio.volume;
    const startedAt = performance.now();
    if (targetVolume > 0 && audio.paused) {
      audio.muted = false;
      audio.play().catch(() => {});
    }
    audioManager.fadeTimers[trackName] = window.setInterval(() => {
      const elapsed = performance.now() - startedAt;
      const ratio = Math.min(1, elapsed / duration);
      const nextVolume = start + (targetVolume - start) * ratio;
      audio.volume = Math.max(0, Math.min(1, nextVolume));
      if (ratio >= 1) {
        window.clearInterval(audioManager.fadeTimers[trackName]);
        audioManager.fadeTimers[trackName] = null;
        if (targetVolume === 0) audio.pause();
      }
    }, 40);
  }

  function playRevealEffectOnce(slide) {
    const key = `${state.index}:${slide.question.image}`;
    if (state.playedRevealEffects.has(key)) return;
    state.playedRevealEffects.add(key);
    playSoundEffect("reveal");
  }

  function playSoundEffect(effectName) {
    if (state.musicMuted) return;
    const base = ensureSoundEffect(effectName);
    const profile = effectProfiles[effectName];
    if (!base || !profile) return;
    const audio = base.cloneNode(true);
    audio.volume = profile.volume;
    audio.play().catch(() => {});
  }

  function ensureSoundEffect(effectName) {
    if (audioManager.effects[effectName]) return audioManager.effects[effectName];
    const profile = effectProfiles[effectName];
    const src = profile ? data.assets?.[profile.asset] : "";
    if (!src) return null;
    const audio = new Audio(src);
    audio.preload = "auto";
    audio.volume = profile.volume;
    audioManager.effects[effectName] = audio;
    return audio;
  }

  function isVideoPerformance(slide) {
    return slide.kind === "performance" && Boolean(slide.source.video);
  }

  function startPerformanceVideo() {
    const video = stage.querySelector(".performance-video");
    if (!video) return;
    state.performanceVideoStarted = true;
    stage.classList.add("video-started");
    switchMusic("video");
    video.muted = false;
    video.volume = 1;
    try {
      video.currentTime = 0;
    } catch {
      // Some browsers may delay seeking until metadata is ready.
    }
    video.play().catch(() => {
      video.controls = true;
    });
  }

  function stopActiveVideo() {
    const video = stage.querySelector(".performance-video");
    if (!video) {
      state.performanceVideoStarted = false;
      return;
    }
    video.pause();
    try {
      video.currentTime = 0;
    } catch {
      // Ignore seek failures while unloading the slide.
    }
    state.performanceVideoStarted = false;
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
