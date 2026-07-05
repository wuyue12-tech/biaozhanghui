from pathlib import Path
from xml.sax.saxutils import escape


OUT = Path("/Users/wuyue/Documents/自主管理学院/output/心愿便利贴_三观众席小黑分镜_v8")
OUT.mkdir(parents=True, exist_ok=True)

W, H = 2200, 1400

COL = {
    "语": "#ef4444",
    "数": "#2563eb",
    "英": "#16a34a",
    "科": "#d97706",
    "社": "#7c3aed",
    "学": "#64748b",
    "助": "#111827",
}


def e(text):
    return escape(str(text))


def svg_start(title, subtitle=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <style>
      .bg {{ fill:#fff; }}
      .title {{ font:700 46px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#111827; }}
      .sub {{ font:400 23px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#4b5563; }}
      .h1 {{ font:700 30px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#111827; }}
      .h2 {{ font:700 23px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#111827; }}
      .txt {{ font:400 20px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#374151; }}
      .small {{ font:400 16px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#4b5563; }}
      .tiny {{ font:400 13px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#4b5563; }}
      .panel {{ fill:#fff; stroke:#111827; stroke-width:3; stroke-linecap:round; stroke-linejoin:round; }}
      .stage {{ fill:#f8fafc; stroke:#111827; stroke-width:3.4; stroke-linecap:round; stroke-linejoin:round; }}
      .front {{ stroke:#f97316; stroke-width:7; stroke-linecap:round; }}
      .seat {{ fill:#f8fafc; stroke:#94a3b8; stroke-width:2.6; stroke-linecap:round; stroke-linejoin:round; }}
      .dot {{ fill:#cbd5e1; }}
      .aisle {{ fill:#fff7ed; stroke:#fb923c; stroke-width:3; stroke-dasharray:12 9; stroke-linecap:round; stroke-linejoin:round; }}
      .arc {{ fill:none; stroke:#94a3b8; stroke-width:2.6; stroke-dasharray:9 8; stroke-linecap:round; stroke-linejoin:round; }}
      .note {{ fill:#fff7ed; stroke:#fb923c; stroke-width:2.4; stroke-linecap:round; stroke-linejoin:round; }}
      .card {{ fill:#f8fafc; stroke:#cbd5e1; stroke-width:2.2; stroke-linecap:round; stroke-linejoin:round; }}
      .orange {{ stroke:#f97316; stroke-width:5.4; fill:none; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#ao); }}
      .blue {{ stroke:#2563eb; stroke-width:5; fill:none; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#ab); }}
      .green {{ stroke:#16a34a; stroke-width:4.8; fill:none; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#ag); }}
      .return {{ stroke:#2563eb; stroke-width:5; fill:none; stroke-dasharray:12 9; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#ab); }}
      .gift {{ fill:#fef3c7; stroke:#d97706; stroke-width:2; }}
      .basket {{ fill:#fff7ed; stroke:#ea580c; stroke-width:2.5; }}
    </style>
    <marker id="ao" markerWidth="16" markerHeight="16" refX="12" refY="8" orient="auto"><path d="M2,2 L14,8 L2,14 Z" fill="#f97316"/></marker>
    <marker id="ab" markerWidth="16" markerHeight="16" refX="12" refY="8" orient="auto"><path d="M2,2 L14,8 L2,14 Z" fill="#2563eb"/></marker>
    <marker id="ag" markerWidth="16" markerHeight="16" refX="12" refY="8" orient="auto"><path d="M2,2 L14,8 L2,14 Z" fill="#16a34a"/></marker>
  </defs>
  <rect width="{W}" height="{H}" class="bg"/>
  <text x="{W/2}" y="58" text-anchor="middle" class="title">{e(title)}</text>
  <text x="{W/2}" y="96" text-anchor="middle" class="sub">{e(subtitle)}</text>
'''


def svg_end():
    return "</svg>\n"


def rect(x, y, w, h, cls="panel", r=18):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" class="{cls}"/>\n'


def text(x, y, value, cls="txt", anchor="start"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{e(value)}</text>\n'


def note(x, y, w, h, lines):
    s = rect(x, y, w, h, "note", 16)
    for i, line in enumerate(lines):
        s += text(x + 35, y + 43 + i * 38, line, "txt")
    return s


def xiaohei(x, y, tag="", group="", scale=1.0, face="front", basket=False, gift=False, arms="down"):
    color = COL.get(group, "#111827")
    if face == "left":
        eyes = [(-7, -26), (-7, -12)]
    elif face == "right":
        eyes = [(7, -26), (7, -12)]
    else:
        eyes = [(-6, -20), (6, -20)]
    sw = 3 * scale
    if arms == "open":
        arms_path = f'<line x1="0" y1="{3*scale}" x2="{-25*scale}" y2="{-12*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/><line x1="0" y1="{3*scale}" x2="{25*scale}" y2="{-12*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/>\n'
    elif arms == "basket":
        arms_path = f'<line x1="0" y1="{3*scale}" x2="{-25*scale}" y2="{17*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/><line x1="0" y1="{3*scale}" x2="{25*scale}" y2="{17*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/>\n'
    else:
        arms_path = f'<line x1="0" y1="{3*scale}" x2="{-18*scale}" y2="{14*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/><line x1="0" y1="{3*scale}" x2="{18*scale}" y2="{14*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/>\n'
    s = f'''
  <g transform="translate({x},{y})">
    <ellipse cx="0" cy="-18" rx="{18*scale}" ry="{27*scale}" fill="#111827"/>
    <circle cx="{eyes[0][0]*scale}" cy="{eyes[0][1]*scale}" r="{4.4*scale}" fill="#fff"/>
    <circle cx="{eyes[1][0]*scale}" cy="{eyes[1][1]*scale}" r="{4.4*scale}" fill="#fff"/>
    {arms_path}
    <line x1="{-8*scale}" y1="{7*scale}" x2="{-16*scale}" y2="{35*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/>
    <line x1="{8*scale}" y1="{7*scale}" x2="{16*scale}" y2="{35*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/>
    <circle cx="0" cy="{-57*scale}" r="{13*scale}" fill="#fff" stroke="{color}" stroke-width="{3*scale}"/>
    <text x="0" y="{-52*scale}" text-anchor="middle" class="tiny" fill="{color}">{e(tag)}</text>
'''
    if basket:
        s += f'''
    <path d="M{-28*scale},{17*scale} Q0,{-14*scale} {28*scale},{17*scale}" stroke="#ea580c" stroke-width="{2.5*scale}" fill="none"/>
    <rect x="{-30*scale}" y="{17*scale}" width="{60*scale}" height="{38*scale}" rx="{8*scale}" class="basket"/>
'''
    if gift:
        s += f'<rect x="{19*scale}" y="{8*scale}" width="{23*scale}" height="{18*scale}" rx="{4*scale}" class="gift"/>\n'
    s += "  </g>\n"
    return s


def legend(y=122):
    items = [("语文3", "语"), ("数学3", "数"), ("英语4", "英"), ("科学4", "科"), ("社政3", "社")]
    s = ""
    start = 260
    for i, (label, key) in enumerate(items):
        x = start + i * 310
        s += xiaohei(x, y, "", key, 0.45)
        s += text(x + 35, y + 9, label, "txt")
    s += text(1770, y + 9, "共17人", "txt")
    return s


def venue(x=0, y=0, scale=1.0, labels=True, dots=True):
    def sx(v):
        return x + v * scale

    def sy(v):
        return y + v * scale

    s = ""
    s += rect(sx(470), sy(120), 1260 * scale, 160 * scale, "stage", 18)
    s += f'<line x1="{sx(515)}" y1="{sy(280)}" x2="{sx(1685)}" y2="{sy(280)}" class="front"/>\n'
    if labels:
        s += text(sx(1100), sy(176), "舞台", "h2", "middle")
        s += text(sx(1100), sy(320), "台口 / 面向观众", "small", "middle")
        s += rect(sx(1790), sy(140), 130 * scale, 80 * scale, "card", 10)
        s += text(sx(1855), sy(190), "候场门", "small", "middle")
    s += rect(sx(105), sy(500), 405 * scale, 520 * scale, "seat", 12)
    s += rect(sx(650), sy(455), 900 * scale, 610 * scale, "seat", 12)
    s += rect(sx(1690), sy(500), 405 * scale, 520 * scale, "seat", 12)
    s += rect(sx(535), sy(420), 90 * scale, 700 * scale, "aisle", 10)
    s += rect(sx(1575), sy(420), 90 * scale, 700 * scale, "aisle", 10)
    if labels:
        s += text(sx(305), sy(550), "左侧观众席", "h2", "middle")
        s += text(sx(1100), sy(505), "主观众席", "h2", "middle")
        s += text(sx(1892), sy(550), "右侧观众席", "h2", "middle")
        s += text(sx(580), sy(450), "左国道/过道", "h2", "middle")
        s += text(sx(1620), sy(450), "右国道/过道", "h2", "middle")
    if dots:
        for r in range(5):
            yy = sy(590 + r * 88)
            for c in range(4):
                s += f'<circle cx="{sx(190 + c * 75)}" cy="{yy}" r="{10*scale}" class="dot"/>\n'
                s += f'<circle cx="{sx(1775 + c * 75)}" cy="{yy}" r="{10*scale}" class="dot"/>\n'
        for r in range(6):
            yy = sy(545 + r * 80)
            for c in range(10):
                s += f'<circle cx="{sx(760 + c * 72)}" cy="{yy}" r="{10*scale}" class="dot"/>\n'
    return s


def stage_positions(sx, sy, sw, sh, scale=1.0):
    groups = [
        ("语", ["语1", "语2", "语3"], 0.16),
        ("数", ["数1", "数2", "数3"], 0.33),
        ("英", ["英1", "英2", "英3", "英4"], 0.52),
        ("科", ["科1", "科2", "科3", "科4"], 0.70),
        ("社", ["社1", "社2", "社3"], 0.86),
    ]
    points = {}
    s = ""
    for key, labels, xr in groups:
        cx = sx + sw * xr
        for i, label in enumerate(labels):
            local = i - (len(labels) - 1) / 2
            px = cx + local * 44 * scale
            if i == 0:
                py = sy + sh * 0.72
            elif i == 1:
                py = sy + sh * 0.53
            else:
                py = sy + sh * 0.34 + (i - 2) * 18 * scale
            points[label] = (px, py, key)
            s += xiaohei(px, py, label, key, 0.72 * scale)
    return s, points


def stage_board(x, y, w, h, title="舞台放大图"):
    s = rect(x, y, w, h, "stage", 18)
    s += f'<line x1="{x+45}" y1="{y+h}" x2="{x+w-45}" y2="{y+h}" class="front"/>\n'
    s += text(x + w / 2, y + 45, title, "h2", "middle")
    s += text(x + w / 2, y + h + 75, "台口 / 面向三块观众席", "h2", "middle")
    return s


def page_overview():
    s = svg_start("00 小黑电影分镜总览", "一页看懂：场地、上台、前移、发礼、回台、ending") + legend()
    px, py = 36, 165
    gap = 24
    pw = (W - px * 2 - gap * 2) / 3
    ph = 555
    titles = ["① 场地", "② 上台落位", "③ 小组前移", "④ 段落口令", "⑤ 发礼回台", "⑥ Ending"]
    for i, title in enumerate(titles):
        col, row = i % 3, i // 3
        x = px + col * (pw + gap)
        y = py + row * 620
        s += rect(x, y, pw, ph, "panel", 12)
        s += text(x + 22, y + 45, title, "h1")
        if i == 0:
            s += venue(x - 70, y + 65, 0.36, labels=True, dots=True)
        elif i == 1:
            s += rect(x + 80, y + 95, pw - 160, 205, "stage", 10)
            s += f'<line x1="{x+110}" y1="{y+300}" x2="{x+pw-110}" y2="{y+300}" class="front"/>\n'
            sp, _ = stage_positions(x + 105, y + 112, pw - 210, 160, 0.66)
            s += sp
            s += f'<path d="M{x+80} {y+380} C{x+190} {y+320},{x+275} {y+270},{x+355} {y+245}" class="orange"/>\n'
            s += f'<path d="M{x+pw-80} {y+380} C{x+pw-190} {y+320},{x+pw-275} {y+270},{x+pw-355} {y+245}" class="orange"/>\n'
            s += text(x + pw / 2, y + 430, "两侧上台，三排弧线", "txt", "middle")
        elif i == 2:
            s += rect(x + 80, y + 105, pw - 160, 230, "stage", 10)
            s += f'<line x1="{x+110}" y1="{y+335}" x2="{x+pw-110}" y2="{y+335}" class="front"/>\n'
            s += f'<path d="M{x+130} {y+282} C{x+280} {y+220},{x+pw-280} {y+220},{x+pw-130} {y+282}" class="arc"/>\n'
            for j, key in enumerate(["语", "数", "英", "科", "社"]):
                xx = x + 150 + j * 118
                s += xiaohei(xx, y + 286, key, key, 0.58, arms="open")
                s += f'<path d="M{xx} {y+260} C{xx} {y+225},{xx+12} {y+190},{xx+40} {y+160}" class="orange"/>\n'
            s += text(x + pw / 2, y + 425, "唱到本组，代表到前移线", "txt", "middle")
        elif i == 3:
            rows = [("L1-L2", "语文"), ("L3-L4", "数学"), ("L5-L7", "英语"), ("L8-L10", "科学"), ("L11-L12", "社政"), ("副歌", "全体")]
            for r, (a, b) in enumerate(rows):
                yy = y + 90 + r * 60
                s += rect(x + 55, yy, pw - 110, 48, "card", 9)
                s += text(x + 85, yy + 31, a, "txt")
                s += text(x + 285, yy + 31, b, "txt")
        elif i == 4:
            s += venue(x - 70, y + 75, 0.36, labels=False, dots=False)
            s += f'<path d="M{x+210} {y+210} C{x+175} {y+315},{x+170} {y+420},{x+205} {y+505}" class="orange"/>\n'
            s += f'<path d="M{x+515} {y+210} C{x+550} {y+315},{x+555} {y+420},{x+520} {y+505}" class="orange"/>\n'
            s += f'<path d="M{x+365} {y+215} C{x+365} {y+305},{x+365} {y+390},{x+365} {y+500}" class="green"/>\n'
            s += f'<path d="M{x+205} {y+505} C{x+185} {y+400},{x+180} {y+310},{x+250} {y+215}" class="return"/>\n'
            s += f'<path d="M{x+520} {y+505} C{x+540} {y+400},{x+545} {y+310},{x+475} {y+215}" class="return"/>\n'
            s += text(x + pw / 2, y + 520, "橙线发礼，蓝虚线回台", "txt", "middle")
        else:
            s += rect(x + 95, y + 92, pw - 190, 360, "stage", 10)
            s += f'<line x1="{x+130}" y1="{y+452}" x2="{x+pw-130}" y2="{y+452}" class="front"/>\n'
            heart = f'M{x+265} {y+300} C{x+245} {y+190},{x+365} {y+170},{x+430} {y+250} C{x+495} {y+170},{x+620} {y+190},{x+595} {y+300} C{x+575} {y+390},{x+490} {y+420},{x+430} {y+455} C{x+370} {y+420},{x+285} {y+390},{x+265} {y+300}'
            s += f'<path d="{heart}" class="arc"/>\n'
            for j, key in enumerate(["语", "数", "英", "科", "社"]):
                s += xiaohei(x + 315 + j * 58, y + 414, key, key, 0.48, basket=True)
            for j, key in enumerate(["语", "数", "英", "科", "社", "英", "科"]):
                s += xiaohei(x + 290 + j * 58, y + 285 - abs(j - 3) * 17, "", key, 0.42, arms="open")
            s += text(x + pw / 2, y + 520, "五篮在前，后排心形", "txt", "middle")
    return s + svg_end()


def page_venue():
    s = svg_start("01 场地总览", "三块观众席：左侧、主观众席、右侧；主侧之间两条国道/过道") + legend()
    s += venue(0, 45, 1.0, labels=True, dots=True)
    s += '<path d="M580 330 C560 385,560 445,580 515" class="orange"/>\n'
    s += '<path d="M1620 330 C1640 385,1640 445,1620 515" class="orange"/>\n'
    s += '<path d="M1100 330 C1100 395,1100 455,1100 525" class="blue"/>\n'
    s += note(120, 1270, 1960, 80, ["看图口诀：舞台在前，台口朝三块观众席；两条国道/过道夹在主观众席和两侧观众席之间。"])
    return s + svg_end()


def page_stage():
    s = svg_start("02 上台动线与站位", "语数英从左侧上台；科社从右侧上台；17人落三排弧线") + legend()
    x, y, w, h = 170, 175, 1860, 700
    s += stage_board(x, y, w, h)
    s += f'<path d="M{x+220} {y+540} C{x+560} {y+430},{x+1300} {y+430},{x+1640} {y+540}" class="arc"/>\n'
    s += f'<path d="M{x+250} {y+400} C{x+620} {y+285},{x+1240} {y+285},{x+1610} {y+400}" class="arc"/>\n'
    s += f'<path d="M{x+300} {y+260} C{x+670} {y+170},{x+1190} {y+170},{x+1560} {y+260}" class="arc"/>\n'
    sp, _ = stage_positions(x + 160, y + 95, w - 320, h - 180, 1.18)
    s += sp
    s += f'<path d="M{x+35} {y+h-20} C{x+145} {y+h-95},{x+215} {y+h-175},{x+335} {y+h-230}" class="orange"/>\n'
    s += f'<path d="M{x+w-35} {y+h-20} C{x+w-145} {y+h-95},{x+w-215} {y+h-175},{x+w-335} {y+h-230}" class="orange"/>\n'
    s += text(x + 80, y + h - 35, "左侧上台：语 数 英", "txt")
    s += text(x + w - 80, y + h - 35, "右侧上台：科 社", "txt", "end")
    s += note(170, 990, 1860, 120, ["站位：三排弧线面向台下三块观众席；前排五人是后续下台发礼代表。", "舞台监督只需看五个前排点：语1、数1、英1、科1、社1。"])
    return s + svg_end()


def page_forward():
    s = svg_start("03 小组前移动作", "唱到本组时，本组代表从弧线走到前移线；唱完回弧线") + legend()
    x, y, w, h = 170, 175, 1860, 700
    s += stage_board(x, y, w, h)
    sp, pts = stage_positions(x + 160, y + 95, w - 320, h - 180, 1.15)
    s += sp
    fy = y + h - 100
    s += f'<path d="M{x+260} {fy} C{x+640} {fy-60},{x+1220} {fy-60},{x+1600} {fy}" class="arc"/>\n'
    s += text(x + w / 2, fy - 82, "前移线：唱到本组，站到这里", "h2", "middle")
    front = {
        "语": (x + 430, fy),
        "数": (x + 715, fy - 38),
        "英": (x + 940, fy - 55),
        "科": (x + 1215, fy - 38),
        "社": (x + 1490, fy),
    }
    for label, key, card in [("语1", "语", "L1-L2"), ("数1", "数", "L3-L4"), ("英1", "英", "L5-L7"), ("科1", "科", "L8-L10"), ("社1", "社", "L11-L12")]:
        x1, y1, _ = pts[label]
        x2, y2 = front[key]
        s += f'<path d="M{x1} {y1+8} C{(x1+x2)/2} {y1+95},{(x1+x2)/2} {y2-85},{x2} {y2}" class="orange"/>\n'
        s += xiaohei(x2, y2, label, key, 0.78, arms="open")
        s += text(x2, y2 + 68, card, "small", "middle")
    s += note(170, 990, 1860, 120, ["动作口令：本组前移，组员原位轻拍或摆手；唱完归回弧线。", "不要整组大幅移动，保持弧线稳定，避免后面发礼动线混乱。"])
    return s + svg_end()


def page_segments():
    s = svg_start("04 歌曲段落分镜", "按伴奏字幕编号执行；每个段落都有一个明确动作") + legend()
    panels = [
        (80, 175, "前奏", "两侧上台"),
        (470, 175, "主歌1", "五组前移轮唱"),
        (860, 175, "副歌1", "全体摆手"),
        (1250, 175, "副歌2", "五人取篮"),
        (360, 675, "尾副歌", "下台发礼"),
        (970, 675, "尾声", "回台定格"),
    ]
    for x, y, title, desc in panels:
        s += rect(x, y, 330, 350, "panel", 16)
        s += text(x + 28, y + 45, title, "h1")
        s += text(x + 28, y + 82, desc, "txt")
    s += rect(160, 305, 135, 130, "stage", 12)
    s += f'<line x1="175" y1="435" x2="280" y2="435" class="front"/>\n'
    s += xiaohei(330, 360, "语", "语", 0.62)
    s += xiaohei(370, 390, "数", "数", 0.62)
    s += '<path d="M400 345 C350 345,310 360,270 392" class="orange"/>\n'
    s += rect(550, 305, 135, 130, "stage", 12)
    s += f'<line x1="565" y1="435" x2="670" y2="435" class="front"/>\n'
    for i, key in enumerate(["语", "数", "英", "科", "社"]):
        s += xiaohei(590 + i * 42, 400 - abs(i - 2) * 14, key, key, 0.48, arms="open")
    s += '<path d="M625 405 C620 370,635 340,665 325" class="orange"/>\n'
    s += rect(940, 305, 155, 130, "stage", 12)
    s += f'<line x1="955" y1="435" x2="1080" y2="435" class="front"/>\n'
    for i, key in enumerate(["语", "数", "英", "科", "社"]):
        s += xiaohei(980 + i * 30, 390 - abs(i - 2) * 8, key, key, 0.45, arms="open")
    s += '<path d="M965 335 C1025 295,1110 320,1140 375" class="blue"/>\n'
    s += rect(1330, 305, 135, 130, "stage", 12)
    s += f'<line x1="1345" y1="435" x2="1450" y2="435" class="front"/>\n'
    s += xiaohei(1410, 375, "科", "科", 0.62, basket=True, arms="basket")
    s += xiaohei(1515, 375, "篮", "助", 0.48, basket=True, arms="basket")
    s += '<path d="M1440 375 C1470 365,1490 365,1515 375" class="orange"/>\n'
    s += venue(340, 780, 0.30, labels=False, dots=False)
    s += '<path d="M520 875 C490 945,490 1005,520 1075" class="orange"/>\n'
    s += '<path d="M805 875 C840 945,840 1005,805 1075" class="orange"/>\n'
    s += rect(1070, 780, 370, 220, "stage", 12)
    s += f'<line x1="1090" y1="1000" x2="1420" y2="1000" class="front"/>\n'
    for i, key in enumerate(["语", "数", "英", "科", "社"]):
        s += xiaohei(1160 + i * 58, 930 - abs(i - 2) * 16, key, key, 0.52, basket=(i in [0, 2, 4]))
    s += '<path d="M1135 960 C1210 880,1330 880,1410 960" class="arc"/>\n'
    s += note(1590, 700, 420, 300, ["段落口令", "前奏：上台", "主歌：前移", "副歌：摆手", "尾副歌：发礼", "尾声：回台定格"])
    return s + svg_end()


def page_gift():
    s = svg_start("05 发礼物动线与回台路线", "橙线下台发礼，绿色向座位内传，蓝色虚线回台") + legend()
    s += venue(0, 45, 1.0, labels=True, dots=True)
    starts = {
        "语1": (720, 335, "语"),
        "数1": (900, 335, "数"),
        "英1": (1100, 335, "英"),
        "科1": (1300, 335, "科"),
        "社1": (1480, 335, "社"),
    }
    for label, (x, y, key) in starts.items():
        s += xiaohei(x, y, label, key, 0.64, basket=True, arms="basket")
    s += '<path d="M720 365 C625 445,575 560,570 725 C565 875,505 960,330 1010" class="orange"/>\n'
    s += '<path d="M900 365 C760 480,620 620,590 790 C570 920,690 1015,805 1045" class="orange"/>\n'
    s += '<path d="M1100 365 C1100 445,1100 520,1100 625" class="green"/>\n'
    s += '<path d="M1300 365 C1440 480,1580 620,1610 790 C1630 920,1510 1015,1395 1045" class="orange"/>\n'
    s += '<path d="M1480 365 C1575 445,1625 560,1630 725 C1635 875,1695 960,1870 1010" class="orange"/>\n'
    s += '<path d="M330 1005 C500 920,535 790,548 635 C560 490,620 400,700 340" class="return"/>\n'
    s += '<path d="M805 1045 C700 965,620 885,615 755 C610 580,740 440,880 340" class="return"/>\n'
    s += '<path d="M1100 625 C1100 525,1100 430,1100 340" class="return"/>\n'
    s += '<path d="M1395 1045 C1500 965,1580 885,1585 755 C1590 580,1460 440,1320 340" class="return"/>\n'
    s += '<path d="M1870 1005 C1700 920,1665 790,1652 635 C1640 490,1580 400,1500 340" class="return"/>\n'
    for yy in [585, 720, 855, 990]:
        s += f'<rect x="505" y="{yy}" width="34" height="24" rx="5" class="gift"/>\n'
        s += f'<path d="M539 {yy+12} C600 {yy-5},650 {yy-5},715 {yy+12}" class="green"/>\n'
        s += f'<rect x="645" y="{yy}" width="34" height="24" rx="5" class="gift"/>\n'
        s += f'<path d="M679 {yy+12} C780 {yy-6},900 {yy-6},1035 {yy+12}" class="green"/>\n'
        s += f'<rect x="1525" y="{yy}" width="34" height="24" rx="5" class="gift"/>\n'
        s += f'<path d="M1525 {yy+12} C1420 {yy-6},1300 {yy-6},1165 {yy+12}" class="green"/>\n'
        s += f'<rect x="1662" y="{yy}" width="34" height="24" rx="5" class="gift"/>\n'
        s += f'<path d="M1662 {yy+12} C1605 {yy-5},1552 {yy-5},1495 {yy+12}" class="green"/>\n'
    for x, y in [(545, 555), (545, 825), (1048, 595), (1605, 555), (1605, 825), (1850, 900), (350, 900)]:
        s += xiaohei(x, y, "助", "助", 0.52, gift=True)
    s += note(115, 1195, 1970, 115, [
        "分配：语1给左侧观众席；数1给主观众席左半；英1走中线；科1给主观众席右半；社1给右侧观众席。",
        "回台：尾声口令后，五人按蓝色虚线回到台口前排，直接接 Ending Pose。",
    ])
    return s + svg_end()


def page_ending():
    s = svg_start("06 Ending Pose：心愿花", "五个花篮在台口前排，十二位老师在后方形成心形花瓣") + legend()
    x, y, w, h = 260, 165, 1680, 790
    s += stage_board(x, y, w, h)
    heart = (
        f"M{x+430} {y+450} C{x+370} {y+235},{x+650} {y+185},{x+835} {y+365} "
        f"C{x+1030} {y+185},{x+1310} {y+235},{x+1250} {y+450} "
        f"C{x+1210} {y+610},{x+960} {y+680},{x+840} {y+735} "
        f"C{x+720} {y+680},{x+470} {y+610},{x+430} {y+450}"
    )
    s += f'<path d="{heart}" class="arc"/>\n'
    back = [
        ("语2", "语", x + 515, y + 485), ("语3", "语", x + 565, y + 345),
        ("数2", "数", x + 735, y + 295), ("数3", "数", x + 810, y + 410),
        ("英2", "英", x + 910, y + 410), ("英3", "英", x + 985, y + 295),
        ("英4", "英", x + 1135, y + 345), ("科2", "科", x + 1185, y + 485),
        ("科3", "科", x + 1115, y + 615), ("科4", "科", x + 980, y + 690),
        ("社2", "社", x + 700, y + 690), ("社3", "社", x + 565, y + 615),
    ]
    front = [
        ("语1", "语", x + 620, y + 725),
        ("数1", "数", x + 730, y + 770),
        ("英1", "英", x + 840, y + 790),
        ("科1", "科", x + 950, y + 770),
        ("社1", "社", x + 1060, y + 725),
    ]
    for label, key, xx, yy in back:
        s += xiaohei(xx, yy, label, key, 0.76, arms="open")
    for label, key, xx, yy in front:
        s += xiaohei(xx, yy, label, key, 0.84, basket=True, arms="basket")
    s += note(260, 1070, 1680, 125, [
        "回台后：五位发礼老师带花篮站台口前排；其他十二位从左右向中间收成心形花瓣。",
        "定格口令：前排五篮，后排花瓣，全体微笑合唱，停两拍鞠躬退场。",
    ])
    return s + svg_end()


def write_all():
    pages = [
        ("00_小黑电影分镜总览.svg", page_overview()),
        ("01_场地总览.svg", page_venue()),
        ("02_上台动线与站位.svg", page_stage()),
        ("03_小组前移动作.svg", page_forward()),
        ("04_歌曲段落分镜.svg", page_segments()),
        ("05_发礼物动线与回台路线.svg", page_gift()),
        ("06_EndingPose_心愿花.svg", page_ending()),
    ]
    for name, body in pages:
        (OUT / name).write_text(body, encoding="utf-8")
    md = """# 《心愿便利贴》三观众席小黑简笔分镜 v8

## 图纸顺序

1. 小黑电影分镜总览
2. 场地总览
3. 上台动线与站位
4. 小组前移动作
5. 歌曲段落分镜
6. 发礼物动线与回台路线
7. Ending Pose：心愿花

## 关键执行点

- 台下是左侧观众席、主观众席、右侧观众席。
- 主观众席与两侧观众席之间各有一条国道/过道。
- 语文、数学、英语从左侧上台；科学、社政从右侧上台。
- 前排五人：语1、数1、英1、科1、社1，是发礼物代表。
- 发礼物：橙线下台，绿色向座位内传，蓝色虚线回台。
- Ending：五篮在台口前排，十二位老师在后方组成心形花瓣。
"""
    (OUT / "心愿便利贴_三观众席小黑分镜_v8_说明.md").write_text(md, encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    write_all()
