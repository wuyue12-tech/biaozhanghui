from pathlib import Path
from xml.sax.saxutils import escape


OUT = Path("/Users/wuyue/Documents/自主管理学院/output/心愿便利贴_小黑分镜_v5")
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1800, 1200

COL = {
    "语": "#ef4444",
    "数": "#2563eb",
    "英": "#16a34a",
    "科": "#d97706",
    "社": "#7c3aed",
    "学": "#64748b",
}


def svg_start(title, subtitle):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <style>
      .bg {{ fill:#fff; }}
      .title {{ font:700 46px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#111827; }}
      .sub {{ font:400 23px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#4b5563; }}
      .label {{ font:700 24px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#111827; }}
      .txt {{ font:400 20px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#374151; }}
      .small {{ font:400 16px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#4b5563; }}
      .tiny {{ font:400 13px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#4b5563; }}
      .thin {{ stroke:#111827; stroke-width:2.6; fill:none; stroke-linecap:round; stroke-linejoin:round; }}
      .soft {{ stroke:#94a3b8; stroke-width:2.4; fill:none; stroke-dasharray:8 8; stroke-linecap:round; }}
      .stage {{ fill:#f8fafc; stroke:#111827; stroke-width:3.2; }}
      .seat {{ fill:#f3f4f6; stroke:#9ca3af; stroke-width:2.3; }}
      .aisle {{ fill:#fff; stroke:#cbd5e1; stroke-width:2.2; stroke-dasharray:10 8; }}
      .orange {{ stroke:#f97316; stroke-width:5.5; fill:none; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#ao); }}
      .blue {{ stroke:#2563eb; stroke-width:5; fill:none; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#ab); }}
      .green {{ stroke:#16a34a; stroke-width:5; fill:none; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#ag); }}
      .front {{ stroke:#f97316; stroke-width:10; stroke-linecap:round; }}
      .note {{ fill:#fff7ed; stroke:#fb923c; stroke-width:2.4; }}
      .basket {{ fill:#fff7ed; stroke:#ea580c; stroke-width:2.5; }}
      .gift {{ fill:#fef3c7; stroke:#d97706; stroke-width:2; }}
    </style>
    <marker id="ao" markerWidth="14" markerHeight="14" refX="11" refY="7" orient="auto"><path d="M2,2 L12,7 L2,12 Z" fill="#f97316"/></marker>
    <marker id="ab" markerWidth="14" markerHeight="14" refX="11" refY="7" orient="auto"><path d="M2,2 L12,7 L2,12 Z" fill="#2563eb"/></marker>
    <marker id="ag" markerWidth="14" markerHeight="14" refX="11" refY="7" orient="auto"><path d="M2,2 L12,7 L2,12 Z" fill="#16a34a"/></marker>
  </defs>
  <rect width="{W}" height="{H}" class="bg"/>
  <text x="900" y="62" text-anchor="middle" class="title">{escape(title)}</text>
  <text x="900" y="100" text-anchor="middle" class="sub">{escape(subtitle)}</text>
'''


def svg_end():
    return "</svg>\n"


def xiaohei(x, y, tag="", group="", scale=1.0, face="front", basket=False, gift=False):
    c = COL.get(group, "#111827")
    rx, ry = 17 * scale, 25 * scale
    if face == "left":
        eye = [(-8, -8), (-8, 5)]
    elif face == "right":
        eye = [(8, -8), (8, 5)]
    else:
        eye = [(-6, -5), (6, -5)]
    s = f'''
  <g transform="translate({x},{y})">
    <ellipse cx="0" cy="-18" rx="{rx}" ry="{ry}" fill="#111827"/>
    <circle cx="{eye[0][0]*scale}" cy="{(-18+eye[0][1])*scale}" r="{4.2*scale}" fill="#fff"/>
    <circle cx="{eye[1][0]*scale}" cy="{(-18+eye[1][1])*scale}" r="{4.2*scale}" fill="#fff"/>
    <line x1="{-8*scale}" y1="{5*scale}" x2="{-15*scale}" y2="{34*scale}" stroke="#111827" stroke-width="{3*scale}" stroke-linecap="round"/>
    <line x1="{8*scale}" y1="{5*scale}" x2="{15*scale}" y2="{34*scale}" stroke="#111827" stroke-width="{3*scale}" stroke-linecap="round"/>
    <circle cx="0" cy="{-54*scale}" r="{12*scale}" fill="#fff" stroke="{c}" stroke-width="{3*scale}"/>
    <text x="0" y="{-50*scale}" text-anchor="middle" class="tiny" fill="{c}">{escape(tag)}</text>
'''
    if basket:
        s += f'''
    <path d="M{-32*scale},{-20*scale} Q{-8*scale},{-48*scale} {18*scale},{-20*scale}" stroke="#ea580c" stroke-width="{2.2*scale}" fill="none"/>
    <rect x="{-34*scale}" y="{-20*scale}" width="{54*scale}" height="{36*scale}" rx="{8*scale}" class="basket"/>
'''
    if gift:
        s += f'<rect x="{-34*scale}" y="{-28*scale}" width="{22*scale}" height="{17*scale}" rx="{3*scale}" class="gift"/>\n'
    s += "  </g>\n"
    return s


def flower(x, y, text="篮", scale=1.0):
    return f'''
  <g transform="translate({x},{y})">
    <path d="M{-30*scale},0 Q0,{-38*scale} {30*scale},0" stroke="#ea580c" stroke-width="{2.4*scale}" fill="none"/>
    <rect x="{-34*scale}" y="0" width="{68*scale}" height="{44*scale}" rx="{9*scale}" class="basket"/>
    <circle cx="{-18*scale}" cy="{1*scale}" r="{5*scale}" fill="#ef4444"/>
    <circle cx="0" cy="{-5*scale}" r="{5*scale}" fill="#f97316"/>
    <circle cx="{18*scale}" cy="{1*scale}" r="{5*scale}" fill="#16a34a"/>
    <text x="0" y="{31*scale}" text-anchor="middle" class="tiny">{escape(text)}</text>
  </g>'''


def stage(x=1270, y=210, w=330, h=660, title=True):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" class="stage"/><line x1="{x}" y1="{y+24}" x2="{x}" y2="{y+h-24}" class="front"/>\n'
    if title:
        s += f'<text x="{x+w/2}" y="{y+55}" text-anchor="middle" class="label">舞台</text><text x="{x-70}" y="{y+h/2}" text-anchor="middle" class="txt" fill="#f97316">台口</text>\n'
    return s


def seats():
    s = '<rect x="250" y="290" width="760" height="460" rx="20" class="seat"/><text x="630" y="335" text-anchor="middle" class="label">观众席</text>\n'
    for row in range(6):
        yy = 390 + row * 56
        for col in range(10):
            xx = 350 + col * 62
            s += f'<circle cx="{xx}" cy="{yy}" r="11" fill="#d1d5db"/>\n'
    s += '<rect x="170" y="170" width="1000" height="58" rx="15" class="aisle"/><text x="670" y="207" text-anchor="middle" class="txt">上过道</text>\n'
    s += '<rect x="170" y="815" width="1000" height="58" rx="15" class="aisle"/><text x="670" y="852" text-anchor="middle" class="txt">下过道</text>\n'
    return s


def legend(x=110, y=1080):
    items = [("语文3", "语"), ("数学3", "数"), ("英语4", "英"), ("科学4", "科"), ("社政3", "社")]
    s = ""
    for i, (txt, g) in enumerate(items):
        xx = x + i * 250
        s += f'<circle cx="{xx}" cy="{y}" r="15" fill="#fff" stroke="{COL[g]}" stroke-width="4"/><text x="{xx+30}" y="{y+7}" class="txt">{txt}</text>\n'
    return s


def stage_positions():
    return [
        (1360, 715, "语1", "语"), (1430, 670, "数1", "数"), (1500, 650, "英1", "英"), (1565, 680, "科1", "科"), (1595, 745, "社1", "社"),
        (1355, 545, "语2", "语"), (1420, 500, "数2", "数"), (1488, 485, "英2", "英"), (1548, 505, "英3", "英"), (1595, 570, "科2", "科"), (1610, 635, "社2", "社"),
        (1375, 375, "语3", "语"), (1445, 340, "数3", "数"), (1515, 330, "英4", "英"), (1575, 365, "科3", "科"), (1610, 430, "科4", "科"), (1620, 500, "社3", "社"),
    ]


def page1():
    s = svg_start("01 总平面与方向", "舞台在前方右侧，台口朝向观众席；两条过道用于发礼和回台")
    s += seats() + stage()
    for p in stage_positions():
        s += xiaohei(*p, scale=0.62, face="left")
    s += '<path d="M1165 200 C1235 225,1265 275,1270 345" class="orange"/><path d="M1165 845 C1235 815,1265 760,1270 705" class="orange"/>\n'
    s += '<path d="M1270 535 C1190 535,1120 535,1035 535" class="blue"/><text x="1165" y="518" text-anchor="middle" class="txt">演唱朝向</text>\n'
    s += '<text x="1160" y="150" text-anchor="middle" class="small">上台入口</text><text x="1160" y="930" text-anchor="middle" class="small">下台入口</text>\n'
    s += '<rect x="930" y="955" width="720" height="78" rx="16" class="note"/><text x="1290" y="1005" text-anchor="middle" class="txt">橙线：上台动线；蓝线：面向观众席演唱。</text>\n'
    s += legend()
    return s + svg_end()


def page2():
    s = svg_start("02 上台动线与站位", "两侧入口上台，17位老师落到三排弧线")
    s += stage(x=260, y=155, w=1080, h=820, title=False)
    s += '<text x="800" y="205" text-anchor="middle" class="label">舞台放大图：左侧橙线为台口</text><text x="205" y="570" text-anchor="middle" class="txt" fill="#f97316">台口</text>\n'
    s += '<path d="M500 790 C710 660,980 680,1160 800" class="soft"/><path d="M465 560 C710 435,1010 465,1195 620" class="soft"/><path d="M520 370 C760 260,1060 310,1220 480" class="soft"/>\n'
    # Scale stage positions into enlarged stage.
    for x, y, tag, g in stage_positions():
        sx = 260 + (x - 1270) * 2.55
        sy = 155 + (y - 210) * 1.0
        s += xiaohei(sx, sy, tag, g, scale=0.8, face="left")
    s += '<path d="M1680 270 C1515 300,1395 340,1240 415" class="orange"/><path d="M1680 850 C1515 785,1390 725,1240 650" class="orange"/>\n'
    s += '<rect x="1395" y="210" width="300" height="290" rx="18" class="note"/><text x="1545" y="260" text-anchor="middle" class="label">上台口令</text><text x="1545" y="320" text-anchor="middle" class="txt">上入口：语 数 英</text><text x="1545" y="370" text-anchor="middle" class="txt">下入口：科 社</text><text x="1545" y="420" text-anchor="middle" class="txt">落位：三排弧线</text>\n'
    s += legend(330, 1085)
    return s + svg_end()


def page3():
    s = svg_start("03 小组唱前移线", "唱到本组，本组向台口前移半步；唱完回到弧线")
    s += stage(x=260, y=155, w=1080, h=820, title=False)
    s += '<text x="205" y="570" text-anchor="middle" class="txt" fill="#f97316">台口</text>\n'
    # Front movement line near stage front.
    s += '<path d="M350 610 C570 490,950 505,1200 630" class="soft"/><text x="650" y="455" class="txt">前移线</text>\n'
    for x, y, tag, g in stage_positions():
        sx = 260 + (x - 1270) * 2.55
        sy = 155 + (y - 210) * 1.0
        s += xiaohei(sx, sy, tag, g, scale=0.78, face="left")
    # group arrows to the front line
    arrows = [(520, 745, 405, 660), (640, 690, 500, 610), (810, 670, 650, 565), (970, 690, 830, 590), (1090, 745, 1040, 655)]
    for x1, y1, x2, y2 in arrows:
        s += f'<path d="M{x1} {y1} C{x1-40} {y1-40}, {x2+60} {y2+20}, {x2} {y2}" class="orange"/>\n'
    s += '<rect x="1390" y="250" width="330" height="330" rx="18" class="note"/><text x="1555" y="305" text-anchor="middle" class="label">动作口令</text><text x="1555" y="365" text-anchor="middle" class="txt">本组前移</text><text x="1555" y="420" text-anchor="middle" class="txt">等待组轻拍</text><text x="1555" y="475" text-anchor="middle" class="txt">副歌整体摆手</text><text x="1555" y="530" text-anchor="middle" class="txt">弧线保持收紧</text>\n'
    s += legend(330, 1085)
    return s + svg_end()


def page4():
    s = svg_start("04 歌曲段落分镜", "前奏上台、主歌前移、副歌摆手、副歌2取篮、尾副歌发礼、尾声回台")
    panels = [
        (70, 160, "前奏", "上台"), (465, 160, "主歌", "前移"),
        (860, 160, "副歌", "摆手"), (1255, 160, "副歌2", "取篮"),
        (270, 650, "尾副歌", "发礼"), (850, 650, "尾声", "回台"),
    ]
    for x, y, title, note in panels:
        s += f'<rect x="{x}" y="{y}" width="345" height="350" rx="22" class="stage"/><text x="{x+28}" y="{y+45}" class="label">{title}</text><text x="{x+28}" y="{y+82}" class="txt">{note}</text>\n'
    s += stage(150, 275, 115, 150, False) + xiaohei(330, 330, "语", "语", .62, "left") + xiaohei(360, 370, "数", "数", .62, "left") + '<path d="M390 315 C330 310,285 320,250 345" class="orange"/>\n'
    s += stage(545, 275, 115, 150, False) + xiaohei(625, 350, "英", "英", .7, "left") + '<path d="M625 350 C585 350,555 350,520 350" class="orange"/>\n'
    s += stage(940, 275, 150, 150, False)
    for i, g in enumerate(["语", "数", "英", "科", "社"]):
        s += xiaohei(1002+i*26, 370-abs(i-2)*8, g, g, .5, "left")
    s += '<path d="M985 315 C1040 280,1110 300,1145 350" class="blue"/>\n'
    s += stage(1335, 275, 115, 150, False) + xiaohei(1410, 335, "科", "科", .62, "left", basket=True) + flower(1520, 330, "篮", .8) + '<path d="M1445 335 C1480 330,1505 330,1535 335" class="orange"/>\n'
    s += seats().replace('x="250"', 'x="340"', 1).replace('y="290"', 'y="775"', 1)
    s += '<rect x="640" y="760" width="55" height="215" rx="10" class="aisle"/>' + xiaohei(665, 830, "英", "英", .58, "down", basket=True) + xiaohei(665, 920, "数", "数", .58, "down", basket=True) + '<path d="M665 780 C665 840,665 895,665 960" class="orange"/>\n'
    s += stage(980, 760, 270, 220, False)
    for i, g in enumerate(["语", "数", "英", "科", "社"]):
        s += xiaohei(1070+i*38, 905-abs(i-2)*16, g, g, .55, "left", basket=(i in [0, 2, 4]))
    s += '<path d="M1035 925 C1105 850,1210 850,1270 925" class="blue"/>\n'
    s += '<rect x="1335" y="745" width="300" height="255" rx="18" class="note"/><text x="1485" y="795" text-anchor="middle" class="label">段落口令</text><text x="1485" y="850" text-anchor="middle" class="txt">前奏上台</text><text x="1485" y="900" text-anchor="middle" class="txt">副歌2取篮</text><text x="1485" y="950" text-anchor="middle" class="txt">尾声回台</text>\n'
    return s + svg_end()


def page5():
    s = svg_start("05 发礼物动线", "每组前排代表下台发礼；学生在排头接礼并向内传")
    s += seats() + stage()
    # singers remain on stage
    for x, y, tag, g in stage_positions()[5:]:
        s += xiaohei(x, y, tag, g, scale=0.5, face="left")
    # five gift teachers route
    top = [(1190, 195, "语1", "语"), (965, 195, "数1", "数")]
    bottom = [(1190, 845, "科1", "科"), (965, 845, "社1", "社")]
    middle = [(1050, 520, "英1", "英")]
    for p in top:
        s += xiaohei(*p, scale=.72, face="left", basket=True)
    for p in bottom:
        s += xiaohei(*p, scale=.72, face="left", basket=True)
    for p in middle:
        s += xiaohei(*p, scale=.72, face="left", basket=True)
    s += '<path d="M1270 330 C1180 250,1050 200,900 198 C760 195,610 195,440 220" class="orange"/>\n'
    s += '<path d="M1270 725 C1180 810,1050 845,900 850 C760 855,610 850,440 820" class="orange"/>\n'
    s += '<path d="M1270 535 C1195 535,1120 530,1030 520 C930 510,850 510,760 520" class="orange"/>\n'
    # gifts passed inward
    for yy in [395, 455, 515, 575, 635, 695]:
        s += f'<rect x="1015" y="{yy}" width="28" height="22" rx="4" class="gift"/><path d="M1015 {yy+10} C930 {yy},860 {yy},780 {yy+10}" class="green"/>\n'
        s += f'<rect x="455" y="{yy}" width="28" height="22" rx="4" class="gift"/><path d="M483 {yy+10} C560 {yy},630 {yy},710 {yy+10}" class="green"/>\n'
    for x, y in [(420, 250), (1035, 250), (420, 820), (1035, 820), (500, 540), (1010, 540)]:
        s += xiaohei(x, y, "学", "学", scale=.52, face="front", gift=True)
    s += '<rect x="930" y="955" width="720" height="78" rx="16" class="note"/><text x="1290" y="1005" text-anchor="middle" class="txt">语1、数1走上过道；科1、社1走下过道；英1走中线交接。</text>\n'
    return s + svg_end()


def page6():
    s = svg_start("06 Ending Pose：心愿花", "五个花篮在台口，十二位老师在后方形成花瓣弧线")
    s += stage(x=260, y=155, w=1120, h=830, title=False)
    s += '<text x="205" y="570" text-anchor="middle" class="txt" fill="#f97316">台口</text><path d="M520 535 C480 350,700 285,850 440 C1010 285,1230 350,1180 535 C1140 715,955 780,850 850 C745 780,560 715,520 535" class="soft"/>\n'
    back = [(590, 475, "语2", "语"), (655, 385, "语3", "语"), (770, 345, "数2", "数"), (845, 415, "数3", "数"), (920, 415, "英2", "英"), (1000, 345, "英3", "英"), (1110, 390, "英4", "英"), (1170, 485, "科2", "科"), (1110, 625, "科3", "科"), (990, 720, "科4", "科"), (710, 720, "社2", "社"), (590, 625, "社3", "社")]
    front = [(650, 805, "语1", "语"), (750, 850, "数1", "数"), (850, 870, "英1", "英"), (950, 850, "科1", "科"), (1050, 805, "社1", "社")]
    for p in back:
        s += xiaohei(*p, scale=.72, face="left")
    for p in front:
        s += xiaohei(*p, scale=.82, face="left", basket=True)
    s += '<rect x="1430" y="260" width="300" height="340" rx="18" class="note"/><text x="1580" y="315" text-anchor="middle" class="label">定格口令</text><text x="1580" y="375" text-anchor="middle" class="txt">前排五篮</text><text x="1580" y="430" text-anchor="middle" class="txt">后排花瓣</text><text x="1580" y="485" text-anchor="middle" class="txt">全体合唱</text><text x="1580" y="540" text-anchor="middle" class="txt">停两拍鞠躬</text>\n'
    s += legend(400, 1080)
    return s + svg_end()


def write_all():
    pages = [
        ("01_总平面与方向.svg", page1()),
        ("02_上台动线与站位.svg", page2()),
        ("03_小组唱前移线.svg", page3()),
        ("04_歌曲段落分镜.svg", page4()),
        ("05_发礼物动线.svg", page5()),
        ("06_EndingPose_心愿花.svg", page6()),
    ]
    for name, data in pages:
        (OUT / name).write_text(data, encoding="utf-8")
    md = """# 《心愿便利贴》Ian 小黑简笔分镜 v5

## 图纸

1. 总平面与方向
2. 上台动线与站位
3. 小组唱前移线
4. 歌曲段落分镜
5. 发礼物动线
6. Ending Pose：心愿花

## 执行设定

- 每组前排代表下台发礼：语1、数1、英1、科1、社1。
- 其余老师留台合唱。
- 发礼路线按上过道、下过道、中线交接组织。
- 回台后摆“心愿花”：五个花篮在台口，后排十二人形成花瓣弧线。
"""
    (OUT / "心愿便利贴_Ian小黑分镜_v5_说明.md").write_text(md, encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    write_all()
