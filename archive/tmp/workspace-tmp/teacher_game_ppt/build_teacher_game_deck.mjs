import fs from "node:fs/promises";
import path from "node:path";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const ROOT = "/Users/wuyue/Documents/自主管理学院";
const OUT_DIR = path.join(ROOT, "outputs");
const HTML_DIR = path.join(ROOT, "output/老师鉴定局");
const FINAL_PPTX = path.join(OUT_DIR, "老师鉴定局_抢话筒答题版.pptx");
const PREVIEW_DIR = path.join(ROOT, "tmp/teacher_game_ppt/preview");
const AUDIO_PATH = path.join(HTML_DIR, "teacher_game_bgm.wav");

const W = 1280;
const H = 720;
const C = {
  ink: "#111111",
  paper: "#FFFAF1",
  white: "#FFFFFF",
  red: "#D92D20",
  blue: "#2563EB",
  gold: "#F59E0B",
  gray: "#6B7280",
  soft: "#F4EFE5",
};

const questions = [
  ["Q1", "童年照", "这是哪位老师小时候？", "assets/q01.jpg", ["候选1", "候选2", "候选3", "候选4"], "A｜候选1", "老师起立挥手认证"],
  ["Q2", "口头禅", "这句口头禅是谁说的？", "这句话替换成老师真实口头禅", ["候选1", "候选2", "候选3", "候选4"], "B｜候选2", "老师现场原声复刻"],
  ["Q3", "水杯/物品", "这个物品属于哪位老师？", "assets/q03.jpg", ["候选1", "候选2", "候选3", "候选4"], "C｜候选3", "老师举起同款物品"],
  ["Q4", "板书/便利贴", "这张板书/便利贴属于哪位老师？", "assets/q04.jpg", ["候选1", "候选2", "候选3", "候选4"], "D｜候选4", "老师站起来认领"],
  ["Q5", "童年照", "这是哪位老师小时候？", "assets/q05.jpg", ["候选1", "候选2", "候选3", "候选4"], "A｜候选1", "老师起立挥手认证"],
  ["Q6", "口头禅", "这句口头禅是谁说的？", "这句话替换成老师真实口头禅", ["候选1", "候选2", "候选3", "候选4"], "C｜候选3", "老师现场原声复刻"],
  ["Q7", "水杯/物品", "这个物品属于哪位老师？", "assets/q07.jpg", ["候选1", "候选2", "候选3", "候选4"], "B｜候选2", "老师举起同款物品"],
  ["Q8", "板书/便利贴", "这张板书/便利贴属于哪位老师？", "assets/q08.jpg", ["候选1", "候选2", "候选3", "候选4"], "D｜候选4", "老师站起来认领"],
  ["Q9", "终极题", "终极题：四张童年照分别是哪四位老师？", "assets/q09.jpg", ["候选1", "候选2", "候选3", "候选4"], "全对得2分", "四位老师一起认证"],
];

function addShape(slide, { x, y, w, h, fill = C.white, line = C.ink, shadow = true }) {
  slide.shapes.add({
    geometry: "rect",
    position: { left: x, top: y, width: w, height: h },
    fill,
    line: { style: "solid", fill: line, width: 3 },
    shadow: shadow ? "5px 5px 0px #111111" : "shadow-none",
  });
}

function addText(slide, text, x, y, w, h, style = {}) {
  const box = slide.shapes.add({
    geometry: "textbox",
    position: { left: x, top: y, width: w, height: h },
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  box.text = text;
  box.text.style = {
    fontSize: style.fontSize || 28,
    bold: style.bold ?? true,
    color: style.color || C.ink,
    alignment: style.align || "left",
  };
  return box;
}

function addTopline(slide, label, right = "") {
  addText(slide, "老师鉴定局", 54, 36, 280, 44, { fontSize: 30, bold: true });
  addText(slide, label, 476, 36, 328, 44, { fontSize: 26, color: C.gray, align: "center" });
  addText(slide, right, 926, 36, 300, 44, { fontSize: 24, color: C.gray, align: "right" });
}

function addOption(slide, letter, text, x, y) {
  addShape(slide, { x, y, w: 482, h: 64, fill: C.white, shadow: true });
  slide.shapes.add({
    geometry: "rect",
    position: { left: x, top: y, width: 64, height: 64 },
    fill: C.ink,
    line: { style: "solid", fill: C.ink, width: 0 },
  });
  addText(slide, letter, x, y + 8, 64, 42, { fontSize: 30, color: C.white, align: "center" });
  addText(slide, text, x + 84, y + 12, 368, 38, { fontSize: 28, bold: true });
}

function addVisualPlaceholder(slide, kind, source) {
  addShape(slide, { x: 58, y: 132, w: 500, h: 466, fill: C.white, shadow: true });
  if (kind === "口头禅") {
    slide.shapes.add({
      geometry: "rect",
      position: { left: 104, top: 232, width: 408, height: 190 },
      fill: C.soft,
      line: { style: "solid", fill: C.ink, width: 3 },
    });
    addText(slide, source, 128, 270, 360, 118, { fontSize: 44, bold: true, align: "center" });
  } else {
    slide.shapes.add({
      geometry: "rect",
      position: { left: 106, top: 196, width: 402, height: 276 },
      fill: C.soft,
      line: { style: "dash", fill: C.ink, width: 4 },
    });
    addText(slide, source, 128, 282, 360, 56, { fontSize: 32, color: C.gray, align: "center" });
    addText(slide, "素材待替换", 128, 348, 360, 48, { fontSize: 30, bold: true, align: "center" });
  }
}

function addQuestionSlide(p, q, idx) {
  const [id, kind, prompt, source, options] = q;
  const slide = p.slides.add();
  slide.background.fill = C.paper;
  addTopline(slide, `${id} / ${questions.length}`, "红队 0｜蓝队 0");
  addVisualPlaceholder(slide, kind, source);
  addShape(slide, { x: 610, y: 132, w: 166, h: 52, fill: C.gold, shadow: true });
  addText(slide, kind, 630, 143, 126, 28, { fontSize: 24, bold: true, align: "center" });
  addText(slide, prompt, 610, 208, 590, 132, { fontSize: prompt.length > 17 ? 44 : 58, bold: true });
  addOption(slide, "A", options[0], 610, 384);
  addOption(slide, "B", options[1], 610, 464);
  addOption(slide, "C", options[2], 610, 544);
  addOption(slide, "D", options[3], 610, 624);
  slide.speakerNotes.textFrame.setText([
    "主持人口令：请看题。红队、蓝队，各派一位代表。",
    "操作：读完题后进入倒计时页。",
    idx === questions.length - 1 ? "终极题答对加2分。" : "常规题答对加1分。",
  ].join("\n"));
}

function addCountdownSlide(p, q) {
  const [id] = q;
  const slide = p.slides.add();
  slide.background.fill = C.ink;
  addText(slide, id, 62, 42, 180, 44, { fontSize: 30, color: C.white });
  addText(slide, "5", 0, 130, W, 310, { fontSize: 270, color: C.white, align: "center" });
  addText(slide, "准备抢话筒", 0, 486, W, 90, { fontSize: 66, color: C.gold, align: "center" });
  slide.speakerNotes.textFrame.setText("主持人口令：5、4、3、2、1。下一页喊：抢话筒。");
}

function addGrabSlide(p, q) {
  const [id] = q;
  const slide = p.slides.add();
  slide.background.fill = C.ink;
  addText(slide, id, 62, 42, 180, 44, { fontSize: 30, color: C.white });
  addText(slide, "抢话筒", 0, 202, W, 178, { fontSize: 128, color: C.gold, align: "center" });
  addText(slide, "先拿到话筒的一队先答", 0, 422, W, 64, { fontSize: 44, color: C.white, align: "center" });
  slide.speakerNotes.textFrame.setText("主持人口令：抢话筒！拿到话筒后请直接作答。作答后进入公布答案页。");
}

function addAnswerSlide(p, q) {
  const [id, kind, , , , answer, reveal] = q;
  const slide = p.slides.add();
  slide.background.fill = C.paper;
  addTopline(slide, `${id} 答案`, kind === "终极题" ? "本题2分" : "本题1分");
  addShape(slide, { x: 72, y: 142, w: 660, h: 410, fill: C.white, shadow: true });
  addText(slide, "公布答案", 116, 184, 300, 54, { fontSize: 38, color: C.gray });
  addText(slide, answer, 116, 264, 560, 112, { fontSize: answer.length > 6 ? 66 : 92, color: C.red });
  addText(slide, reveal, 116, 414, 560, 70, { fontSize: 40, color: C.ink });
  addShape(slide, { x: 790, y: 142, w: 380, h: 410, fill: C.soft, shadow: true });
  addText(slide, "请老师现场认证", 830, 286, 300, 110, { fontSize: 54, align: "center" });
  slide.speakerNotes.textFrame.setText("主持人口令：回答正确，加分。请老师现场认证一下。");
}

function addCover(p) {
  const slide = p.slides.add();
  slide.background.fill = C.paper;
  addShape(slide, { x: 64, y: 70, w: 1150, h: 520, fill: C.white, shadow: true });
  addText(slide, "老师鉴定局", 108, 146, 660, 120, { fontSize: 92 });
  addText(slide, "抢话筒答题版", 112, 286, 520, 62, { fontSize: 46, color: C.red });
  addText(slide, "两队上台｜倒计时｜抢话筒｜公布答案｜老师认证", 112, 430, 800, 54, { fontSize: 34, color: C.gray });
  addText(slide, "请音控同时播放 teacher_game_bgm.wav", 112, 510, 700, 38, { fontSize: 24, color: C.gray });
  slide.speakerNotes.textFrame.setText("本PPT可并入总表彰会PPT。BGM建议由音控单独播放。");
}

function addRules(p) {
  const slide = p.slides.add();
  slide.background.fill = C.paper;
  addTopline(slide, "游戏规则", "红队 vs 蓝队");
  addText(slide, "抽两队人马上台", 72, 132, 500, 64, { fontSize: 54 });
  const rules = [
    "每队5人，红队站左侧，蓝队站右侧",
    "每题各派1名代表站到抢答线",
    "倒计时结束后，主持人喊“抢话筒”",
    "先拿到话筒的一队先答",
    "答对加1分，答错给对方补答一次",
    "终极题答对加2分"
  ];
  rules.forEach((rule, i) => {
    const y = 224 + i * 64;
    addShape(slide, { x: 96, y, w: 34, h: 34, fill: i % 2 === 0 ? C.red : C.blue, shadow: false });
    addText(slide, rule, 152, y - 4, 940, 42, { fontSize: 32 });
  });
  slide.speakerNotes.textFrame.setText("主持人用30秒讲完规则。重点只说：倒计时结束，听到抢话筒再上前。");
}

function addTeamSlide(p) {
  const slide = p.slides.add();
  slide.background.fill = C.paper;
  addTopline(slide, "抽队上台", "每队5人");
  addText(slide, "红队", 170, 150, 300, 70, { fontSize: 62, color: C.red, align: "center" });
  addText(slide, "蓝队", 810, 150, 300, 70, { fontSize: 62, color: C.blue, align: "center" });
  addShape(slide, { x: 128, y: 250, w: 390, h: 300, fill: "#FEE2E2", line: C.red, shadow: true });
  addShape(slide, { x: 762, y: 250, w: 390, h: 300, fill: "#DBEAFE", line: C.blue, shadow: true });
  addText(slide, "1  2  3  4  5", 162, 372, 322, 62, { fontSize: 50, color: C.red, align: "center" });
  addText(slide, "1  2  3  4  5", 796, 372, 322, 62, { fontSize: 50, color: C.blue, align: "center" });
  addText(slide, "话筒放舞台中央", 0, 600, W, 54, { fontSize: 38, align: "center" });
  slide.speakerNotes.textFrame.setText("抽10名学生上台。红队站舞台左侧，蓝队站舞台右侧。话筒放中间。");
}

function addScoreSlide(p, title) {
  const slide = p.slides.add();
  slide.background.fill = C.paper;
  addTopline(slide, title, "记分员报分");
  addText(slide, "红队", 198, 176, 280, 70, { fontSize: 62, color: C.red, align: "center" });
  addText(slide, "蓝队", 802, 176, 280, 70, { fontSize: 62, color: C.blue, align: "center" });
  addShape(slide, { x: 168, y: 280, w: 340, h: 180, fill: "#FEE2E2", line: C.red, shadow: true });
  addShape(slide, { x: 772, y: 280, w: 340, h: 180, fill: "#DBEAFE", line: C.blue, shadow: true });
  addText(slide, "___ 分", 202, 336, 272, 70, { fontSize: 66, color: C.red, align: "center" });
  addText(slide, "___ 分", 806, 336, 272, 70, { fontSize: 66, color: C.blue, align: "center" });
  slide.speakerNotes.textFrame.setText("记分员把当前比分告诉主持人。");
}

function writeWav(filePath) {
  const sampleRate = 22050;
  const seconds = 75;
  const samples = sampleRate * seconds;
  const channels = 1;
  const bits = 16;
  const dataSize = samples * channels * (bits / 8);
  const buffer = Buffer.alloc(44 + dataSize);

  buffer.write("RIFF", 0);
  buffer.writeUInt32LE(36 + dataSize, 4);
  buffer.write("WAVE", 8);
  buffer.write("fmt ", 12);
  buffer.writeUInt32LE(16, 16);
  buffer.writeUInt16LE(1, 20);
  buffer.writeUInt16LE(channels, 22);
  buffer.writeUInt32LE(sampleRate, 24);
  buffer.writeUInt32LE(sampleRate * channels * bits / 8, 28);
  buffer.writeUInt16LE(channels * bits / 8, 32);
  buffer.writeUInt16LE(bits, 34);
  buffer.write("data", 36);
  buffer.writeUInt32LE(dataSize, 40);

  const notes = [196, 247, 294, 330, 294, 247, 220, 247];
  for (let i = 0; i < samples; i += 1) {
    const t = i / sampleRate;
    const step = Math.floor(t / 0.36) % notes.length;
    const note = notes[step];
    const beat = Math.floor(t / 0.36);
    const env = Math.exp(-((t % 0.36) * 5.3));
    const bassEnv = Math.exp(-((t % 0.72) * 12));
    const lead = Math.sin(2 * Math.PI * note * t) * 0.18 * env;
    const bass = Math.sin(2 * Math.PI * 98 * t) * 0.22 * bassEnv * (beat % 2 === 0 ? 1 : 0.35);
    const click = Math.sin(2 * Math.PI * 1760 * t) * 0.05 * Math.exp(-((t % 0.18) * 45));
    const sample = Math.max(-1, Math.min(1, lead + bass + click));
    buffer.writeInt16LE(Math.floor(sample * 32767), 44 + i * 2);
  }
  return fs.writeFile(filePath, buffer);
}

async function main() {
  await fs.mkdir(OUT_DIR, { recursive: true });
  await fs.mkdir(PREVIEW_DIR, { recursive: true });
  await fs.mkdir(path.dirname(AUDIO_PATH), { recursive: true });
  await writeWav(AUDIO_PATH);

  const p = Presentation.create({ slideSize: { width: W, height: H } });
  addCover(p);
  addRules(p);
  addTeamSlide(p);
  questions.forEach((q, i) => {
    addQuestionSlide(p, q, i);
    addCountdownSlide(p, q);
    addGrabSlide(p, q);
    addAnswerSlide(p, q);
    if (i === 3 || i === 7) addScoreSlide(p, i === 3 ? "中场比分" : "终极题前比分");
  });
  addScoreSlide(p, "最终比分");

  const pptx = await PresentationFile.exportPptx(p);
  await pptx.save(FINAL_PPTX);

  for (const [i, slide] of p.slides.items.entries()) {
    const stem = `slide-${String(i + 1).padStart(2, "0")}`;
    const png = await p.export({ slide, format: "png", scale: 1 });
    await fs.writeFile(path.join(PREVIEW_DIR, `${stem}.png`), new Uint8Array(await png.arrayBuffer()));
  }
  const montage = await p.export({ format: "webp", montage: true, scale: 0.45 });
  await fs.writeFile(path.join(PREVIEW_DIR, "montage.webp"), new Uint8Array(await montage.arrayBuffer()));
  console.log(JSON.stringify({ pptx: FINAL_PPTX, audio: AUDIO_PATH, slides: p.slides.items.length }, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
