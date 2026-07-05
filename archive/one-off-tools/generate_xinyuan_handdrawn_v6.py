from pathlib import Path
from xml.sax.saxutils import escape


OUT = Path("/Users/wuyue/Documents/自主管理学院/output/心愿便利贴_白底手绘分镜_v6")
OUT.mkdir(parents=True, exist_ok=True)

W, H = 2200, 1400

COLORS = {
    "语": "#dc2626",
    "数": "#2563eb",
    "英": "#16a34a",
    "科": "#d97706",
    "社": "#7c3aed",
    "学": "#111827",
    "助": "#64748b",
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
      .seat {{ fill:none; stroke:#111827; stroke-width:2; stroke-linecap:round; }}
      .aisle {{ fill:#fff; stroke:#be123c; stroke-width:3; stroke-linecap:round; stroke-linejoin:round; }}
      .stage {{ fill:#fff; stroke:#111827; stroke-width:3.4; stroke-linecap:round; stroke-linejoin:round; }}
      .stageFront {{ stroke:#f97316; stroke-width:5.5; stroke-linecap:round; }}
      .note {{ fill:#fff7ed; stroke:#fb923c; stroke-width:2.5; stroke-linecap:round; stroke-linejoin:round; }}
      .lyrics {{ fill:#f8fafc; stroke:#cbd5e1; stroke-width:2.2; stroke-linecap:round; stroke-linejoin:round; }}
      .arrowO {{ fill:none; stroke:#f97316; stroke-width:4.8; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#arrO); }}
      .arrowB {{ fill:none; stroke:#2563eb; stroke-width:4.4; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#arrB); }}
      .arrowG {{ fill:none; stroke:#16a34a; stroke-width:4.2; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#arrG); }}
      .arrowP {{ fill:none; stroke:#7c3aed; stroke-width:4.2; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#arrP); }}
    </style>
    <marker id="arrO" markerWidth="14" markerHeight="14" refX="11" refY="7" orient="auto"><path d="M2,2 L12,7 L2,12 Z" fill="#f97316"/></marker>
    <marker id="arrB" markerWidth="14" markerHeight="14" refX="11" refY="7" orient="auto"><path d="M2,2 L12,7 L2,12 Z" fill="#2563eb"/></marker>
    <marker id="arrG" markerWidth="14" markerHeight="14" refX="11" refY="7" orient="auto"><path d="M2,2 L12,7 L2,12 Z" fill="#16a34a"/></marker>
    <marker id="arrP" markerWidth="14" markerHeight="14" refX="11" refY="7" orient="auto"><path d="M2,2 L12,7 L2,12 Z" fill="#7c3aed"/></marker>
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


def hand_trapezoid(points, cls="paper", label=None, tx=None, ty=None):
    p = " ".join(f"{x},{y}" for x, y in points)
    s = f'<polygon points="{p}" class="{cls}"/>\n'
    if label:
        lx = tx if tx is not None else sum(x for x, _ in points) / len(points)
        ly = ty if ty is not None else sum(y for _, y in points) / len(points)
        s += f'<text x="{lx}" y="{ly}" text-anchor="middle" class="h2">{e(label)}</text>\n'
    return s


def line_text(x, y, text, cls="txt", anchor="start"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{e(text)}</text>\n'


def group_legend(x=350, y=112):
    items = [("语文3人", "语"), ("数学3人", "数"), ("英语4人", "英"), ("科学4人", "科"), ("社政3人", "社")]
    s = ""
    for i, (label, key) in enumerate(items):
        xx = x + i * 300
        s += stick(xx, y + 18, key, "", 0.48)
        s += f'<text x="{xx+26}" y="{y+25}" class="txt">{e(label)}</text>\n'
    s += f'<text x="{x + 1500}" y="{y+25}" class="txt">共17人</text>\n'
    return s


def stick(x, y, key, label="", scale=1.0, arms="down", basket=False, gift=False):
    c = COLORS[key]
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
    s = f'''
  <g transform="translate({x},{y})">
    <circle cx="0" cy="{-22*scale}" r="{head_r}" fill="#fff" stroke="{c}" stroke-width="{sw}"/>
    <line x1="0" y1="{-8*scale}" x2="0" y2="{body*0.62}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/>
    {arms_path}
    <line x1="0" y1="{body*0.62}" x2="{-leg*0.62}" y2="{body}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/>
    <line x1="0" y1="{body*0.62}" x2="{leg*0.62}" y2="{body}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/>
'''
    if label:
        s += f'    <text x="0" y="{-17*scale}" text-anchor="middle" class="tiny" fill="{c}">{e(label)}</text>\n'
    if basket:
        s += f'''
    <path d="M{-24*scale},{18*scale} Q0,{-8*scale} {24*scale},{18*scale}" fill="none" stroke="#ea580c" stroke-width="{2.5*scale}" stroke-linecap="round"/>
    <rect x="{-26*scale}" y="{18*scale}" width="{52*scale}" height="{34*scale}" rx="{7*scale}" fill="#fff7ed" stroke="#ea580c" stroke-width="{2.5*scale}"/>
'''
    if gift:
        s += f'<rect x="{17*scale}" y="{10*scale}" width="{22*scale}" height="{17*scale}" rx="{3*scale}" fill="#fef08a" stroke="#ca8a04" stroke-width="{2*scale}"/>\n'
    s += "  </g>\n"
    return s


def basket_icon(x, y, label="", scale=1.0):
    return f'''
  <g transform="translate({x},{y})">
    <path d="M{-28*scale},0 Q0,{-36*scale} {28*scale},0" fill="none" stroke="#ea580c" stroke-width="{2.6*scale}" stroke-linecap="round"/>
    <rect x="{-32*scale}" y="0" width="{64*scale}" height="{42*scale}" rx="{8*scale}" fill="#fff7ed" stroke="#ea580c" stroke-width="{2.6*scale}"/>
    <circle cx="{-16*scale}" cy="{3*scale}" r="{5*scale}" fill="#ef4444"/>
    <circle cx="0" cy="{-4*scale}" r="{5*scale}" fill="#f59e0b"/>
    <circle cx="{16*scale}" cy="{3*scale}" r="{5*scale}" fill="#22c55e"/>
    <text x="0" y="{30*scale}" text-anchor="middle" class="tiny">{e(label)}</text>
  </g>'''


def venue(x=0, y=0, scale=1.0, labels=True, seats=True):
    def sx(v): return x + v * scale
    def sy(v): return y + v * scale
    s = ""
    s += hand_rect(sx(690), sy(120), 820 * scale, 150 * scale, "stage", "舞台" if labels else None)
    s += f'<line x1="{sx(715)}" y1="{sy(270)}" x2="{sx(1485)}" y2="{sy(270)}" class="stageFront"/>\n'
    if labels:
        s += line_text(sx(1100), sy(305), "台口面向观众", "small", "middle")
        s += hand_rect(sx(1568), sy(285), 72 * scale, 58 * scale, "soft", "门")
    s += hand_trapezoid([(sx(250), sy(470)), (sx(545), sy(410)), (sx(575), sy(1055)), (sx(225), sy(1110))], "paper", "观众席" if labels else None, sx(395), sy(720))
    s += hand_trapezoid([(sx(565), sy(380)), (sx(665), sy(330)), (sx(705), sy(1120)), (sx(605), sy(1160))], "aisle", "左过道" if labels else None, sx(635), sy(760))
    s += hand_rect(sx(735), sy(360), 730 * scale, 765 * scale, "paper", "观众席" if labels else None)
    s += hand_trapezoid([(sx(1495), sy(330)), (sx(1600), sy(385)), (sx(1580), sy(1160)), (sx(1480), sy(1120))], "aisle", "右过道" if labels else None, sx(1535), sy(760))
    s += hand_trapezoid([(sx(1625), sy(410)), (sx(1920), sy(470)), (sx(1950), sy(1110)), (sx(1600), sy(1055))], "paper", "观众席" if labels else None, sx(1765), sy(720))
    if seats:
        for row in range(5):
            yy = sy(500 + row * 105)
            s += f'<path d="M{sx(810)} {yy} C{sx(960)} {yy-35*scale}, {sx(1220)} {yy-35*scale}, {sx(1390)} {yy}" class="seat"/>\n'
        for row in range(5):
            s += f'<path d="M{sx(310)} {sy(555+row*95)} C{sx(380)} {sy(525+row*95)}, {sx(480)} {sy(525+row*95)}, {sx(535)} {sy(560+row*95)}" class="seat"/>\n'
            s += f'<path d="M{sx(1665)} {sy(560+row*95)} C{sx(1730)} {sy(525+row*95)}, {sx(1830)} {sy(525+row*95)}, {sx(1900)} {sy(555+row*95)}" class="seat"/>\n'
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
            row = i % 3
            px = cx + local * 42 * scale
            py = stage_y + stage_h * (0.48 + row * 0.14) + abs(local) * 6 * scale
            if i == 0:
                py = stage_y + stage_h * 0.70 + front_extra
            elif i == 1:
                py = stage_y + stage_h * 0.52
            else:
                py = stage_y + stage_h * 0.35 + (i - 2) * 18 * scale
            points[label] = (px, py)
            s += stick(px, py, key, label, 0.68 * scale, "down")
    return s, points


def overview_page():
    s = svg_start("教师表演《心愿便利贴》报告厅流程图", "白底手绘分镜｜按最新舞台与观众席示意图绘制") + group_legend(320, 108)
    margin_x, gap_x = 36, 24
    panel_w = (W - 2 * margin_x - 2 * gap_x) / 3
    panel_h = 555
    y1, y2 = 165, 785
    titles = ["① 场地总览", "② 上台落位", "③ 小组唱前移", "④ 歌词动作", "⑤ 发礼回台", "⑥ Ending Pose"]
    for idx, title in enumerate(titles):
        row = 0 if idx < 3 else 1
        col = idx % 3
        x = margin_x + col * (panel_w + gap_x)
        y = y1 if row == 0 else y2
        s += hand_rect(x, y, panel_w, panel_h, "paper")
        s += line_text(x + 24, y + 42, title, "h1")
        if idx == 0:
            s += venue(x - 112, y + 15, 0.40, labels=True, seats=True)
        elif idx == 1:
            s += hand_rect(x + 65, y + 92, panel_w - 130, 195, "stage", "舞台")
            s += f'<line x1="{x+95}" y1="{y+287}" x2="{x+panel_w-95}" y2="{y+287}" class="stageFront"/>\n'
            sp, pts = stage_people(x + 80, y + 105, panel_w - 160, 170, 0.70)
            s += sp
            s += f'<path d="M{x+80} {y+320} C{x+185} {y+285}, {x+250} {y+260}, {x+330} {y+235}" class="arrowO"/>\n'
            s += f'<path d="M{x+panel_w-80} {y+320} C{x+panel_w-190} {y+285}, {x+panel_w-260} {y+260}, {x+panel_w-340} {y+235}" class="arrowO"/>\n'
            s += line_text(x + panel_w / 2, y + 365, "两侧上台，三排弧线落位", "txt", "middle")
        elif idx == 2:
            s += hand_rect(x + 70, y + 95, panel_w - 140, 230, "stage", "舞台")
            s += f'<line x1="{x+105}" y1="{y+314}" x2="{x+panel_w-105}" y2="{y+314}" class="stageFront"/>\n'
            s += f'<path d="M{x+125} {y+280} C{x+260} {y+230}, {x+panel_w-260} {y+230}, {x+panel_w-125} {y+280}" class="dash"/>\n'
            for i, (key, label) in enumerate([("语", "L1-2"), ("数", "L3-4"), ("英", "L5-7"), ("科", "L8-10"), ("社", "L11-12")]):
                px = x + 150 + i * 116
                s += stick(px, y + 245, key, key, 0.58, "sing")
                s += f'<path d="M{px} {y+240} C{px-10} {y+215}, {px-5} {y+195}, {px+15} {y+175}" class="arrowO"/>\n'
                s += line_text(px, y + 350, label, "tiny", "middle")
            s += line_text(x + panel_w / 2, y + 392, "唱到本组，前排到前移线", "txt", "middle")
        elif idx == 3:
            rows = [("语文", "L1-2", "前移点1"), ("数学", "L3-4", "前移点2"), ("英语", "L5-7", "前移点3"), ("科学", "L8-10", "前移点4"), ("社政", "L11-12", "前移点5")]
            for r, (g, l, a) in enumerate(rows):
                yy = y + 95 + r * 70
                s += f'<rect x="{x+55}" y="{yy}" width="{panel_w-110}" height="52" rx="10" class="lyrics"/>\n'
                s += line_text(x + 82, yy + 34, f"{g} {l}", "txt")
                s += line_text(x + 330, yy + 34, a, "small")
            s += line_text(x + panel_w / 2, y + 505, "副歌全体合唱，尾副歌发礼互动", "txt", "middle")
        elif idx == 4:
            s += venue(x - 125, y + 30, 0.37, labels=False, seats=False)
            s += line_text(x + 182, y + 112, "舞台", "h2", "middle")
            for key, label, px, py in [("语", "语1", 285, 200), ("数", "数1", 360, 210), ("英", "英1", 450, 210), ("科", "科1", 530, 210), ("社", "社1", 600, 200)]:
                s += stick(x + px, y + py, key, label, 0.47, "basket", True)
            s += f'<path d="M{x+300} {y+235} C{x+250} {y+310}, {x+235} {y+430}, {x+225} {y+505}" class="arrowO"/>\n'
            s += f'<path d="M{x+565} {y+235} C{x+625} {y+310}, {x+635} {y+430}, {x+625} {y+505}" class="arrowO"/>\n'
            s += f'<path d="M{x+450} {y+235} C{x+445} {y+285}, {x+445} {y+330}, {x+445} {y+375}" class="arrowG"/>\n'
            s += line_text(x + panel_w / 2, y + 520, "两条过道发礼，蓝线回台", "txt", "middle")
        else:
            s += hand_rect(x + 90, y + 88, panel_w - 180, 355, "stage", "舞台")
            s += f'<line x1="{x+130}" y1="{y+443}" x2="{x+panel_w-130}" y2="{y+443}" class="stageFront"/>\n'
            heart = f'M{x+265} {y+300} C{x+250} {y+180}, {x+375} {y+165}, {x+430} {y+245} C{x+490} {y+165}, {x+620} {y+180}, {x+600} {y+300} C{x+585} {y+390}, {x+485} {y+415}, {x+430} {y+455} C{x+375} {y+415}, {x+280} {y+390}, {x+265} {y+300}'
            s += f'<path d="{heart}" class="dash"/>\n'
            for i, key in enumerate(["语", "数", "英", "科", "社"]):
                s += stick(x + 315 + i * 58, y + 405, key, key, 0.48, "basket", True)
            for i, key in enumerate(["语", "数", "英", "科", "社", "英", "科"]):
                s += stick(x + 290 + i * 58, y + 280 - abs(i - 3) * 18, key, "", 0.42, "wave")
            s += line_text(x + panel_w / 2, y + 520, "五篮在前，后排成心愿花", "txt", "middle")
    return s + svg_end()


def page_venue():
    s = svg_start("01 场地总览与方向", "舞台在前方，台口面向观众席；左右过道服务发礼与回台") + group_legend(320, 108)
    s += venue(0, 40, 1.0, labels=True, seats=True)
    s += '<path d="M710 315 C640 360,610 430,615 520" class="arrowO"/>\n'
    s += '<path d="M1490 315 C1565 365,1590 435,1585 520" class="arrowO"/>\n'
    s += '<path d="M1100 300 C1100 345,1100 390,1100 430" class="arrowB"/>\n'
    s += hand_rect(120, 1155, 1960, 120, "note")
    s += line_text(160, 1205, "执行口诀：舞台上方，观众下方；左过道连左区和中区左半，右过道连右区和中区右半。", "txt")
    s += line_text(160, 1248, "门口在右侧前方，学生助手可在门口与两条过道排头接应。", "txt")
    return s + svg_end()


def page_stage_move():
    s = svg_start("02 上台站位与小组前移", "17位老师两侧上台，落三排弧线；唱到本组时前排到前移线") + group_legend(320, 108)
    sx, sy, sw, sh = 180, 185, 1840, 660
    s += hand_rect(sx, sy, sw, sh, "stage", "舞台放大图")
    s += f'<line x1="{sx+40}" y1="{sy+sh}" x2="{sx+sw-40}" y2="{sy+sh}" class="stageFront"/>\n'
    s += line_text(sx + sw / 2, sy + sh + 38, "台口 / 面向观众", "h2", "middle")
    s += f'<path d="M{sx+160} {sy+520} C{sx+520} {sy+430}, {sx+1320} {sy+430}, {sx+1680} {sy+520}" class="dash"/>\n'
    s += f'<path d="M{sx+210} {sy+390} C{sx+580} {sy+280}, {sx+1260} {sy+280}, {sx+1630} {sy+390}" class="dash"/>\n'
    s += f'<path d="M{sx+260} {sy+255} C{sx+620} {sy+170}, {sx+1220} {sy+170}, {sx+1580} {sy+255}" class="dash"/>\n'
    people, pts = stage_people(sx + 145, sy + 80, sw - 290, sh - 175, 1.15)
    s += people
    front_y = sy + sh - 78
    s += f'<path d="M{sx+250} {front_y} C{sx+620} {front_y-55}, {sx+1250} {front_y-55}, {sx+1590} {front_y}" class="dash"/>\n'
    s += line_text(sx + sw / 2, front_y - 72, "前移线", "h2", "middle")
    front_points = {
        "语": (sx + 420, front_y),
        "数": (sx + 700, front_y - 38),
        "英": (sx + 950, front_y - 55),
        "科": (sx + 1220, front_y - 38),
        "社": (sx + 1490, front_y),
    }
    reps = [("语1", "语", "L1-2"), ("数1", "数", "L3-4"), ("英1", "英", "L5-7"), ("科1", "科", "L8-10"), ("社1", "社", "L11-12")]
    for label, key, lyric in reps:
        x1, y1 = pts[label]
        x2, y2 = front_points[key]
        s += f'<path d="M{x1} {y1+20} C{(x1+x2)/2} {y1+85}, {(x1+x2)/2} {y2-80}, {x2} {y2}" class="arrowO"/>\n'
        s += stick(x2, y2, key, label, 0.74, "sing")
        s += line_text(x2, y2 + 60, lyric, "small", "middle")
    s += hand_rect(180, 925, 1840, 145, "note")
    s += line_text(230, 975, "上台分配：语文、数学、英语从左侧进入；科学、社政从右侧进入；各组按三排弧线站成合唱队形。", "txt")
    s += line_text(230, 1020, "前移动作：本组前排代表到前移线演唱，组员原位轻拍，唱完归入弧线。", "txt")
    return s + svg_end()


def page_lyrics():
    s = svg_start("03 歌词分配与动作对应", "正式歌词按伴奏字幕逐句编号；每个歌词卡对应组别、站位和动作") + group_legend(320, 108)
    s += hand_rect(85, 165, 2030, 1060, "paper")
    headers = ["歌词卡", "演唱组", "站位动作", "舞台口令"]
    widths = [230, 270, 870, 560]
    x0, y0 = 130, 225
    s += f'<rect x="{x0}" y="{y0}" width="{sum(widths)}" height="54" rx="10" class="lyrics"/>\n'
    x = x0
    for h, w in zip(headers, widths):
        s += line_text(x + 18, y0 + 36, h, "h2")
        x += w
    rows = [
        ("L1-L2", "语文组", "语1到前移点1；语2、语3轻拍两拍", "语文前移"),
        ("L3-L4", "数学组", "数1到前移点2；数2、数3轻拍两拍", "数学前移"),
        ("L5-L7", "英语组", "英1到前移点3；英2、英3、英4左右摆手", "英语前移"),
        ("L8-L10", "科学组", "科1到前移点4；科2、科3、科4左右摆手", "科学前移"),
        ("L11-L12", "社政组", "社1到前移点5；社2、社3轻拍两拍", "社政前移"),
        ("L13-L16", "全体合唱", "五组归入三排弧线；面向观众小幅摆手", "副歌合唱"),
        ("L17-L21", "五组轮唱", "语、数、英、科、社各接一句；对应组前移", "第二轮轮唱"),
        ("L22-L25", "全体合唱", "台上保持合唱；五位发礼老师从后侧取篮", "取篮准备"),
        ("L26-L30", "台上12人", "台上继续唱；五位老师沿路线发礼互动", "发礼互动"),
        ("L31", "全体收尾", "五位老师回台；全体组成心愿花定格", "Ending Pose"),
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
    s += line_text(170, 1170, "使用方式：把伴奏字幕逐句标成 L1、L2、L3，再按表格分给对应组；排练时直接喊舞台口令。", "txt")
    return s + svg_end()


def page_gift_route():
    s = svg_start("04 发礼物动线与回台路线", "语1、数1、英1、科1、社1下台发礼；学生助手在排头接礼并向内传") + group_legend(320, 108)
    s += venue(0, 40, 1.0, labels=True, seats=True)
    # Start points at stage front
    starts = {
        "语1": (790, 325, "语"),
        "数1": (910, 325, "数"),
        "英1": (1100, 325, "英"),
        "科1": (1290, 325, "科"),
        "社1": (1410, 325, "社"),
    }
    for label, (x, y, key) in starts.items():
        s += stick(x, y, key, label, 0.62, "basket", True)
    # Outbound routes
    s += '<path d="M790 350 C690 430,635 545,625 770 C620 915,595 1025,520 1090" class="arrowO"/>\n'
    s += '<path d="M910 350 C770 470,680 600,650 820 C635 960,720 1055,850 1110" class="arrowO"/>\n'
    s += '<path d="M1100 350 C1100 420,1100 465,1100 520" class="arrowG"/>\n'
    s += '<path d="M1290 350 C1430 470,1525 600,1545 820 C1560 960,1480 1055,1350 1110" class="arrowO"/>\n'
    s += '<path d="M1410 350 C1515 430,1570 545,1575 770 C1580 915,1605 1025,1680 1090" class="arrowO"/>\n'
    # Return routes
    s += '<path d="M520 1088 C585 1000,620 835,625 650 C630 500,690 400,770 330" class="arrowB"/>\n'
    s += '<path d="M1680 1088 C1615 1000,1580 835,1575 650 C1570 500,1510 400,1430 330" class="arrowB"/>\n'
    s += '<path d="M1100 520 C1100 455,1100 390,1100 330" class="arrowB"/>\n'
    # Gift transfer arrows
    for yy in [560, 700, 840, 980]:
        s += f'<rect x="680" y="{yy}" width="34" height="24" rx="5" fill="#fef08a" stroke="#ca8a04" stroke-width="2"/>\n'
        s += f'<path d="M714 {yy+12} C810 {yy-4}, 935 {yy-4}, 1040 {yy+12}" class="arrowG"/>\n'
        s += f'<rect x="1485" y="{yy}" width="34" height="24" rx="5" fill="#fef08a" stroke="#ca8a04" stroke-width="2"/>\n'
        s += f'<path d="M1485 {yy+12} C1380 {yy-4}, 1260 {yy-4}, 1165 {yy+12}" class="arrowG"/>\n'
    for pos in [(610, 590), (610, 840), (1535, 590), (1535, 840), (1100, 540)]:
        s += stick(pos[0], pos[1], "助", "助", 0.52, "gift", gift=True)
    s += hand_rect(115, 1185, 1970, 105, "note")
    s += line_text(155, 1230, "发礼分配：语1服务左侧观众席，数1服务中区左半，英1在台口中线交接中区，科1服务中区右半，社1服务右侧观众席。", "txt")
    s += line_text(155, 1272, "回台节奏：尾声口令后，左过道老师沿左线回台，右过道老师沿右线回台，英1从台口中线回台。", "txt")
    return s + svg_end()


def page_ending():
    s = svg_start("05 Ending Pose：心愿花", "五个花篮在台口前排，十二位老师在后方形成花瓣弧线") + group_legend(320, 108)
    sx, sy, sw, sh = 260, 165, 1680, 790
    s += hand_rect(sx, sy, sw, sh, "stage", "舞台放大图")
    s += f'<line x1="{sx+50}" y1="{sy+sh}" x2="{sx+sw-50}" y2="{sy+sh}" class="stageFront"/>\n'
    s += line_text(sx + sw / 2, sy + sh + 38, "台口 / 面向观众", "h2", "middle")
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
    s += hand_rect(260, 1070, 1680, 120, "note")
    s += line_text(310, 1120, "回台后，五位发礼老师带花篮站台口，十二位老师从左右向中间收成心形花瓣。", "txt")
    s += line_text(310, 1164, "口令：前排五篮，后排花瓣，全体微笑合唱，停两拍鞠躬退场。", "txt")
    return s + svg_end()


def page_script_card():
    s = svg_start("06 排练口令卡", "主持、音乐、学生助手可共用这一页核对流程") + group_legend(320, 108)
    s += hand_rect(115, 170, 1970, 1030, "paper")
    rows = [
        ("前奏", "音乐起", "两侧上台，三排弧线站定"),
        ("主歌1", "L1-L12", "五组按语、数、英、科、社顺序前移轮唱"),
        ("副歌1", "L13-L16", "全体归入弧线，面向观众小幅摆手"),
        ("主歌2", "L17-L21", "五组各接一句，对应前移点亮相"),
        ("副歌2", "L22-L25", "全体合唱，五位发礼老师后侧取篮"),
        ("尾副歌", "L26-L30", "台上12人继续唱，台下5人发礼互动"),
        ("尾声", "L31", "五位老师回台，组成心愿花定格"),
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
    s += hand_rect(170, 1080, 1860, 85, "note")
    s += line_text(210, 1132, "学生助手位置：门口、左过道排头、右过道排头、中区前排各设一人，接礼后向各排内侧传递。", "txt")
    return s + svg_end()


def write_all():
    pages = [
        ("00_六宫格总览_白底手绘.svg", overview_page()),
        ("01_场地总览与方向.svg", page_venue()),
        ("02_上台站位与小组前移.svg", page_stage_move()),
        ("03_歌词分配与动作对应.svg", page_lyrics()),
        ("04_发礼物动线与回台路线.svg", page_gift_route()),
        ("05_EndingPose_心愿花.svg", page_ending()),
        ("06_排练口令卡.svg", page_script_card()),
    ]
    for name, body in pages:
        (OUT / name).write_text(body, encoding="utf-8")
    md = """# 《心愿便利贴》白底手绘分镜 v6

## 场地设定

- 舞台在图面上方，台口面向下方观众席。
- 主观众席居中，左右各一条过道，过道外侧为侧区观众席。
- 右侧前方设门口与学生助手接应点。

## 人员与路线

- 上台：语文、数学、英语从左侧进入；科学、社政从右侧进入。
- 站位：17位老师形成三排弧线，前排为语1、数1、英1、科1、社1。
- 前移：唱到本组时，本组前排代表到前移线；组员原位轻拍或摆手。
- 发礼：语1、数1、英1、科1、社1下台发礼。
- 回台：左过道老师沿左线回台，右过道老师沿右线回台，英1从台口中线回台。
- Ending：五个花篮站台口前排，十二位老师在后方形成心愿花。

## 歌词卡分配

正式歌词按伴奏字幕逐句编号为 L1、L2、L3。图中已把歌词卡分配到组别、动作和口令：

| 歌词卡 | 演唱组 | 动作 |
| --- | --- | --- |
| L1-L2 | 语文组 | 语1前移，语2、语3轻拍 |
| L3-L4 | 数学组 | 数1前移，数2、数3轻拍 |
| L5-L7 | 英语组 | 英1前移，英2、英3、英4摆手 |
| L8-L10 | 科学组 | 科1前移，科2、科3、科4摆手 |
| L11-L12 | 社政组 | 社1前移，社2、社3轻拍 |
| L13-L16 | 全体合唱 | 三排弧线，小幅摆手 |
| L17-L21 | 五组轮唱 | 五组各接一句，对应前移 |
| L22-L25 | 全体合唱 | 五位发礼老师后侧取篮 |
| L26-L30 | 台上12人 | 台上继续唱，台下发礼互动 |
| L31 | 全体收尾 | 回台，组成心愿花定格 |
"""
    (OUT / "心愿便利贴_白底手绘分镜_v6_说明.md").write_text(md, encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    write_all()
