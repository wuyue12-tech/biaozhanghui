from pathlib import Path
from xml.sax.saxutils import escape


OUT = Path("/Users/wuyue/Documents/自主管理学院/output/心愿便利贴_小黑分镜_v4")
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1800, 1200

SUBJECTS = {
    "语": "#ef4444",
    "数": "#2563eb",
    "英": "#16a34a",
    "科": "#d97706",
    "社": "#7c3aed",
}


def base(title, subtitle=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <style>
      .bg {{ fill:#ffffff; }}
      .title {{ font:700 46px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#111827; }}
      .sub {{ font:400 24px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#4b5563; }}
      .label {{ font:700 24px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#111827; }}
      .txt {{ font:400 20px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#374151; }}
      .small {{ font:400 16px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#4b5563; }}
      .tiny {{ font:400 13px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#4b5563; }}
      .stage {{ fill:#f8fafc; stroke:#111827; stroke-width:3.5; }}
      .front {{ stroke:#f97316; stroke-width:10; stroke-linecap:round; }}
      .seat {{ fill:#f3f4f6; stroke:#9ca3af; stroke-width:2.5; }}
      .aisle {{ fill:#ffffff; stroke:#cbd5e1; stroke-width:2.5; stroke-dasharray:10 8; }}
      .panel {{ fill:#ffffff; stroke:#111827; stroke-width:3; }}
      .orange {{ stroke:#f97316; stroke-width:5; fill:none; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#arrO); }}
      .blue {{ stroke:#2563eb; stroke-width:5; fill:none; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#arrB); }}
      .green {{ stroke:#16a34a; stroke-width:5; fill:none; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#arrG); }}
      .light {{ stroke:#94a3b8; stroke-width:2.5; fill:none; stroke-dasharray:8 8; }}
      .basket {{ fill:#fff7ed; stroke:#ea580c; stroke-width:2.5; }}
      .gift {{ fill:#fef3c7; stroke:#d97706; stroke-width:2; }}
      .tag {{ fill:#fff7ed; stroke:#fb923c; stroke-width:2.5; }}
    </style>
    <marker id="arrO" markerWidth="14" markerHeight="14" refX="11" refY="7" orient="auto"><path d="M2,2 L12,7 L2,12 Z" fill="#f97316"/></marker>
    <marker id="arrB" markerWidth="14" markerHeight="14" refX="11" refY="7" orient="auto"><path d="M2,2 L12,7 L2,12 Z" fill="#2563eb"/></marker>
    <marker id="arrG" markerWidth="14" markerHeight="14" refX="11" refY="7" orient="auto"><path d="M2,2 L12,7 L2,12 Z" fill="#16a34a"/></marker>
  </defs>
  <rect width="{W}" height="{H}" class="bg"/>
  <text x="900" y="62" text-anchor="middle" class="title">{escape(title)}</text>
  <text x="900" y="100" text-anchor="middle" class="sub">{escape(subtitle)}</text>
'''


def end():
    return "</svg>\n"


def xiaohei(x, y, label="", subject="", scale=1.0, face="left", basket=False, gift=False):
    color = SUBJECTS.get(subject, "#111827")
    body_w = 34 * scale
    body_h = 48 * scale
    eye_r = 4.3 * scale
    if face == "left":
        e1, e2 = (-8 * scale, -13 * scale), (-8 * scale, 1 * scale)
    elif face == "right":
        e1, e2 = (8 * scale, -13 * scale), (8 * scale, 1 * scale)
    elif face == "down":
        e1, e2 = (-6 * scale, -4 * scale), (6 * scale, -4 * scale)
    else:
        e1, e2 = (-6 * scale, -11 * scale), (6 * scale, -11 * scale)
    s = f'''
  <g transform="translate({x},{y})">
    <ellipse cx="0" cy="-18" rx="{body_w/2}" ry="{body_h/2}" fill="#111827"/>
    <circle cx="{e1[0]}" cy="{e1[1]-18}" r="{eye_r}" fill="#ffffff"/>
    <circle cx="{e2[0]}" cy="{e2[1]-18}" r="{eye_r}" fill="#ffffff"/>
    <line x1="-7" y1="8" x2="-13" y2="30" stroke="#111827" stroke-width="{3*scale}" stroke-linecap="round"/>
    <line x1="7" y1="8" x2="13" y2="30" stroke="#111827" stroke-width="{3*scale}" stroke-linecap="round"/>
    <circle cx="0" cy="-52" r="{12*scale}" fill="#ffffff" stroke="{color}" stroke-width="{3*scale}"/>
    <text x="0" y="{(-48)*scale}" text-anchor="middle" class="tiny" fill="{color}">{escape(label)}</text>
'''
    if basket:
        s += f'''
    <path d="M{-30*scale},{-18*scale} Q{-12*scale},{-48*scale} {6*scale},{-18*scale}" stroke="#ea580c" stroke-width="{2.2*scale}" fill="none"/>
    <rect x="{-33*scale}" y="{-18*scale}" width="{42*scale}" height="{30*scale}" rx="{7*scale}" class="basket"/>
'''
    if gift:
        s += f'<rect x="{-34*scale}" y="{-28*scale}" width="{20*scale}" height="{16*scale}" rx="{3*scale}" class="gift"/>\n'
    s += "  </g>\n"
    return s


def flower_basket(x, y, label="篮", scale=1.0):
    return f'''
  <g transform="translate({x},{y})">
    <path d="M{-30*scale},0 Q0,{-38*scale} {30*scale},0" stroke="#ea580c" stroke-width="{2.5*scale}" fill="none"/>
    <rect x="{-32*scale}" y="0" width="{64*scale}" height="{42*scale}" rx="{9*scale}" class="basket"/>
    <circle cx="{-18*scale}" cy="{3*scale}" r="{5*scale}" fill="#ef4444"/>
    <circle cx="{0}" cy="{-3*scale}" r="{5*scale}" fill="#f97316"/>
    <circle cx="{18*scale}" cy="{3*scale}" r="{5*scale}" fill="#16a34a"/>
    <text x="0" y="{30*scale}" text-anchor="middle" class="tiny">{escape(label)}</text>
  </g>'''


def stage_right(x=1260, y=170, w=390, h=760, title=True):
    s = f'''
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" class="stage"/>
  <line x1="{x}" y1="{y+30}" x2="{x}" y2="{y+h-30}" class="front"/>
'''
    if title:
        s += f'<text x="{x+w/2}" y="{y+50}" text-anchor="middle" class="label">舞台</text>\n'
        s += f'<text x="{x-82}" y="{y+h/2}" text-anchor="middle" class="txt" fill="#f97316">台口</text>\n'
    return s


def audience(x=150, y=250, w=880, h=560):
    s = f'''
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" class="seat"/>
  <text x="{x+w/2}" y="{y+45}" text-anchor="middle" class="label">观众席</text>
'''
    for row in range(6):
        yy = y + 105 + row * 66
        for col in range(11):
            xx = x + 95 + col * 66
            s += f'<circle cx="{xx}" cy="{yy}" r="12" fill="#d1d5db"/>\n'
    return s


def aisles():
    return '''
  <rect x="170" y="160" width="1040" height="68" rx="16" class="aisle"/>
  <rect x="170" y="840" width="1040" height="68" rx="16" class="aisle"/>
  <text x="700" y="205" text-anchor="middle" class="txt">上过道</text>
  <text x="700" y="883" text-anchor="middle" class="txt">下过道</text>
'''


def legend(x=90, y=1040, gap=260):
    labels = [("语文3", "语"), ("数学3", "数"), ("英语4", "英"), ("科学4", "科"), ("社政3", "社")]
    s = ""
    for i, (t, key) in enumerate(labels):
        color = SUBJECTS[key]
        xx = x + i * gap
        s += f'<circle cx="{xx}" cy="{y}" r="14" fill="#ffffff" stroke="{color}" stroke-width="4"/><text x="{xx+28}" y="{y+7}" class="txt">{t}</text>\n'
    return s


def actor_positions(offset_x=0, offset_y=0):
    # Three compact arcs on a vertical stage, all facing audience on the left.
    return [
        (1340, 720, "语1", "语"), (1405, 665, "数1", "数"), (1470, 640, "英1", "英"), (1535, 665, "科1", "科"), (1600, 720, "社1", "社"),
        (1332, 535, "语2", "语"), (1395, 490, "数2", "数"), (1460, 470, "英2", "英"), (1524, 490, "英3", "英"), (1588, 535, "科2", "科"), (1622, 590, "社2", "社"),
        (1350, 360, "语3", "语"), (1415, 325, "数3", "数"), (1480, 310, "英4", "英"), (1545, 325, "科3", "科"), (1605, 360, "科4", "科"), (1628, 430, "社3", "社"),
    ]


def page1():
    s = base("01 报告厅方向与总动线", "舞台在右侧，台口朝向左侧观众席；两条过道承接发礼路线")
    s += audience() + aisles() + stage_right()
    s += '''
  <path d="M1160 195 C1220 220,1240 260,1260 315" class="orange"/>
  <path d="M1160 875 C1220 850,1240 810,1260 755" class="orange"/>
  <path d="M1260 520 C1180 520,1125 520,1050 520" class="blue"/>
  <text x="1165" y="145" text-anchor="middle" class="small">上台入口</text>
  <text x="1165" y="942" text-anchor="middle" class="small">下台入口</text>
'''
    for x, y, label, sub in actor_positions():
        s += xiaohei(x, y, label, sub, scale=0.82, face="left")
    s += '''
  <rect x="900" y="955" width="770" height="78" rx="16" class="tag"/>
  <text x="1285" y="1005" text-anchor="middle" class="txt">台上小黑全部面向观众席；橙线是上台动线，蓝线是演唱朝向。</text>
'''
    s += legend(90, 1090, 250)
    return s + end()


def page2():
    s = base("02 舞台站位与小组唱动作", "17人采用紧凑三排弧线；唱到本组，本组向台口前半步")
    s += stage_right(x=220, y=150, w=1040, h=860, title=False)
    s += '<text x="740" y="210" text-anchor="middle" class="label">舞台：台口在左，观众席在左侧画外</text>\n'
    s += '<line x1="220" y1="180" x2="220" y2="980" class="front"/>\n'
    s += '<text x="150" y="590" text-anchor="middle" class="txt" fill="#f97316">台口</text>\n'
    # arcs
    s += '<path d="M405 780 C610 670,900 675,1100 800" class="light"/>\n'
    s += '<path d="M390 560 C615 430,940 455,1130 620" class="light"/>\n'
    s += '<path d="M445 365 C660 245,960 280,1140 470" class="light"/>\n'
    for x, y, label, sub in actor_positions():
        sx = 220 + (x - 1260) * 2.2
        sy = 150 + (y - 170) * 1.02
        s += xiaohei(sx, sy, label, sub, scale=0.95, face="left")
    # group action arrows toward front edge
    s += '''
  <path d="M595 725 C530 720,455 720,340 720" class="orange"/>
  <path d="M790 510 C700 505,570 510,360 535" class="orange"/>
  <path d="M1005 350 C875 325,655 325,380 380" class="orange"/>
  <rect x="1340" y="190" width="330" height="545" rx="20" class="panel"/>
  <text x="1370" y="240" class="label">舞台动作</text>
  <text x="1370" y="295" class="txt">前奏：两侧进入弧线。</text>
  <text x="1370" y="345" class="txt">小组唱：本组前半步。</text>
  <text x="1370" y="395" class="txt">等待组：空手轻拍。</text>
  <text x="1370" y="445" class="txt">副歌：整体小幅摆手。</text>
  <text x="1370" y="495" class="txt">尾副歌：台上保持弧线。</text>
  <rect x="1365" y="565" width="270" height="105" rx="16" class="tag"/>
  <text x="1500" y="610" text-anchor="middle" class="label">造型口令</text>
  <text x="1500" y="648" text-anchor="middle" class="txt">弧线收紧，眼睛看观众</text>
'''
    s += legend(330, 1080, 260)
    return s + end()


def page3():
    s = base("03 歌曲段落与动作分镜", "每格画动作，排练时按最终伴奏字幕微调时间点")
    panels = [
        (70, 160, "前奏", "两侧上台"),
        (470, 160, "主歌", "小组前半步"),
        (870, 160, "副歌", "全体小幅摆手"),
        (1270, 160, "副歌2尾", "取花篮"),
        (270, 650, "尾副歌", "走过道发礼"),
        (850, 650, "尾声", "回台摆造型"),
    ]
    for x, y, title, note in panels:
        s += f'<rect x="{x}" y="{y}" width="350" height="360" rx="22" class="panel"/><text x="{x+28}" y="{y+45}" class="label">{title}</text><text x="{x+28}" y="{y+82}" class="txt">{note}</text>\n'
    # panel 1
    s += stage_right(150, 275, 120, 160, title=False)
    s += xiaohei(345, 320, "语", "语", 0.65, "left") + xiaohei(375, 365, "数", "数", 0.65, "left")
    s += '<path d="M395 300 C340 295,280 300,250 335" class="orange"/>\n'
    # panel 2
    s += stage_right(540, 275, 120, 160, title=False)
    s += xiaohei(610, 340, "英", "英", 0.72, "left")
    s += '<path d="M610 340 C560 340,535 340,515 340" class="orange"/>\n'
    # panel 3
    s += stage_right(930, 275, 150, 160, title=False)
    for i, key in enumerate(["语", "数", "英", "科", "社"]):
        s += xiaohei(1015 + (i-2)*25, 370 + abs(i-2)*10, key, key, 0.55, "left")
    s += '<path d="M990 300 C1040 270,1110 295,1135 345" class="blue"/>\n'
    # panel 4
    s += stage_right(1335, 275, 130, 160, title=False)
    s += xiaohei(1420, 330, "科", "科", 0.62, "left", basket=True)
    s += flower_basket(1510, 325, "篮")
    s += '<path d="M1455 330 C1490 320,1510 320,1530 330" class="orange"/>\n'
    # panel 5
    s += audience(320, 775, 290, 170)
    s += '<rect x="640" y="760" width="55" height="215" rx="10" class="aisle"/>\n'
    s += xiaohei(665, 825, "英", "英", 0.62, "down", basket=True)
    s += xiaohei(665, 910, "数", "数", 0.62, "down", basket=True)
    s += '<path d="M665 780 C665 835,665 890,665 955" class="orange"/>\n'
    # panel 6
    s += stage_right(980, 760, 270, 220, title=False)
    for i, key in enumerate(["语", "数", "英", "科", "社"]):
        s += xiaohei(1070 + i*36, 900 - abs(i-2)*16, key, key, 0.56, "left", basket=(i in [1, 3]))
    s += '<path d="M1045 925 C1110 850,1215 850,1265 925" class="blue"/>\n'
    s += '<rect x="1330" y="740" width="330" height="260" rx="20" class="tag"/><text x="1495" y="790" text-anchor="middle" class="label">段落口令</text><text x="1495" y="845" text-anchor="middle" class="txt">前奏上台</text><text x="1495" y="895" text-anchor="middle" class="txt">副歌2取篮</text><text x="1495" y="945" text-anchor="middle" class="txt">尾声回台</text>\n'
    return s + end()


def page4():
    s = base("04 两条过道发礼路线", "人物、花篮、礼物传递全部画在路线中")
    s += audience(190, 265, 790, 520) + aisles() + stage_right(1240, 200, 360, 690)
    # On stage singers
    for x, y, label, sub in actor_positions()[:12]:
        s += xiaohei(x - 10, y + 30, label, sub, scale=0.48, face="left")
    # gift teachers on top aisle and bottom aisle
    top_route = [(1140, 195, "语", "语"), (980, 195, "数", "数"), (790, 195, "英", "英")]
    bottom_route = [(1140, 875, "科", "科"), (980, 875, "社", "社"), (790, 875, "英", "英")]
    for p in top_route:
        s += xiaohei(*p, scale=0.75, face="left", basket=True)
    for p in bottom_route:
        s += xiaohei(*p, scale=0.75, face="left", basket=True)
    s += '''
  <path d="M1240 320 C1160 260,1060 205,935 195 C820 185,700 185,555 205" class="orange"/>
  <path d="M1240 760 C1160 820,1060 875,935 875 C820 885,700 885,555 865" class="orange"/>
'''
    # gifts to row heads
    for yy in [350, 420, 490, 560, 630, 700]:
        s += f'<rect x="1000" y="{yy}" width="28" height="22" rx="4" class="gift"/><path d="M1000 {yy+10} C930 {yy+5},890 {yy+5},845 {yy+10}" class="green"/>\n'
        s += f'<rect x="540" y="{yy}" width="28" height="22" rx="4" class="gift"/><path d="M568 {yy+10} C625 {yy+5},665 {yy+5},710 {yy+10}" class="green"/>\n'
    # student helpers
    for x, y in [(585, 235), (1060, 235), (585, 835), (1060, 835), (1030, 520), (520, 520)]:
        s += xiaohei(x, y, "学", "学生", scale=0.55, face="left", gift=True)
    s += '''
  <rect x="1040" y="980" width="590" height="82" rx="16" class="tag"/>
  <text x="1335" y="1032" text-anchor="middle" class="txt">老师沿两条过道移动；学生把礼物从排头传向中间。</text>
'''
    return s + end()


def page5():
    s = base("05 Ending 造型", "五个花篮在前，十二位老师在后形成心形弧线")
    s += stage_right(260, 160, 1180, 820, title=False)
    s += '<line x1="260" y1="190" x2="260" y2="950" class="front"/><text x="205" y="565" transform="rotate(-90 205,565)" text-anchor="middle" class="txt" fill="#f97316">台口朝向观众席</text>\n'
    # heart/flower arc
    s += '<path d="M480 545 C430 330,675 270,850 430 C1030 270,1265 330,1220 545 C1175 735,960 810,850 875 C740 810,525 735,480 545" class="light"/>\n'
    back = [
        (540, 480, "语2", "语"), (610, 390, "语3", "语"), (720, 350, "数2", "数"), (820, 405, "数3", "数"),
        (900, 405, "英2", "英"), (995, 350, "英3", "英"), (1105, 390, "英4", "英"), (1175, 480, "科2", "科"),
        (1125, 620, "科3", "科"), (1000, 720, "科4", "科"), (710, 720, "社2", "社"), (585, 620, "社3", "社"),
    ]
    front = [(660, 790, "语1", "语"), (755, 835, "数1", "数"), (850, 855, "英1", "英"), (945, 835, "科1", "科"), (1040, 790, "社1", "社")]
    for p in back:
        s += xiaohei(*p, scale=0.78, face="left")
    for p in front:
        s += xiaohei(*p, scale=0.88, face="left", basket=True)
    s += '''
  <rect x="1460" y="230" width="260" height="470" rx="20" class="panel"/>
  <text x="1490" y="285" class="label">定格动作</text>
  <text x="1490" y="345" class="txt">前排五人持花篮。</text>
  <text x="1490" y="405" class="txt">后排形成心形弧线。</text>
  <text x="1490" y="465" class="txt">最后一句全体合唱。</text>
  <text x="1490" y="525" class="txt">停两拍，鞠躬。</text>
  <rect x="1478" y="585" width="210" height="74" rx="14" class="tag"/>
  <text x="1583" y="633" text-anchor="middle" class="txt">造型：心愿花</text>
'''
    s += legend(430, 1040)
    return s + end()


def write_md():
    md = """# 《心愿便利贴》小黑分镜 v4

## 核心设定

- 报告厅图按“舞台在右、观众席在左”绘制。
- 台口用橙色粗线标出，所有老师面向观众席。
- 上台、发礼、回台路线用小黑人物连续位置和箭头表达。
- 老师道具集中在花篮发礼段。
- Ending 采用“心愿花”造型：前排五个花篮，后排心形弧线。

## 五张图

1. 报告厅方向与总动线。
2. 舞台站位与小组唱动作。
3. 歌曲段落与动作分镜。
4. 两条过道发礼路线。
5. Ending 造型。
"""
    (OUT / "心愿便利贴_小黑分镜_v4_说明.md").write_text(md, encoding="utf-8")


def write_all():
    pages = [
        ("01_报告厅方向与总动线.svg", page1()),
        ("02_舞台站位与小组唱动作.svg", page2()),
        ("03_歌曲段落与动作分镜.svg", page3()),
        ("04_两条过道发礼路线.svg", page4()),
        ("05_Ending造型.svg", page5()),
    ]
    for name, content in pages:
        (OUT / name).write_text(content, encoding="utf-8")
    write_md()
    print(OUT)


if __name__ == "__main__":
    write_all()
