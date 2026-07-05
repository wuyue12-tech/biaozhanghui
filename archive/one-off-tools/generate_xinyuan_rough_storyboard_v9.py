from pathlib import Path
from xml.sax.saxutils import escape


OUT = Path("/Users/wuyue/Documents/自主管理学院/output/心愿便利贴_小黑电影分镜_v9")
OUT.mkdir(parents=True, exist_ok=True)

W, H = 2400, 1600

COL = {
    "语": "#ef4444",
    "数": "#2563eb",
    "英": "#16a34a",
    "科": "#d97706",
    "社": "#7c3aed",
    "助": "#111827",
    "学": "#64748b",
}


def e(text):
    return escape(str(text))


def start(title, subtitle=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <style>
      .bg {{ fill:#fffdf8; }}
      .title {{ font:700 48px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#111827; }}
      .sub {{ font:400 23px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#4b5563; }}
      .shot {{ font:700 26px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#111827; }}
      .cap {{ font:400 19px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#374151; }}
      .small {{ font:400 15px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#4b5563; }}
      .tiny {{ font:400 12px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#4b5563; }}
      .ink {{ fill:none; stroke:#111827; stroke-width:3.4; stroke-linecap:round; stroke-linejoin:round; }}
      .thin {{ fill:none; stroke:#111827; stroke-width:2.2; stroke-linecap:round; stroke-linejoin:round; }}
      .soft {{ fill:#f8fafc; stroke:#94a3b8; stroke-width:2.5; stroke-linecap:round; stroke-linejoin:round; }}
      .seat {{ fill:#e2e8f0; }}
      .stageFill {{ fill:#f8fafc; }}
      .aisleFill {{ fill:#fff7ed; }}
      .dash {{ fill:none; stroke:#94a3b8; stroke-width:2.4; stroke-dasharray:9 8; stroke-linecap:round; stroke-linejoin:round; }}
      .front {{ stroke:#f97316; stroke-width:6; stroke-linecap:round; }}
      .orange {{ fill:none; stroke:#f97316; stroke-width:6; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#ao); }}
      .blue {{ fill:none; stroke:#2563eb; stroke-width:5.5; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#ab); }}
      .return {{ fill:none; stroke:#2563eb; stroke-width:5.5; stroke-dasharray:13 9; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#ab); }}
      .green {{ fill:none; stroke:#16a34a; stroke-width:5.2; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#ag); }}
      .gift {{ fill:#fef3c7; stroke:#d97706; stroke-width:2; }}
      .basket {{ fill:#fff7ed; stroke:#ea580c; stroke-width:2.4; }}
    </style>
    <marker id="ao" markerWidth="17" markerHeight="17" refX="13" refY="8.5" orient="auto"><path d="M2,2 L15,8.5 L2,15 Z" fill="#f97316"/></marker>
    <marker id="ab" markerWidth="17" markerHeight="17" refX="13" refY="8.5" orient="auto"><path d="M2,2 L15,8.5 L2,15 Z" fill="#2563eb"/></marker>
    <marker id="ag" markerWidth="17" markerHeight="17" refX="13" refY="8.5" orient="auto"><path d="M2,2 L15,8.5 L2,15 Z" fill="#16a34a"/></marker>
  </defs>
  <rect width="{W}" height="{H}" class="bg"/>
  <text x="{W/2}" y="62" text-anchor="middle" class="title">{e(title)}</text>
  <text x="{W/2}" y="100" text-anchor="middle" class="sub">{e(subtitle)}</text>
'''


def end():
    return "</svg>\n"


def txt(x, y, t, cls="cap", anchor="start"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{e(t)}</text>\n'


def rough_rect(x, y, w, h, fill="none", cls="ink", r=12):
    # Two slightly offset outlines give the frame a storyboard sketch feel.
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" class="{cls}"/>\n'
    s += f'<path d="M{x+3},{y+1} C{x+w*.32},{y-3} {x+w*.7},{y+4} {x+w-2},{y+2} L{x+w+1},{y+h-4} C{x+w*.68},{y+h+4} {x+w*.24},{y+h-2} {x+2},{y+h+1} Z" fill="none" class="{cls}"/>\n'
    return s


def frame(x, y, w, h, no, title, caption):
    s = rough_rect(x, y, w, h, "#ffffff", "ink", 14)
    s += txt(x + 22, y + 38, f"镜头{no:02d}  {title}", "shot")
    s += f'<line x1="{x+18}" y1="{y+h-76}" x2="{x+w-18}" y2="{y+h-76}" class="thin"/>\n'
    s += txt(x + 24, y + h - 35, caption, "cap")
    return s


def slate(x, y, w, lines):
    s = rough_rect(x, y, w, 72 + len(lines) * 34, "#fff7ed", "thin", 12)
    for i, line in enumerate(lines):
        s += txt(x + 28, y + 42 + i * 34, line, "cap")
    return s


def xiaohei(x, y, tag="", group="", scale=1.0, basket=False, gift=False, arms="down"):
    color = COL.get(group, "#111827")
    sw = 3.2 * scale
    if arms == "open":
        arms_path = f'<line x1="0" y1="{3*scale}" x2="{-24*scale}" y2="{-13*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/><line x1="0" y1="{3*scale}" x2="{24*scale}" y2="{-13*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/>\n'
    elif arms == "basket":
        arms_path = f'<line x1="0" y1="{3*scale}" x2="{-25*scale}" y2="{18*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/><line x1="0" y1="{3*scale}" x2="{25*scale}" y2="{18*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/>\n'
    else:
        arms_path = f'<line x1="0" y1="{3*scale}" x2="{-18*scale}" y2="{15*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/><line x1="0" y1="{3*scale}" x2="{18*scale}" y2="{15*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/>\n'
    s = f'''
  <g transform="translate({x},{y})">
    <ellipse cx="0" cy="-18" rx="{18*scale}" ry="{27*scale}" fill="#111827"/>
    <circle cx="{-6*scale}" cy="{-20*scale}" r="{4.4*scale}" fill="#fff"/>
    <circle cx="{6*scale}" cy="{-20*scale}" r="{4.4*scale}" fill="#fff"/>
    {arms_path}
    <line x1="{-8*scale}" y1="{7*scale}" x2="{-16*scale}" y2="{35*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/>
    <line x1="{8*scale}" y1="{7*scale}" x2="{16*scale}" y2="{35*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/>
    <circle cx="0" cy="{-58*scale}" r="{13*scale}" fill="#fff" stroke="{color}" stroke-width="{3*scale}"/>
    <text x="0" y="{-53*scale}" text-anchor="middle" class="tiny" fill="{color}">{e(tag)}</text>
'''
    if basket:
        s += f'<path d="M{-29*scale},{17*scale} Q0,{-15*scale} {29*scale},{17*scale}" stroke="#ea580c" stroke-width="{2.5*scale}" fill="none"/><rect x="{-31*scale}" y="{17*scale}" width="{62*scale}" height="{39*scale}" rx="{8*scale}" class="basket"/>\n'
    if gift:
        s += f'<rect x="{19*scale}" y="{8*scale}" width="{23*scale}" height="{18*scale}" rx="{4*scale}" class="gift"/>\n'
    s += "  </g>\n"
    return s


def legend(y=124):
    s = ""
    for i, (lab, key) in enumerate([("语文3", "语"), ("数学3", "数"), ("英语4", "英"), ("科学4", "科"), ("社政3", "社")]):
        x = 305 + i * 325
        s += xiaohei(x, y, "", key, .45)
        s += txt(x + 35, y + 8, lab, "cap")
    s += txt(1970, y + 8, "共17人", "cap", "end")
    return s


def stage(x, y, w, h, label=True):
    s = rough_rect(x, y, w, h, "#f8fafc", "ink", 16)
    s += f'<line x1="{x+35}" y1="{y+h}" x2="{x+w-35}" y2="{y+h}" class="front"/>\n'
    if label:
        s += txt(x + w / 2, y + 46, "舞台", "shot", "middle")
        s += txt(x + w / 2, y + h + 34, "台口 / 面向观众", "cap", "middle")
    return s


def audience(x, y, scale=1.0, labels=True, dots=True):
    def sx(v): return x + v * scale
    def sy(v): return y + v * scale
    s = ""
    s += rough_rect(sx(0), sy(210), 310 * scale, 420 * scale, "#f8fafc", "soft", 12)
    s += rough_rect(sx(435), sy(170), 720 * scale, 500 * scale, "#f8fafc", "soft", 12)
    s += rough_rect(sx(1280), sy(210), 310 * scale, 420 * scale, "#f8fafc", "soft", 12)
    s += rough_rect(sx(330), sy(150), 75 * scale, 580 * scale, "#fff7ed", "aisle", 10)
    s += rough_rect(sx(1190), sy(150), 75 * scale, 580 * scale, "#fff7ed", "aisle", 10)
    if labels:
        s += txt(sx(155), sy(265), "左侧观众席", "shot", "middle")
        s += txt(sx(795), sy(230), "主观众席", "shot", "middle")
        s += txt(sx(1435), sy(265), "右侧观众席", "shot", "middle")
        s += txt(sx(368), sy(175), "左国道/过道", "cap", "middle")
        s += txt(sx(1228), sy(175), "右国道/过道", "cap", "middle")
    if dots:
        for r in range(5):
            yy = sy(315 + r * 68)
            for c in range(4):
                s += f'<circle cx="{sx(65+c*58)}" cy="{yy}" r="{8*scale}" class="seat"/>\n'
                s += f'<circle cx="{sx(1350+c*58)}" cy="{yy}" r="{8*scale}" class="seat"/>\n'
        for r in range(6):
            yy = sy(270 + r * 60)
            for c in range(9):
                s += f'<circle cx="{sx(505+c*68)}" cy="{yy}" r="{8*scale}" class="seat"/>\n'
    return s


def venue_scene(x, y, scale=1.0):
    s = stage(x + 360 * scale, y, 860 * scale, 125 * scale, True)
    s += audience(x, y + 155 * scale, scale, True, True)
    return s


def people_on_stage(x, y, w, h, scale=1.0):
    groups = [
        ("语", ["语1", "语2", "语3"], .16),
        ("数", ["数1", "数2", "数3"], .33),
        ("英", ["英1", "英2", "英3", "英4"], .52),
        ("科", ["科1", "科2", "科3", "科4"], .70),
        ("社", ["社1", "社2", "社3"], .86),
    ]
    s, pts = "", {}
    for key, labels, xr in groups:
        cx = x + w * xr
        for i, lab in enumerate(labels):
            local = i - (len(labels) - 1) / 2
            px = cx + local * 43 * scale
            py = y + h * ([.72, .53, .34, .39][min(i, 3)])
            pts[lab] = (px, py, key)
            s += xiaohei(px, py, lab, key, .72 * scale)
    return s, pts


def page_contact_sheet():
    s = start("《心愿便利贴》小黑电影分镜", "黑白分镜风格｜橙线行动，蓝线回台，绿线传礼") + legend()
    xs = [60, 830, 1600]
    ys = [175, 865]
    titles = [
        ("全景", "场地三块观众席，两条国道/过道"),
        ("上台", "语数英左侧，科社右侧"),
        ("前移", "唱到本组，代表到前移线"),
        ("取篮", "五位前排代表准备下台"),
        ("发礼", "五人下台，学生排头接礼"),
        ("定格", "五篮在前，后排心形"),
    ]
    for i, (t, c) in enumerate(titles):
        x, y = xs[i % 3], ys[i // 3]
        s += frame(x, y, 720, 620, i + 1, t, c)
        if i == 0:
            s += venue_scene(x + 65, y + 96, .36)
        elif i == 1:
            s += stage(x + 90, y + 105, 540, 190, False)
            p, _ = people_on_stage(x + 115, y + 135, 490, 150, .62)
            s += p
            s += f'<path d="M{x+95} {y+410} C{x+210} {y+330},{x+280} {y+265},{x+360} {y+230}" class="orange"/>\n'
            s += f'<path d="M{x+625} {y+410} C{x+510} {y+330},{x+440} {y+265},{x+360} {y+230}" class="orange"/>\n'
        elif i == 2:
            s += stage(x + 100, y + 120, 520, 220, False)
            s += f'<path d="M{x+150} {y+290} C{x+260} {y+235},{x+460} {y+235},{x+570} {y+290}" class="dash"/>\n'
            for j, key in enumerate(["语", "数", "英", "科", "社"]):
                xx = x + 165 + j * 105
                s += xiaohei(xx, y + 315, key, key, .56, arms="open")
                s += f'<path d="M{xx} {y+290} C{xx+5} {y+260},{xx+22} {y+225},{xx+48} {y+200}" class="orange"/>\n'
        elif i == 3:
            s += stage(x + 100, y + 120, 520, 220, False)
            for j, key in enumerate(["语", "数", "英", "科", "社"]):
                s += xiaohei(x + 170 + j * 95, y + 315, key, key, .58, basket=True, arms="basket")
        elif i == 4:
            s += audience(x + 62, y + 80, .36, False, False)
            s += f'<path d="M{x+260} {y+175} C{x+205} {y+260},{x+200} {y+370},{x+245} {y+500}" class="orange"/>\n'
            s += f'<path d="M{x+460} {y+175} C{x+515} {y+260},{x+520} {y+370},{x+475} {y+500}" class="orange"/>\n'
            s += f'<path d="M{x+360} {y+175} C{x+360} {y+280},{x+360} {y+390},{x+360} {y+500}" class="green"/>\n'
        else:
            s += stage(x + 100, y + 110, 520, 320, False)
            heart = f'M{x+245} {y+275} C{x+225} {y+190},{x+320} {y+175},{x+360} {y+245} C{x+410} {y+175},{x+500} {y+190},{x+485} {y+275} C{x+470} {y+360},{x+405} {y+385},{x+360} {y+420} C{x+315} {y+385},{x+260} {y+360},{x+245} {y+275}'
            s += f'<path d="{heart}" class="dash"/>\n'
            for j, key in enumerate(["语", "数", "英", "科", "社"]):
                s += xiaohei(x + 250 + j * 55, y + 395, key, key, .43, basket=True, arms="basket")
    return s + end()


def page_stage_move():
    s = start("镜头 01-03：上台、站位、前移", "每个老师先看自己从哪边上台，再看本组何时前移") + legend()
    s += frame(70, 175, 700, 560, 1, "左侧上台", "语文、数学、英语从左侧上台入口进入。")
    s += stage(145, 265, 550, 180, False)
    for j, key in enumerate(["语", "数", "英"]):
        s += xiaohei(200 + j * 80, 500 - j * 28, key, key, .64)
    s += '<path d="M165 610 C250 520,340 455,485 405" class="orange"/>\n'
    s += frame(850, 175, 700, 560, 2, "右侧上台", "科学、社政从右侧上台入口进入。")
    s += stage(925, 265, 550, 180, False)
    for j, key in enumerate(["科", "社"]):
        s += xiaohei(1400 - j * 90, 500 - j * 45, key, key, .64)
    s += '<path d="M1450 610 C1370 520,1280 455,1135 405" class="orange"/>\n'
    s += frame(1630, 175, 700, 560, 3, "三排弧线", "全体落位，台口朝三块观众席。")
    s += stage(1695, 260, 570, 240, False)
    s += '<path d="M1745 430 C1885 365,2075 365,2215 430" class="dash"/>\n'
    s += '<path d="M1775 355 C1910 305,2050 305,2185 355" class="dash"/>\n'
    p, _ = people_on_stage(1720, 285, 520, 185, .58)
    s += p
    s += frame(350, 825, 1700, 610, 4, "小组前移", "唱到本组时，前排代表到前移线；唱完回弧线。")
    s += stage(460, 925, 1480, 320, False)
    s += '<path d="M560 1170 C860 1100,1540 1100,1840 1170" class="dash"/>\n'
    p, pts = people_on_stage(560, 950, 1280, 240, .84)
    s += p
    front = [("语1", "语", 680, 1210), ("数1", "数", 930, 1175), ("英1", "英", 1200, 1155), ("科1", "科", 1470, 1175), ("社1", "社", 1720, 1210)]
    for lab, key, x2, y2 in front:
        x1, y1, _ = pts[lab]
        s += f'<path d="M{x1} {y1} C{(x1+x2)/2} {y1+80},{(x1+x2)/2} {y2-80},{x2} {y2}" class="orange"/>\n'
        s += xiaohei(x2, y2, lab, key, .58, arms="open")
    return s + end()


def page_gift_route():
    s = start("镜头 04-06：发礼物与回台", "五位代表下台；排头学生接礼并向内传；尾声按蓝线回台") + legend()
    s += frame(70, 175, 1040, 1120, 4, "全景动线", "橙线下台，绿线传礼，蓝色虚线回台。")
    s += stage(330, 265, 520, 145, False)
    s += audience(205, 455, .58, True, True)
    for j, (lab, key) in enumerate([("语1", "语"), ("数1", "数"), ("英1", "英"), ("科1", "科"), ("社1", "社")]):
        s += xiaohei(390 + j * 95, 435, lab, key, .50, basket=True, arms="basket")
    s += '<path d="M390 458 C320 535,300 650,300 870 C295 1010,245 1110,165 1180" class="orange"/>\n'
    s += '<path d="M485 458 C400 560,355 700,370 930 C380 1050,450 1125,530 1170" class="orange"/>\n'
    s += '<path d="M580 458 C580 610,580 790,580 1030" class="green"/>\n'
    s += '<path d="M675 458 C760 560,805 700,790 930 C780 1050,710 1125,630 1170" class="orange"/>\n'
    s += '<path d="M770 458 C840 535,860 650,860 870 C865 1010,915 1110,995 1180" class="orange"/>\n'
    s += '<path d="M165 1180 C285 1095,310 930,310 720 C310 590,345 500,390 445" class="return"/>\n'
    s += '<path d="M995 1180 C875 1095,850 930,850 720 C850 590,815 500,770 445" class="return"/>\n'
    for yy in [720, 835, 950, 1065]:
        s += f'<rect x="345" y="{yy}" width="28" height="20" rx="4" class="gift"/><path d="M373 {yy+10} C445 {yy-4},510 {yy-4},570 {yy+10}" class="green"/>\n'
        s += f'<rect x="815" y="{yy}" width="28" height="20" rx="4" class="gift"/><path d="M815 {yy+10} C745 {yy-4},675 {yy-4},605 {yy+10}" class="green"/>\n'
    for x, y in [(340, 665), (340, 910), (580, 650), (820, 665), (820, 910), (170, 980), (990, 980)]:
        s += xiaohei(x, y, "助", "助", .42, gift=True)
    s += frame(1180, 175, 1050, 520, 5, "分区发礼", "左侧、主观众席、右侧三个区域同步接礼。")
    s += audience(1260, 245, .50, True, False)
    s += txt(1325, 640, "语1", "shot", "middle") + txt(1500, 640, "数1", "shot", "middle")
    s += txt(1700, 640, "英1", "shot", "middle") + txt(1900, 640, "科1", "shot", "middle") + txt(2075, 640, "社1", "shot", "middle")
    s += frame(1180, 775, 1050, 520, 6, "回台接Ending", "尾声口令后，五人回到台口前排。")
    s += stage(1450, 870, 520, 155, False)
    for j, key in enumerate(["语", "数", "英", "科", "社"]):
        s += xiaohei(1515 + j * 85, 1115, key, key, .62, basket=True, arms="basket")
    s += '<path d="M1320 1190 C1460 1110,1510 1045,1540 990" class="return"/>\n'
    s += '<path d="M2140 1190 C2000 1110,1950 1045,1920 990" class="return"/>\n'
    return s + end()


def page_ending():
    s = start("镜头 07：Ending Pose 心愿花", "五篮在台口前排，后排十二位老师形成心形花瓣") + legend()
    s += frame(185, 175, 2030, 1120, 7, "最终定格", "前排五篮，后排心形；合唱最后一句，停两拍鞠躬。")
    s += stage(405, 295, 1580, 780, False)
    s += txt(1195, 1115, "台口 / 面向三块观众席", "shot", "middle")
    heart = "M760 730 C700 500,980 460,1180 650 C1380 460,1660 500,1600 730 C1560 910,1320 980,1190 1050 C1060 980,800 910,760 730"
    s += f'<path d="{heart}" class="dash"/>\n'
    back = [
        ("语2", "语", 845, 760), ("语3", "语", 900, 585),
        ("数2", "数", 1065, 530), ("数3", "数", 1150, 675),
        ("英2", "英", 1255, 675), ("英3", "英", 1345, 530), ("英4", "英", 1510, 590),
        ("科2", "科", 1570, 760), ("科3", "科", 1490, 910), ("科4", "科", 1335, 1000),
        ("社2", "社", 1035, 1000), ("社3", "社", 880, 910),
    ]
    front = [("语1", "语", 970, 1060), ("数1", "数", 1085, 1110), ("英1", "英", 1200, 1130), ("科1", "科", 1315, 1110), ("社1", "社", 1430, 1060)]
    for lab, key, x, y in back:
        s += xiaohei(x, y, lab, key, .80, arms="open")
    for lab, key, x, y in front:
        s += xiaohei(x, y, lab, key, .88, basket=True, arms="basket")
    s += slate(325, 1350, 1750, ["定格口令：前排五篮，后排花瓣，全体微笑合唱，停两拍鞠躬退场。"])
    return s + end()


def write_all():
    pages = [
        ("00_小黑电影分镜总览.svg", page_contact_sheet()),
        ("01_上台站位前移_电影分镜.svg", page_stage_move()),
        ("02_发礼回台_电影分镜.svg", page_gift_route()),
        ("03_EndingPose_电影分镜.svg", page_ending()),
    ]
    for name, body in pages:
        (OUT / name).write_text(body, encoding="utf-8")
    md = """# 《心愿便利贴》小黑电影分镜 v9

这一版改成电影分镜板风格：

- 黑白小黑人物为主，学科只用头顶小圆标识别。
- 每页使用镜头框和场记条，而不是PPT流程图表。
- 橙线表示上台/下台行动，绿线表示礼物向座位内传，蓝色虚线表示回台。
- 台下保留左侧观众席、主观众席、右侧观众席，以及主侧之间两条国道/过道。
"""
    (OUT / "心愿便利贴_小黑电影分镜_v9_说明.md").write_text(md, encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    write_all()
