from pathlib import Path
from xml.sax.saxutils import escape


OUT = Path("/Users/wuyue/Documents/自主管理学院/output/心愿便利贴_三观众席简笔分镜_v7")
OUT.mkdir(parents=True, exist_ok=True)

W, H = 2200, 1400

COLORS = {
    "语": "#dc2626",
    "数": "#2563eb",
    "英": "#16a34a",
    "科": "#d97706",
    "社": "#7c3aed",
    "学": "#475569",
    "助": "#0f172a",
}


def e(text):
    return escape(str(text))


def svg_start(title, subtitle=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <style>
      .bg {{ fill:#fff; }}
      .title {{ font:700 44px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#111827; }}
      .sub {{ font:400 22px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#4b5563; }}
      .h1 {{ font:700 28px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#111827; }}
      .h2 {{ font:700 22px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#111827; }}
      .txt {{ font:400 19px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#374151; }}
      .small {{ font:400 16px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#4b5563; }}
      .tiny {{ font:400 13px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#4b5563; }}
      .paper {{ fill:#fff; stroke:#111827; stroke-width:3.2; stroke-linecap:round; stroke-linejoin:round; }}
      .soft {{ fill:#fff; stroke:#9ca3af; stroke-width:2.2; stroke-linecap:round; stroke-linejoin:round; }}
      .dash {{ fill:none; stroke:#94a3b8; stroke-width:2.4; stroke-dasharray:8 8; stroke-linecap:round; stroke-linejoin:round; }}
      .stage {{ fill:#f8fafc; stroke:#111827; stroke-width:3.4; stroke-linecap:round; stroke-linejoin:round; }}
      .stageFront {{ stroke:#f97316; stroke-width:6; stroke-linecap:round; }}
      .seatBlock {{ fill:#f8fafc; stroke:#94a3b8; stroke-width:2.6; stroke-linecap:round; stroke-linejoin:round; }}
      .seatDot {{ fill:#cbd5e1; }}
      .aisle {{ fill:#fff7ed; stroke:#fb923c; stroke-width:3; stroke-dasharray:12 9; stroke-linecap:round; stroke-linejoin:round; }}
      .note {{ fill:#fff7ed; stroke:#fb923c; stroke-width:2.5; stroke-linecap:round; stroke-linejoin:round; }}
      .lyrics {{ fill:#f8fafc; stroke:#cbd5e1; stroke-width:2.2; stroke-linecap:round; stroke-linejoin:round; }}
      .arrowO {{ fill:none; stroke:#f97316; stroke-width:5; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#arrO); }}
      .arrowB {{ fill:none; stroke:#2563eb; stroke-width:4.7; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#arrB); }}
      .arrowG {{ fill:none; stroke:#16a34a; stroke-width:4.4; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#arrG); }}
      .arrowP {{ fill:none; stroke:#7c3aed; stroke-width:4.4; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#arrP); }}
      .arrowR {{ fill:none; stroke:#dc2626; stroke-width:4.4; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#arrR); }}
      .return {{ fill:none; stroke:#2563eb; stroke-width:4.6; stroke-dasharray:12 8; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#arrB); }}
    </style>
    <marker id="arrO" markerWidth="16" markerHeight="16" refX="12" refY="8" orient="auto"><path d="M2,2 L14,8 L2,14 Z" fill="#f97316"/></marker>
    <marker id="arrB" markerWidth="16" markerHeight="16" refX="12" refY="8" orient="auto"><path d="M2,2 L14,8 L2,14 Z" fill="#2563eb"/></marker>
    <marker id="arrG" markerWidth="16" markerHeight="16" refX="12" refY="8" orient="auto"><path d="M2,2 L14,8 L2,14 Z" fill="#16a34a"/></marker>
    <marker id="arrP" markerWidth="16" markerHeight="16" refX="12" refY="8" orient="auto"><path d="M2,2 L14,8 L2,14 Z" fill="#7c3aed"/></marker>
    <marker id="arrR" markerWidth="16" markerHeight="16" refX="12" refY="8" orient="auto"><path d="M2,2 L14,8 L2,14 Z" fill="#dc2626"/></marker>
  </defs>
  <rect width="{W}" height="{H}" class="bg"/>
  <text x="{W/2}" y="56" text-anchor="middle" class="title">{e(title)}</text>
  <text x="{W/2}" y="92" text-anchor="middle" class="sub">{e(subtitle)}</text>
'''


def svg_end():
    return "</svg>\n"


def hand_rect(x, y, w, h, cls="paper", label=None):
    d = (
        f"M{x+4},{y+2} "
        f"C{x+w*0.28},{y-4} {x+w*0.62},{y+3} {x+w-5},{y+1} "
        f"L{x+w+2},{y+h-3} "
        f"C{x+w*0.65},{y+h+4} {x+w*0.25},{y+h-2} {x+1},{y+h+1} "
        f"L{x+3},{y+4} Z"
    )
    s = f'<path d="{d}" class="{cls}"/>\n'
    if label:
        s += f'<text x="{x+w/2}" y="{y+36}" text-anchor="middle" class="h2">{e(label)}</text>\n'
    return s


def line_text(x, y, text, cls="txt", anchor="start"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{e(text)}</text>\n'


def multiline(x, y, lines, cls="txt", gap=34, anchor="start"):
    return "".join(line_text(x, y + i * gap, t, cls, anchor) for i, t in enumerate(lines))


def stick(x, y, key, label="", scale=1.0, arms="down", basket=False, gift=False, face="front"):
    c = COLORS.get(key, "#111827")
    sw = 3.0 * scale
    head_r = 13 * scale
    body = 42 * scale
    leg = 28 * scale
    if arms == "sing":
        arms_path = f'<line x1="0" y1="{8*scale}" x2="{-28*scale}" y2="{-12*scale}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/><line x1="0" y1="{8*scale}" x2="{28*scale}" y2="{-12*scale}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/>\n'
    elif arms == "wave":
        arms_path = f'<line x1="0" y1="{8*scale}" x2="{-24*scale}" y2="{-8*scale}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/><line x1="0" y1="{8*scale}" x2="{24*scale}" y2="{-20*scale}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/>\n'
    elif arms == "basket":
        arms_path = f'<line x1="0" y1="{8*scale}" x2="{-26*scale}" y2="{20*scale}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/><line x1="0" y1="{8*scale}" x2="{26*scale}" y2="{20*scale}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/>\n'
    else:
        arms_path = f'<line x1="0" y1="{8*scale}" x2="{-20*scale}" y2="{16*scale}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/><line x1="0" y1="{8*scale}" x2="{20*scale}" y2="{16*scale}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/>\n'
    if face == "left":
        eyes = [(-5, -24), (-5, -14)]
    elif face == "right":
        eyes = [(5, -24), (5, -14)]
    else:
        eyes = [(-5, -20), (5, -20)]
    s = f'''
  <g transform="translate({x},{y})">
    <ellipse cx="0" cy="-18" rx="{17*scale}" ry="{25*scale}" fill="#111827"/>
    <circle cx="{eyes[0][0]*scale}" cy="{eyes[0][1]*scale}" r="{4*scale}" fill="#fff"/>
    <circle cx="{eyes[1][0]*scale}" cy="{eyes[1][1]*scale}" r="{4*scale}" fill="#fff"/>
    <line x1="0" y1="{-8*scale}" x2="0" y2="{body*0.62}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/>
    {arms_path}
    <line x1="0" y1="{body*0.62}" x2="{-leg*0.62}" y2="{body}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/>
    <line x1="0" y1="{body*0.62}" x2="{leg*0.62}" y2="{body}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/>
    <circle cx="0" cy="{-54*scale}" r="{head_r}" fill="#fff" stroke="{c}" stroke-width="{sw}"/>
    <text x="0" y="{-50*scale}" text-anchor="middle" class="tiny" fill="{c}">{e(label)}</text>
'''
    if basket:
        s += f'''
    <path d="M{-25*scale},{18*scale} Q0,{-9*scale} {25*scale},{18*scale}" fill="none" stroke="#ea580c" stroke-width="{2.5*scale}" stroke-linecap="round"/>
    <rect x="{-27*scale}" y="{18*scale}" width="{54*scale}" height="{35*scale}" rx="{7*scale}" fill="#fff7ed" stroke="#ea580c" stroke-width="{2.5*scale}"/>
'''
    if gift:
        s += f'<rect x="{18*scale}" y="{10*scale}" width="{22*scale}" height="{17*scale}" rx="{3*scale}" fill="#fef08a" stroke="#ca8a04" stroke-width="{2*scale}"/>\n'
    s += "  </g>\n"
    return s


def group_legend(x=290, y=108):
    items = [("语文3人", "语"), ("数学3人", "数"), ("英语4人", "英"), ("科学4人", "科"), ("社政3人", "社")]
    s = ""
    for i, (label, key) in enumerate(items):
        xx = x + i * 300
        s += stick(xx, y + 18, key, "", 0.48)
        s += f'<text x="{xx+28}" y="{y+25}" class="txt">{e(label)}</text>\n'
    s += f'<text x="{x + 1500}" y="{y+25}" class="txt">共17人</text>\n'
    return s


def venue(x=0, y=0, scale=1.0, labels=True, seats=True, tiny=False):
    def sx(v):
        return x + v * scale

    def sy(v):
        return y + v * scale

    label_cls = "small" if tiny else "h2"
    s = ""
    s += hand_rect(sx(520), sy(120), 1160 * scale, 150 * scale, "stage", "舞台" if labels else None)
    s += f'<line x1="{sx(560)}" y1="{sy(270)}" x2="{sx(1640)}" y2="{sy(270)}" class="stageFront"/>\n'
    if labels:
        s += line_text(sx(1100), sy(305), "台口 / 面向观众", "small", "middle")
        s += hand_rect(sx(1735), sy(135), 135 * scale, 86 * scale, "soft", "候场门")
    # Audience blocks: left side, main, right side.
    s += hand_rect(sx(120), sy(470), 390 * scale, 560 * scale, "seatBlock", "左侧观众席" if labels else None)
    s += hand_rect(sx(650), sy(430), 900 * scale, 640 * scale, "seatBlock", "主观众席" if labels else None)
    s += hand_rect(sx(1690), sy(470), 390 * scale, 560 * scale, "seatBlock", "右侧观众席" if labels else None)
    s += hand_rect(sx(535), sy(410), 90 * scale, 720 * scale, "aisle", "左国道/过道" if labels else None)
    s += hand_rect(sx(1575), sy(410), 90 * scale, 720 * scale, "aisle", "右国道/过道" if labels else None)
    if labels:
        s += line_text(sx(580), sy(1160), "主-侧之间通道", "small", "middle")
        s += line_text(sx(1620), sy(1160), "主-侧之间通道", "small", "middle")
    if seats:
        for row in range(5):
            yy = sy(555 + row * 92)
            for col in range(4):
                s += f'<circle cx="{sx(205 + col * 72)}" cy="{yy}" r="{10*scale}" class="seatDot"/>\n'
                s += f'<circle cx="{sx(1795 + col * 72)}" cy="{yy}" r="{10*scale}" class="seatDot"/>\n'
        for row in range(6):
            yy = sy(535 + row * 82)
            for col in range(10):
                s += f'<circle cx="{sx(760 + col * 72)}" cy="{yy}" r="{10*scale}" class="seatDot"/>\n'
    if labels and not tiny:
        s += hand_rect(sx(120), sy(1185), 1960 * scale, 88 * scale, "note")
        s += line_text(sx(160), sy(1238), "场地口诀：舞台在前，台口朝三块观众席；左、右两条国道/过道夹在主观众席和侧观众席之间。", "txt")
    return s


def stage_people(stage_x, stage_y, stage_w, stage_h, scale=1.0, front_extra=0):
    groups = [
        ("语", ["语1", "语2", "语3"], 0.16),
        ("数", ["数1", "数2", "数3"], 0.33),
        ("英", ["英1", "英2", "英3", "英4"], 0.52),
        ("科", ["科1", "科2", "科3", "科4"], 0.70),
        ("社", ["社1", "社2", "社3"], 0.86),
    ]
    s = ""
    points = {}
    for key, labels, cxr in groups:
        cx = stage_x + stage_w * cxr
        for i, label in enumerate(labels):
            local = i - (len(labels) - 1) / 2
            px = cx + local * 44 * scale
            if i == 0:
                py = stage_y + stage_h * 0.72 + front_extra
            elif i == 1:
                py = stage_y + stage_h * 0.53
            else:
                py = stage_y + stage_h * 0.34 + (i - 2) * 20 * scale
            points[label] = (px, py)
            s += stick(px, py, key, label, 0.70 * scale, "down", face="front")
    return s, points


def page_overview():
    s = svg_start("00 电影分镜总览：一页看懂全流程", "三块观众席 + 两条国道/过道｜橙线行动，蓝线回台，绿线传礼") + group_legend(260, 108)
    margin_x, gap_x = 36, 24
    panel_w = (W - 2 * margin_x - 2 * gap_x) / 3
    panel_h = 555
    y1, y2 = 165, 785
    titles = ["① 场地总览", "② 上台落位", "③ 小组前移", "④ 歌词动作", "⑤ 发礼回台", "⑥ Ending Pose"]
    for idx, title in enumerate(titles):
        row = 0 if idx < 3 else 1
        col = idx % 3
        x = margin_x + col * (panel_w + gap_x)
        y = y1 if row == 0 else y2
        s += hand_rect(x, y, panel_w, panel_h, "paper")
        s += line_text(x + 24, y + 42, title, "h1")
        if idx == 0:
            s += venue(x - 36, y + 62, 0.33, labels=True, seats=True, tiny=True)
        elif idx == 1:
            s += hand_rect(x + 70, y + 90, panel_w - 140, 215, "stage", "舞台")
            s += f'<line x1="{x+105}" y1="{y+305}" x2="{x+panel_w-105}" y2="{y+305}" class="stageFront"/>\n'
            sp, _ = stage_people(x + 90, y + 105, panel_w - 180, 170, 0.68)
            s += sp
            s += f'<path d="M{x+75} {y+360} C{x+205} {y+300}, {x+290} {y+260}, {x+375} {y+230}" class="arrowO"/>\n'
            s += f'<path d="M{x+panel_w-75} {y+360} C{x+panel_w-205} {y+300}, {x+panel_w-290} {y+260}, {x+panel_w-375} {y+230}" class="arrowO"/>\n'
            s += line_text(x + panel_w / 2, y + 410, "两侧上台，三排弧线", "txt", "middle")
        elif idx == 2:
            s += hand_rect(x + 70, y + 96, panel_w - 140, 240, "stage", "舞台")
            s += f'<line x1="{x+110}" y1="{y+336}" x2="{x+panel_w-110}" y2="{y+336}" class="stageFront"/>\n'
            s += f'<path d="M{x+130} {y+285} C{x+270} {y+230}, {x+panel_w-270} {y+230}, {x+panel_w-130} {y+285}" class="dash"/>\n'
            for i, (key, label) in enumerate([("语", "语"), ("数", "数"), ("英", "英"), ("科", "科"), ("社", "社")]):
                px = x + 150 + i * 118
                s += stick(px, y + 270, key, label, 0.58, "sing")
                s += f'<path d="M{px} {y+255} C{px-10} {y+225}, {px-4} {y+200}, {px+18} {y+178}" class="arrowO"/>\n'
            s += line_text(x + panel_w / 2, y + 405, "唱到本组，到前移线", "txt", "middle")
        elif idx == 3:
            rows = [("L1-L2", "语文前移"), ("L3-L4", "数学前移"), ("L5-L7", "英语前移"), ("L8-L10", "科学前移"), ("L11-L12", "社政前移"), ("副歌", "全体摆手")]
            for r, (a, b) in enumerate(rows):
                yy = y + 90 + r * 60
                s += f'<rect x="{x+55}" y="{yy}" width="{panel_w-110}" height="48" rx="10" class="lyrics"/>\n'
                s += line_text(x + 82, yy + 31, a, "txt")
                s += line_text(x + 260, yy + 31, b, "txt")
        elif idx == 4:
            s += venue(x - 45, y + 40, 0.34, labels=False, seats=False)
            s += line_text(x + panel_w / 2, y + 118, "舞台", "h2", "middle")
            s += f'<path d="M{x+225} {y+215} C{x+170} {y+285}, {x+165} {y+395}, {x+188} {y+500}" class="arrowO"/>\n'
            s += f'<path d="M{x+505} {y+215} C{x+565} {y+285}, {x+570} {y+395}, {x+545} {y+500}" class="arrowO"/>\n'
            s += f'<path d="M{x+365} {y+215} C{x+365} {y+290}, {x+365} {y+360}, {x+365} {y+450}" class="arrowG"/>\n'
            s += f'<path d="M{x+188} {y+500} C{x+190} {y+390}, {x+180} {y+285}, {x+260} {y+215}" class="return"/>\n'
            s += f'<path d="M{x+545} {y+500} C{x+545} {y+390}, {x+560} {y+285}, {x+470} {y+215}" class="return"/>\n'
            s += line_text(x + panel_w / 2, y + 520, "发礼后按蓝虚线回台", "txt", "middle")
        else:
            s += hand_rect(x + 92, y + 88, panel_w - 184, 355, "stage", "舞台")
            s += f'<line x1="{x+130}" y1="{y+443}" x2="{x+panel_w-130}" y2="{y+443}" class="stageFront"/>\n'
            heart = f'M{x+265} {y+300} C{x+250} {y+180}, {x+375} {y+165}, {x+430} {y+245} C{x+490} {y+165}, {x+620} {y+180}, {x+600} {y+300} C{x+585} {y+390}, {x+485} {y+415}, {x+430} {y+455} C{x+375} {y+415}, {x+280} {y+390}, {x+265} {y+300}'
            s += f'<path d="{heart}" class="dash"/>\n'
            for i, key in enumerate(["语", "数", "英", "科", "社"]):
                s += stick(x + 315 + i * 58, y + 405, key, key, 0.48, "basket", True)
            for i, key in enumerate(["语", "数", "英", "科", "社", "英", "科"]):
                s += stick(x + 290 + i * 58, y + 280 - abs(i - 3) * 18, key, "", 0.42, "wave")
            s += line_text(x + panel_w / 2, y + 520, "五篮在前，后排心形", "txt", "middle")
    return s + svg_end()


def page_venue():
    s = svg_start("01 场地总览与方向", "台下三部分：左侧观众席、主观众席、右侧观众席；主侧之间是两条国道/过道") + group_legend(260, 108)
    s += venue(0, 40, 1.0, labels=True, seats=True)
    s += '<path d="M575 315 C555 370,560 405,580 470" class="arrowO"/>\n'
    s += '<path d="M1625 315 C1645 370,1640 405,1620 470" class="arrowO"/>\n'
    s += '<path d="M1100 315 C1100 370,1100 405,1100 470" class="arrowB"/>\n'
    s += hand_rect(124, 1287, 1952, 70, "note")
    s += line_text(165, 1331, "图例：橙线为上/下台行动线，蓝线为面向观众或回台线；两条国道/过道是发礼物和学生助手接应的主通道。", "txt")
    return s + svg_end()


def page_stage_move():
    s = svg_start("02 上台动线、站位与前移线", "17位老师两侧上台，落三排弧线；唱到本组时该组前排代表到前移线") + group_legend(260, 108)
    sx, sy, sw, sh = 180, 185, 1840, 660
    s += hand_rect(sx, sy, sw, sh, "stage", "舞台放大图")
    s += f'<line x1="{sx+40}" y1="{sy+sh}" x2="{sx+sw-40}" y2="{sy+sh}" class="stageFront"/>\n'
    s += line_text(sx + sw / 2, sy + sh + 38, "台口 / 面向三块观众席", "h2", "middle")
    s += f'<path d="M{sx+160} {sy+520} C{sx+520} {sy+430}, {sx+1320} {sy+430}, {sx+1680} {sy+520}" class="dash"/>\n'
    s += f'<path d="M{sx+210} {sy+390} C{sx+580} {sy+280}, {sx+1260} {sy+280}, {sx+1630} {sy+390}" class="dash"/>\n'
    s += f'<path d="M{sx+260} {sy+255} C{sx+620} {sy+170}, {sx+1220} {sy+170}, {sx+1580} {sy+255}" class="dash"/>\n'
    s += f'<path d="M{sx+35} {sy+650} C{sx+120} {sy+595}, {sx+165} {sy+540}, {sx+250} {sy+505}" class="arrowO"/>\n'
    s += f'<path d="M{sx+sw-35} {sy+650} C{sx+sw-120} {sy+595}, {sx+sw-165} {sy+540}, {sx+sw-250} {sy+505}" class="arrowO"/>\n'
    s += line_text(sx + 75, sy + 620, "左侧上台：语 数 英", "txt")
    s += line_text(sx + sw - 75, sy + 620, "右侧上台：科 社", "txt", "end")
    people, pts = stage_people(sx + 145, sy + 80, sw - 290, sh - 175, 1.15)
    s += people
    front_y = sy + sh - 82
    s += f'<path d="M{sx+250} {front_y} C{sx+620} {front_y-55}, {sx+1250} {front_y-55}, {sx+1590} {front_y}" class="dash"/>\n'
    s += line_text(sx + sw / 2, front_y - 76, "前移线：唱到本组时站到这里", "h2", "middle")
    front_points = {
        "语": (sx + 420, front_y),
        "数": (sx + 700, front_y - 38),
        "英": (sx + 950, front_y - 55),
        "科": (sx + 1220, front_y - 38),
        "社": (sx + 1490, front_y),
    }
    reps = [("语1", "语", "L1-L2"), ("数1", "数", "L3-L4"), ("英1", "英", "L5-L7"), ("科1", "科", "L8-L10"), ("社1", "社", "L11-L12")]
    for label, key, lyric in reps:
        x1, y1 = pts[label]
        x2, y2 = front_points[key]
        s += f'<path d="M{x1} {y1+20} C{(x1+x2)/2} {y1+85}, {(x1+x2)/2} {y2-80}, {x2} {y2}" class="arrowO"/>\n'
        s += stick(x2, y2, key, label, 0.74, "sing")
        s += line_text(x2, y2 + 60, lyric, "small", "middle")
    s += hand_rect(180, 925, 1840, 150, "note")
    s += multiline(230, 975, [
        "站位：三排弧线面向台下三块观众席，前排五人是各组下台发礼代表。",
        "前移：唱到本组，前排代表到前移线亮相；组员原位轻拍或摆手；唱完回弧线。",
    ], "txt", 44)
    return s + svg_end()


def page_lyrics():
    s = svg_start("03 歌曲段落动作分镜", "按伴奏字幕编号 L1、L2……；每一段对应组别、前移点和舞台口令") + group_legend(260, 108)
    s += hand_rect(85, 165, 2030, 1060, "paper")
    headers = ["段落", "演唱/执行", "舞台动作", "执行口令"]
    widths = [230, 300, 860, 540]
    x0, y0 = 130, 225
    s += f'<rect x="{x0}" y="{y0}" width="{sum(widths)}" height="54" rx="10" class="lyrics"/>\n'
    x = x0
    for h, w in zip(headers, widths):
        s += line_text(x + 18, y0 + 36, h, "h2")
        x += w
    rows = [
        ("前奏", "全体", "语数英从左侧上台；科社从右侧上台；站三排弧线", "两侧上台"),
        ("L1-L2", "语文组", "语1到前移点1；语2、语3原位轻拍", "语文前移"),
        ("L3-L4", "数学组", "数1到前移点2；数2、数3原位轻拍", "数学前移"),
        ("L5-L7", "英语组", "英1到前移点3；英2、英3、英4左右摆手", "英语前移"),
        ("L8-L10", "科学组", "科1到前移点4；科2、科3、科4左右摆手", "科学前移"),
        ("L11-L12", "社政组", "社1到前移点5；社2、社3原位轻拍", "社政前移"),
        ("副歌1", "全体", "五组归入三排弧线；面向台下三块观众席小幅摆手", "全体合唱"),
        ("副歌2", "发礼准备", "语1、数1、英1、科1、社1从舞台后侧取花篮", "五人取篮"),
        ("尾副歌", "台上12人", "台上继续唱；五位老师按两条国道/过道下台发礼", "发礼互动"),
        ("尾声", "全体", "五位老师回台；五篮在前，后排成心形花瓣", "Ending Pose"),
    ]
    row_h = 82
    for i, row in enumerate(rows):
        yy = y0 + 62 + i * row_h
        s += f'<rect x="{x0}" y="{yy}" width="{sum(widths)}" height="{row_h-10}" rx="10" class="lyrics"/>\n'
        x = x0
        for text, w in zip(row, widths):
            s += line_text(x + 18, yy + 45, text, "txt")
            x += w
    s += hand_rect(130, 1120, 1930, 80, "note")
    s += line_text(170, 1170, "排练时只需要把正式伴奏字幕标上 L1-L31，再按本页口令喊组别和动作。", "txt")
    return s + svg_end()


def page_gift_route():
    s = svg_start("04 发礼物动线：下台、分发、回台", "五位老师下台发礼；学生助手在各区排头接礼并向座位内传；蓝色虚线为回台路线") + group_legend(260, 108)
    s += venue(0, 40, 1.0, labels=True, seats=True)
    # Start points at the stage front.
    starts = {
        "语1": (720, 325, "语"),
        "数1": (900, 325, "数"),
        "英1": (1100, 325, "英"),
        "科1": (1300, 325, "科"),
        "社1": (1480, 325, "社"),
    }
    for label, (x, y, key) in starts.items():
        s += stick(x, y, key, label, 0.62, "basket", True)
    # Outbound gift routes.
    s += '<path d="M720 350 C625 430,575 550,570 720 C565 870,505 950,330 1000" class="arrowO"/>\n'
    s += '<path d="M900 350 C760 465,620 610,590 790 C570 910,690 1005,805 1035" class="arrowO"/>\n'
    s += '<path d="M1100 350 C1100 430,1100 500,1100 620" class="arrowG"/>\n'
    s += '<path d="M1300 350 C1440 465,1580 610,1610 790 C1630 910,1510 1005,1395 1035" class="arrowO"/>\n'
    s += '<path d="M1480 350 C1575 430,1625 550,1630 720 C1635 870,1695 950,1870 1000" class="arrowO"/>\n'
    # Return routes, drawn offset from outbound routes.
    s += '<path d="M330 995 C500 910,535 780,548 625 C560 480,620 390,700 330" class="return"/>\n'
    s += '<path d="M805 1035 C700 955,620 875,615 745 C610 570,740 430,880 330" class="return"/>\n'
    s += '<path d="M1100 620 C1100 520,1100 420,1100 330" class="return"/>\n'
    s += '<path d="M1395 1035 C1500 955,1580 875,1585 745 C1590 570,1460 430,1320 330" class="return"/>\n'
    s += '<path d="M1870 995 C1700 910,1665 780,1652 625 C1640 480,1580 390,1500 330" class="return"/>\n'
    # Gift-passing lanes.
    for yy in [570, 700, 830, 960]:
        s += f'<rect x="505" y="{yy}" width="34" height="24" rx="5" fill="#fef08a" stroke="#ca8a04" stroke-width="2"/>\n'
        s += f'<path d="M539 {yy+12} C600 {yy-5}, 650 {yy-5}, 715 {yy+12}" class="arrowG"/>\n'
        s += f'<rect x="645" y="{yy}" width="34" height="24" rx="5" fill="#fef08a" stroke="#ca8a04" stroke-width="2"/>\n'
        s += f'<path d="M679 {yy+12} C780 {yy-6}, 900 {yy-6}, 1035 {yy+12}" class="arrowG"/>\n'
        s += f'<rect x="1525" y="{yy}" width="34" height="24" rx="5" fill="#fef08a" stroke="#ca8a04" stroke-width="2"/>\n'
        s += f'<path d="M1525 {yy+12} C1420 {yy-6}, 1300 {yy-6}, 1165 {yy+12}" class="arrowG"/>\n'
        s += f'<rect x="1662" y="{yy}" width="34" height="24" rx="5" fill="#fef08a" stroke="#ca8a04" stroke-width="2"/>\n'
        s += f'<path d="M1662 {yy+12} C1605 {yy-5}, 1552 {yy-5}, 1495 {yy+12}" class="arrowG"/>\n'
    for x, y, label in [
        (545, 545, "助"), (545, 820, "助"), (1048, 585, "助"),
        (1605, 545, "助"), (1605, 820, "助"), (1850, 890, "助"), (350, 890, "助"),
    ]:
        s += stick(x, y, "助", label, 0.52, "down", gift=True)
    s += hand_rect(115, 1185, 1970, 115, "note")
    s += multiline(155, 1230, [
        "发礼分配：语1服务左侧观众席；数1服务主观众席左半；英1在台口中线交接主观众席中间；科1服务主观众席右半；社1服务右侧观众席。",
        "回台：尾声口令后五人按蓝色虚线回台，回到台口前排，直接摆 Ending Pose。",
    ], "txt", 42)
    return s + svg_end()


def page_ending():
    s = svg_start("05 Ending Pose：心愿花", "五个花篮在台口前排，十二位老师在后方形成心形花瓣弧线") + group_legend(260, 108)
    sx, sy, sw, sh = 260, 165, 1680, 790
    s += hand_rect(sx, sy, sw, sh, "stage", "舞台放大图")
    s += f'<line x1="{sx+50}" y1="{sy+sh}" x2="{sx+sw-50}" y2="{sy+sh}" class="stageFront"/>\n'
    s += line_text(sx + sw / 2, sy + sh + 75, "台口 / 面向三块观众席", "h2", "middle")
    heart = (
        f"M{sx+430} {sy+450} "
        f"C{sx+370} {sy+235}, {sx+650} {sy+185}, {sx+835} {sy+365} "
        f"C{sx+1030} {sy+185}, {sx+1310} {sy+235}, {sx+1250} {sy+450} "
        f"C{sx+1210} {sy+610}, {sx+960} {sy+680}, {sx+840} {sy+735} "
        f"C{sx+720} {sy+680}, {sx+470} {sy+610}, {sx+430} {sy+450}"
    )
    s += f'<path d="{heart}" class="dash"/>\n'
    back = [
        ("语2", "语", sx + 515, sy + 485), ("语3", "语", sx + 565, sy + 345),
        ("数2", "数", sx + 735, sy + 295), ("数3", "数", sx + 810, sy + 410),
        ("英2", "英", sx + 910, sy + 410), ("英3", "英", sx + 985, sy + 295),
        ("英4", "英", sx + 1135, sy + 345), ("科2", "科", sx + 1185, sy + 485),
        ("科3", "科", sx + 1115, sy + 615), ("科4", "科", sx + 980, sy + 690),
        ("社2", "社", sx + 700, sy + 690), ("社3", "社", sx + 565, sy + 615),
    ]
    front = [
        ("语1", "语", sx + 620, sy + 725),
        ("数1", "数", sx + 730, sy + 770),
        ("英1", "英", sx + 840, sy + 790),
        ("科1", "科", sx + 950, sy + 770),
        ("社1", "社", sx + 1060, sy + 725),
    ]
    for label, key, x, y in back:
        s += stick(x, y, key, label, 0.75, "wave")
    for label, key, x, y in front:
        s += stick(x, y, key, label, 0.82, "basket", True)
    s += hand_rect(260, 1070, 1680, 125, "note")
    s += multiline(310, 1120, [
        "回台后：五位发礼老师带花篮站台口前排；其他十二位从左右向中间收成心形花瓣。",
        "定格口令：前排五篮，后排花瓣，全体微笑合唱，停两拍鞠躬退场。",
    ], "txt", 44)
    return s + svg_end()


def page_script_card():
    s = svg_start("06 执行口令卡", "主持、音乐、舞台监督、学生助手可共用这一页核对流程") + group_legend(260, 108)
    s += hand_rect(115, 170, 1970, 1030, "paper")
    rows = [
        ("前奏", "音乐起", "两侧上台，三排弧线站定"),
        ("主歌1", "L1-L12", "五组按语、数、英、科、社顺序前移轮唱"),
        ("副歌1", "L13-L16", "全体归入弧线，面向台下三块观众席摆手"),
        ("主歌2", "L17-L21", "五组各接一句，对应组前移点亮相"),
        ("副歌2", "L22-L25", "五位发礼老师后侧取篮，其他人保持合唱"),
        ("尾副歌", "L26-L30", "五人沿两条国道/过道和中线发礼，学生助手接礼向内传"),
        ("尾声", "L31", "五人按蓝虚线回台，全体组成心愿花定格"),
        ("收束", "感谢词", "停两拍鞠躬，按两侧路线退场"),
    ]
    x0, y0 = 170, 245
    col_w = [260, 300, 1320]
    s += f'<rect x="{x0}" y="{y0}" width="{sum(col_w)}" height="58" rx="10" class="lyrics"/>\n'
    for i, h in enumerate(["段落", "歌词卡", "执行动作"]):
        s += line_text(x0 + sum(col_w[:i]) + 22, y0 + 38, h, "h2")
    for r, row in enumerate(rows):
        yy = y0 + 76 + r * 92
        s += f'<rect x="{x0}" y="{yy}" width="{sum(col_w)}" height="74" rx="10" class="lyrics"/>\n'
        for i, text in enumerate(row):
            s += line_text(x0 + sum(col_w[:i]) + 22, yy + 47, text, "txt")
    s += hand_rect(170, 1080, 1860, 90, "note")
    s += line_text(210, 1135, "学生助手位置：左国道排头、右国道排头、主观众席中区前排、左右侧观众席排头各设一人。", "txt")
    return s + svg_end()


def write_all():
    pages = [
        ("00_电影分镜总览.svg", page_overview()),
        ("01_场地总览与方向.svg", page_venue()),
        ("02_上台站位与前移线.svg", page_stage_move()),
        ("03_歌曲段落动作分镜.svg", page_lyrics()),
        ("04_发礼物动线与回台路线.svg", page_gift_route()),
        ("05_EndingPose_心愿花.svg", page_ending()),
        ("06_执行口令卡.svg", page_script_card()),
    ]
    for name, body in pages:
        (OUT / name).write_text(body, encoding="utf-8")
    md = """# 《心愿便利贴》三观众席简笔分镜 v7

## 场地设定

- 台下观众席分三部分：左侧观众席、主观众席、右侧观众席。
- 主观众席与两侧观众席之间各有一条国道/过道。
- 舞台在图面上方，台口面向三块观众席。

## 舞台动线

- 上台：语文、数学、英语从左侧上台；科学、社政从右侧上台。
- 站位：17位老师形成三排弧线，前排五人为语1、数1、英1、科1、社1。
- 前移：唱到本组时，前排代表站到前移线；组员原位轻拍或摆手；唱完归回弧线。

## 发礼物动线

- 语1：走左国道/过道，服务左侧观众席。
- 数1：走左国道/过道，服务主观众席左半。
- 英1：走台口中线，交接主观众席中间。
- 科1：走右国道/过道，服务主观众席右半。
- 社1：走右国道/过道，服务右侧观众席。
- 学生助手在各区排头接礼，并向座位内传。
- 尾声口令后，五位老师按蓝色虚线回台。

## Ending Pose

- 五个花篮站台口前排。
- 其余十二位老师在后方形成心形花瓣弧线。
- 口令：前排五篮，后排花瓣，全体微笑合唱，停两拍鞠躬退场。
"""
    (OUT / "心愿便利贴_三观众席简笔分镜_v7_说明.md").write_text(md, encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    write_all()
