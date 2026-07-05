from pathlib import Path
from xml.sax.saxutils import escape


OUT = Path("/Users/wuyue/Documents/自主管理学院/output/心愿便利贴_ian_xiaohei_skill_v10")
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1920, 1080

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


def svg_start():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <style>
      .bg {{ fill:#fff; }}
      .ink {{ fill:none; stroke:#111827; stroke-width:3; stroke-linecap:round; stroke-linejoin:round; }}
      .thin {{ fill:none; stroke:#111827; stroke-width:2; stroke-linecap:round; stroke-linejoin:round; }}
      .pale {{ fill:#f8fafc; stroke:#94a3b8; stroke-width:2; stroke-linecap:round; stroke-linejoin:round; }}
      .aisle {{ fill:none; stroke:#fb923c; stroke-width:2.6; stroke-dasharray:9 8; stroke-linecap:round; stroke-linejoin:round; }}
      .front {{ stroke:#f97316; stroke-width:5.5; stroke-linecap:round; }}
      .seat {{ fill:#cbd5e1; opacity:.78; }}
      .dash {{ fill:none; stroke:#94a3b8; stroke-width:2.2; stroke-dasharray:8 8; stroke-linecap:round; stroke-linejoin:round; }}
      .route {{ fill:none; stroke:#f97316; stroke-width:5.2; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#arrO); }}
      .blue {{ fill:none; stroke:#2563eb; stroke-width:4.8; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#arrB); }}
      .return {{ fill:none; stroke:#2563eb; stroke-width:4.8; stroke-dasharray:12 8; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#arrB); }}
      .pass {{ fill:none; stroke:#16a34a; stroke-width:4.6; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#arrG); }}
      .note {{ font:400 28px "Kaiti SC","STKaiti","PingFang SC","Microsoft YaHei",sans-serif; fill:#111827; }}
      .small {{ font:400 21px "Kaiti SC","STKaiti","PingFang SC","Microsoft YaHei",sans-serif; fill:#374151; }}
      .tiny {{ font:400 15px "PingFang SC","Microsoft YaHei",sans-serif; fill:#4b5563; }}
      .tag {{ font:700 16px "PingFang SC","Microsoft YaHei",sans-serif; }}
      .gift {{ fill:#fef3c7; stroke:#d97706; stroke-width:2; }}
      .basket {{ fill:#fff7ed; stroke:#ea580c; stroke-width:2.4; }}
    </style>
    <marker id="arrO" markerWidth="15" markerHeight="15" refX="12" refY="7.5" orient="auto"><path d="M2,2 L13,7.5 L2,13 Z" fill="#f97316"/></marker>
    <marker id="arrB" markerWidth="15" markerHeight="15" refX="12" refY="7.5" orient="auto"><path d="M2,2 L13,7.5 L2,13 Z" fill="#2563eb"/></marker>
    <marker id="arrG" markerWidth="15" markerHeight="15" refX="12" refY="7.5" orient="auto"><path d="M2,2 L13,7.5 L2,13 Z" fill="#16a34a"/></marker>
  </defs>
  <rect width="{W}" height="{H}" class="bg"/>
'''


def svg_end():
    return "</svg>\n"


def txt(x, y, value, cls="note", anchor="start", color=None):
    fill = f' fill="{color}"' if color else ""
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}"{fill}>{e(value)}</text>\n'


def rough_rect(x, y, w, h, cls="ink", fill="none", r=18):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" class="{cls}"/>\n'
        f'<path d="M{x+3},{y+2} C{x+w*.25},{y-3} {x+w*.73},{y+4} {x+w-2},{y+1} '
        f'L{x+w+1},{y+h-3} C{x+w*.67},{y+h+4} {x+w*.2},{y+h-2} {x+2},{y+h+1} Z" class="{cls}" fill="none"/>\n'
    )


def xiaohei(x, y, label="", group="", scale=1.0, basket=False, gift=False, arms="down"):
    color = COL.get(group, "#111827")
    sw = 3 * scale
    if arms == "open":
        arm = f'<line x1="0" y1="{3*scale}" x2="{-24*scale}" y2="{-12*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/><line x1="0" y1="{3*scale}" x2="{24*scale}" y2="{-12*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/>\n'
    elif arms == "carry":
        arm = f'<line x1="0" y1="{3*scale}" x2="{-24*scale}" y2="{18*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/><line x1="0" y1="{3*scale}" x2="{24*scale}" y2="{18*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/>\n'
    elif arms == "pull":
        arm = f'<line x1="0" y1="{2*scale}" x2="{32*scale}" y2="{-8*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/><line x1="0" y1="{2*scale}" x2="{-14*scale}" y2="{16*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/>\n'
    else:
        arm = f'<line x1="0" y1="{3*scale}" x2="{-17*scale}" y2="{15*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/><line x1="0" y1="{3*scale}" x2="{17*scale}" y2="{15*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/>\n'
    s = f'''
  <g transform="translate({x},{y})">
    <ellipse cx="0" cy="-18" rx="{18*scale}" ry="{28*scale}" fill="#111827"/>
    <circle cx="{-6*scale}" cy="{-21*scale}" r="{4.2*scale}" fill="#fff"/>
    <circle cx="{6*scale}" cy="{-20*scale}" r="{4.2*scale}" fill="#fff"/>
    {arm}
    <line x1="{-8*scale}" y1="{7*scale}" x2="{-17*scale}" y2="{36*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/>
    <line x1="{8*scale}" y1="{7*scale}" x2="{17*scale}" y2="{36*scale}" stroke="#111827" stroke-width="{sw}" stroke-linecap="round"/>
    <circle cx="0" cy="{-58*scale}" r="{13*scale}" fill="#fff" stroke="{color}" stroke-width="{3*scale}"/>
    <text x="0" y="{-53*scale}" text-anchor="middle" class="tag" fill="{color}">{e(label)}</text>
'''
    if basket:
        s += f'<path d="M{-28*scale},{18*scale} Q0,{-14*scale} {28*scale},{18*scale}" stroke="#ea580c" stroke-width="{2.4*scale}" fill="none"/><rect x="{-30*scale}" y="{18*scale}" width="{60*scale}" height="{38*scale}" rx="{8*scale}" class="basket"/>\n'
    if gift:
        s += f'<rect x="{20*scale}" y="{8*scale}" width="{22*scale}" height="{17*scale}" rx="{4*scale}" class="gift"/>\n'
    s += "  </g>\n"
    return s


def legend(x=116, y=72):
    s = ""
    for i, (name, key) in enumerate([("语文", "语"), ("数学", "数"), ("英语", "英"), ("科学", "科"), ("社政", "社")]):
        xx = x + i * 150
        s += xiaohei(xx, y, "", key, .38)
        s += txt(xx + 26, y + 8, name, "tiny")
    return s


def stage(x, y, w, h, label=True):
    s = rough_rect(x, y, w, h, "ink", "#f8fafc", 18)
    s += f'<line x1="{x+35}" y1="{y+h}" x2="{x+w-35}" y2="{y+h}" class="front"/>\n'
    if label:
        s += txt(x + w / 2, y + h / 2 + 8, "舞台", "note", "middle")
        s += txt(x + w / 2, y + h + 38, "台口", "small", "middle")
    return s


def audience(x, y, scale=1.0, labels=True, seats=True):
    def sx(v):
        return x + v * scale
    def sy(v):
        return y + v * scale

    s = ""
    s += rough_rect(sx(0), sy(165), 300 * scale, 390 * scale, "pale", "#f8fafc", 14)
    s += rough_rect(sx(430), sy(125), 700 * scale, 470 * scale, "pale", "#f8fafc", 14)
    s += rough_rect(sx(1260), sy(165), 300 * scale, 390 * scale, "pale", "#f8fafc", 14)
    s += rough_rect(sx(325), sy(105), 78 * scale, 545 * scale, "aisle", "none", 12)
    s += rough_rect(sx(1158), sy(105), 78 * scale, 545 * scale, "aisle", "none", 12)
    if labels:
        s += txt(sx(150), sy(215), "左侧观众", "small", "middle")
        s += txt(sx(780), sy(175), "主观众席", "small", "middle")
        s += txt(sx(1410), sy(215), "右侧观众", "small", "middle")
        s += txt(sx(364), sy(90), "左国道", "small", "middle")
        s += txt(sx(1197), sy(90), "右国道", "small", "middle")
    if seats:
        for r in range(5):
            yy = sy(270 + r * 58)
            for c in range(4):
                s += f'<circle cx="{sx(62+c*58)}" cy="{yy}" r="{8*scale}" class="seat"/>\n'
                s += f'<circle cx="{sx(1318+c*58)}" cy="{yy}" r="{8*scale}" class="seat"/>\n'
        for r in range(6):
            yy = sy(232 + r * 52)
            for c in range(9):
                s += f'<circle cx="{sx(500+c*62)}" cy="{yy}" r="{8*scale}" class="seat"/>\n'
    return s


def stage_people(x, y, w, h, scale=1.0):
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
            px = cx + local * 40 * scale
            if i == 0:
                py = y + h * .72
            elif i == 1:
                py = y + h * .53
            else:
                py = y + h * .34 + (i - 2) * 18 * scale
            pts[lab] = (px, py, key)
            s += xiaohei(px, py, lab, key, .68 * scale)
    return s, pts


def page_01_venue():
    s = svg_start() + legend()
    s += txt(1110, 70, "场地：三块观众，两条国道", "note", "middle")
    s += stage(560, 145, 800, 130)
    s += audience(185, 360, 1.0, True, True)
    s += '<path d="M724 300 C720 350,690 405,585 470" class="route"/>\n'
    s += '<path d="M1196 300 C1200 350,1230 405,1335 470" class="route"/>\n'
    s += '<path d="M960 315 C960 370,960 420,960 490" class="blue"/>\n'
    s += xiaohei(720, 345, "", "助", .72, arms="pull")
    s += xiaohei(1200, 345, "", "助", .72, arms="pull")
    s += txt(960, 980, "口令：舞台在前，台口朝观众。橙线走人，蓝线看观众。", "small", "middle")
    return s + svg_end()


def page_02_stage():
    s = svg_start() + legend()
    s += txt(1110, 70, "上台：拉成三排弧线", "note", "middle")
    x, y, w, h = 250, 170, 1420, 610
    s += stage(x, y, w, h, False)
    s += txt(x + w / 2, y + h + 38, "台口", "small", "middle")
    s += f'<path d="M{x+130} {y+430} C{x+460} {y+340},{x+960} {y+340},{x+1290} {y+430}" class="dash"/>\n'
    s += f'<path d="M{x+190} {y+310} C{x+520} {y+220},{x+900} {y+220},{x+1230} {y+310}" class="dash"/>\n'
    s += f'<path d="M{x+250} {y+200} C{x+560} {y+135},{x+860} {y+135},{x+1170} {y+200}" class="dash"/>\n'
    people, _ = stage_people(x + 135, y + 85, w - 270, h - 160, 1.05)
    s += people
    s += '<path d="M210 855 C380 720,470 635,620 585" class="route"/>\n'
    s += '<path d="M1710 855 C1540 720,1450 635,1300 585" class="route"/>\n'
    s += xiaohei(360, 725, "", "助", .8, arms="pull")
    s += xiaohei(1560, 725, "", "助", .8, arms="pull")
    s += txt(275, 900, "左侧：语 数 英", "small")
    s += txt(1645, 900, "右侧：科 社", "small", "end")
    return s + svg_end()


def page_03_forward():
    s = svg_start() + legend()
    s += txt(1110, 70, "轮唱：代表到前移线", "note", "middle")
    x, y, w, h = 250, 165, 1420, 625
    s += stage(x, y, w, h, False)
    s += txt(x + w / 2, y + h + 38, "台口", "small", "middle")
    people, pts = stage_people(x + 135, y + 85, w - 270, h - 165, 1.0)
    s += people
    fy = y + h - 92
    s += f'<path d="M{x+210} {fy} C{x+520} {fy-55},{x+900} {fy-55},{x+1210} {fy}" class="dash"/>\n'
    front = [
        ("语1", "语", x + 355, fy),
        ("数1", "数", x + 575, fy - 34),
        ("英1", "英", x + 710, fy - 52),
        ("科1", "科", x + 925, fy - 34),
        ("社1", "社", x + 1120, fy),
    ]
    for lab, key, x2, y2 in front:
        x1, y1, _ = pts[lab]
        s += f'<path d="M{x1} {y1+8} C{(x1+x2)/2} {y1+72},{(x1+x2)/2} {y2-72},{x2} {y2}" class="route"/>\n'
        s += xiaohei(x2, y2, lab, key, .62, arms="open")
    s += txt(960, 970, "口令：本组前移。唱完，回弧线。", "small", "middle")
    return s + svg_end()


def page_04_gift():
    s = svg_start() + legend()
    s += txt(1110, 70, "发礼：五人下台，礼物往里流", "note", "middle")
    s += stage(580, 130, 760, 125, False)
    s += txt(960, 207, "舞台", "small", "middle")
    s += audience(180, 330, 1.0, True, True)
    starts = [("语1", "语", 690), ("数1", "数", 820), ("英1", "英", 960), ("科1", "科", 1100), ("社1", "社", 1230)]
    for lab, key, xx in starts:
        s += xiaohei(xx, 300, lab, key, .55, basket=True, arms="carry")
    s += '<path d="M690 325 C575 430,520 575,520 770 C520 870,420 920,290 955" class="route"/>\n'
    s += '<path d="M820 325 C675 450,560 600,550 780 C545 890,650 940,770 965" class="route"/>\n'
    s += '<path d="M960 325 C960 450,960 600,960 835" class="pass"/>\n'
    s += '<path d="M1100 325 C1245 450,1360 600,1370 780 C1375 890,1270 940,1150 965" class="route"/>\n'
    s += '<path d="M1230 325 C1345 430,1400 575,1400 770 C1400 870,1500 920,1630 955" class="route"/>\n'
    for yy in [595, 705, 815]:
        s += f'<rect x="540" y="{yy}" width="30" height="22" rx="5" class="gift"/><path d="M570 {yy+11} C690 {yy-5},800 {yy-5},910 {yy+11}" class="pass"/>\n'
        s += f'<rect x="1350" y="{yy}" width="30" height="22" rx="5" class="gift"/><path d="M1350 {yy+11} C1230 {yy-5},1120 {yy-5},1010 {yy+11}" class="pass"/>\n'
    for xx, yy in [(520, 545), (520, 810), (960, 575), (1400, 545), (1400, 810), (320, 885), (1600, 885)]:
        s += xiaohei(xx, yy, "助", "助", .42, gift=True)
    s += txt(960, 1000, "橙线：老师走。绿线：学生向内传。", "small", "middle")
    return s + svg_end()


def page_05_ending():
    s = svg_start() + legend()
    s += txt(1110, 70, "回台：五篮在前，后排成心", "note", "middle")
    x, y, w, h = 285, 150, 1350, 690
    s += stage(x, y, w, h, False)
    heart = (
        "M650 555 C595 360,830 330,960 480 "
        "C1100 330,1335 360,1280 555 "
        "C1245 705,1050 760,960 820 "
        "C870 760,685 705,650 555"
    )
    s += f'<path d="{heart}" class="dash"/>\n'
    back = [
        ("语2", "语", 705, 580), ("语3", "语", 760, 430),
        ("数2", "数", 900, 388), ("数3", "数", 945, 520),
        ("英2", "英", 1015, 520), ("英3", "英", 1065, 388), ("英4", "英", 1210, 430),
        ("科2", "科", 1265, 580), ("科3", "科", 1195, 705), ("科4", "科", 1065, 785),
        ("社2", "社", 855, 785), ("社3", "社", 735, 705),
    ]
    front = [("语1", "语", 800, 830), ("数1", "数", 880, 868), ("英1", "英", 960, 888), ("科1", "科", 1040, 868), ("社1", "社", 1120, 830)]
    for lab, key, xx, yy in back:
        s += xiaohei(xx, yy, lab, key, .62, arms="open")
    for lab, key, xx, yy in front:
        s += xiaohei(xx, yy, lab, key, .70, basket=True, arms="carry")
    s += '<path d="M380 930 C520 855,645 835,800 830" class="return"/>\n'
    s += '<path d="M1540 930 C1400 855,1275 835,1120 830" class="return"/>\n'
    s += txt(960, 1000, "口令：前排五篮，后排花瓣，停两拍鞠躬。", "small", "middle")
    return s + svg_end()


def write_all():
    pages = [
        ("01_场地总览_ian小黑.svg", page_01_venue()),
        ("02_上台落位_ian小黑.svg", page_02_stage()),
        ("03_小组前移_ian小黑.svg", page_03_forward()),
        ("04_发礼物动线_ian小黑.svg", page_04_gift()),
        ("05_EndingPose_ian小黑.svg", page_05_ending()),
    ]
    for name, svg in pages:
        (OUT / name).write_text(svg, encoding="utf-8")
    md = """# 《心愿便利贴》Ian Xiaohei Skill 版 v10

按 `ian-xiaohei-illustrations` skill 的执行排练图模式生成：

- 16:9 横版，纯白背景。
- 黑色手绘线稿，大量留白。
- 小黑作为核心动作主体，不做装饰。
- 语文红、数学蓝、英语绿、科学橙、社政紫。
- 橙线为老师移动，绿线为礼物向座位内传，蓝色虚线为回台或面向观众。
- 每张只保留短口令，避免 PPT 流程图感。
"""
    (OUT / "心愿便利贴_ian小黑skill_v10_说明.md").write_text(md, encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    write_all()
