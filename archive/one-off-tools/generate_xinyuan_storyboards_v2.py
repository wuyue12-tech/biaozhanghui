from pathlib import Path
from xml.sax.saxutils import escape


OUT = Path("/Users/wuyue/Documents/自主管理学院/output/心愿便利贴_报告厅分镜_v3")
OUT.mkdir(parents=True, exist_ok=True)


COLORS = {
    "语": ("#fee2e2", "#dc2626"),
    "数": ("#dbeafe", "#2563eb"),
    "英": ("#dcfce7", "#16a34a"),
    "科": ("#fef3c7", "#d97706"),
    "社": ("#ede9fe", "#7c3aed"),
    "学生": ("#f8fafc", "#111827"),
}


def base(title, subtitle=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1200" viewBox="0 0 1800 1200">
  <defs>
    <style>
      .bg {{ fill:#fffdf8; }}
      .title {{ font:700 46px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#111827; }}
      .subtitle {{ font:400 24px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#4b5563; }}
      .h1 {{ font:700 30px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#111827; }}
      .h2 {{ font:700 23px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#111827; }}
      .txt {{ font:400 20px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#374151; }}
      .small {{ font:400 17px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#4b5563; }}
      .tiny {{ font:400 14px "PingFang SC","Microsoft YaHei",Arial,sans-serif; fill:#4b5563; }}
      .stage {{ fill:#f8fafc; stroke:#64748b; stroke-width:3; }}
      .aud {{ fill:#f3f4f6; stroke:#9ca3af; stroke-width:2.5; }}
      .aisle {{ fill:#ffffff; stroke:#cbd5e1; stroke-width:2; stroke-dasharray:10 8; }}
      .panel {{ fill:#ffffff; stroke:#111827; stroke-width:3; rx:18; }}
      .card {{ fill:#ffffff; stroke:#cbd5e1; stroke-width:2.5; rx:14; }}
      .warn {{ fill:#fff7ed; stroke:#fb923c; stroke-width:2.5; rx:14; }}
      .line {{ stroke:#111827; stroke-width:3; stroke-linecap:round; fill:none; }}
      .soft {{ stroke:#94a3b8; stroke-width:2.5; stroke-dasharray:7 7; fill:none; }}
      .arrowR {{ stroke:#ef4444; stroke-width:5; stroke-linecap:round; stroke-linejoin:round; fill:none; marker-end:url(#arrR); }}
      .arrowB {{ stroke:#2563eb; stroke-width:5; stroke-linecap:round; stroke-linejoin:round; fill:none; marker-end:url(#arrB); }}
      .arrowG {{ stroke:#16a34a; stroke-width:5; stroke-linecap:round; stroke-linejoin:round; fill:none; marker-end:url(#arrG); }}
      .basket {{ fill:#fff7ed; stroke:#ea580c; stroke-width:3; }}
      .postit {{ fill:#fef08a; stroke:#ca8a04; stroke-width:2; }}
    </style>
    <marker id="arrR" markerWidth="14" markerHeight="14" refX="11" refY="7" orient="auto"><path d="M2,2 L12,7 L2,12 Z" fill="#ef4444"/></marker>
    <marker id="arrB" markerWidth="14" markerHeight="14" refX="11" refY="7" orient="auto"><path d="M2,2 L12,7 L2,12 Z" fill="#2563eb"/></marker>
    <marker id="arrG" markerWidth="14" markerHeight="14" refX="11" refY="7" orient="auto"><path d="M2,2 L12,7 L2,12 Z" fill="#16a34a"/></marker>
  </defs>
  <rect width="1800" height="1200" class="bg"/>
  <text x="900" y="62" text-anchor="middle" class="title">{escape(title)}</text>
  <text x="900" y="100" text-anchor="middle" class="subtitle">{escape(subtitle)}</text>
'''


def end():
    return "</svg>\n"


def person(x, y, label, key, scale=1.0):
    fill, stroke = COLORS[key]
    r = 20 * scale
    return f'''
  <g transform="translate({x},{y})">
    <circle cx="0" cy="-34" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>
    <line x1="0" y1="-14" x2="0" y2="30" class="line"/>
    <line x1="-26" y1="3" x2="26" y2="3" class="line"/>
    <line x1="0" y1="30" x2="-22" y2="64" class="line"/>
    <line x1="0" y1="30" x2="22" y2="64" class="line"/>
    <text x="0" y="-26" text-anchor="middle" class="h2" font-size="{20*scale}">{escape(label)}</text>
  </g>'''


def basket(x, y, label):
    return f'''
  <g transform="translate({x},{y})">
    <path d="M0,24 Q36,-20 72,24" class="line"/>
    <rect x="6" y="20" width="60" height="44" rx="10" class="basket"/>
    <text x="36" y="50" text-anchor="middle" class="tiny">{escape(label)}</text>
  </g>'''


def legend(x=70, y=118):
    items = [("语文3", "语"), ("数学3", "数"), ("英语4", "英"), ("科学4", "科"), ("社政3", "社")]
    s = ""
    for i, (label, key) in enumerate(items):
        fill, stroke = COLORS[key]
        xx = x + i * 270
        s += f'<rect x="{xx}" y="{y}" width="220" height="54" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/><text x="{xx+110}" y="{y+36}" text-anchor="middle" class="txt">{label}</text>\n'
    return s


def write_svg(name, body):
    path = OUT / name
    path.write_text(body, encoding="utf-8")
    return path


def page1():
    s = base("01 舞台站位与上台", "台上17人采用三排合唱弧线；两侧上台；老师道具集中在花篮发礼段") + legend()
    s += '''
  <rect x="95" y="205" width="1180" height="610" rx="18" class="stage"/>
  <text x="685" y="245" text-anchor="middle" class="h1">舞台 / 报告厅前方</text>
  <rect x="1340" y="205" width="360" height="610" rx="18" class="panel"/>
  <text x="1370" y="250" class="h1">动作规则</text>
  <text x="1370" y="300" class="txt">前奏：两侧上台，进入弧线。</text>
  <text x="1370" y="340" class="txt">小组唱：本组前排代表向前半步。</text>
  <text x="1370" y="380" class="txt">等待组：空手轻拍或小幅摆手。</text>
  <text x="1370" y="420" class="txt">全体唱：保持三排弧线，形成合唱感。</text>
  <text x="1370" y="460" class="txt">老师道具集中在花篮发礼段。</text>
  <rect x="1370" y="520" width="290" height="125" rx="14" class="warn"/>
  <text x="1515" y="565" text-anchor="middle" class="txt">舞台口诀</text>
  <text x="1515" y="605" text-anchor="middle" class="h2">三排弧线</text>
  <text x="1515" y="635" text-anchor="middle" class="h2">唱到谁谁动</text>
'''
    s += '''
  <path d="M360 675 C520 600,860 600,1030 675" class="soft"/>
  <path d="M315 525 C510 430,875 430,1065 525" class="soft"/>
  <path d="M350 380 C535 295,900 300,1090 395" class="soft"/>
  <text x="685" y="292" text-anchor="middle" class="small">三排合唱弧线：左右收紧，中间略前，整体聚拢。</text>
'''
    # front/mid/back arc rows
    positions = [
        (390, 675, "语1", "语"), (535, 640, "数1", "数"), (685, 625, "英1", "英"), (835, 640, "科1", "科"), (980, 675, "社1", "社"),
        (345, 525, "语2", "语"), (485, 500, "数2", "数"), (625, 488, "英2", "英"), (745, 488, "英3", "英"), (885, 500, "科2", "科"), (1025, 525, "社2", "社"),
        (380, 382, "语3", "语"), (535, 350, "数3", "数"), (685, 338, "英4", "英"), (835, 350, "科3", "科"), (940, 365, "科4", "科"), (1090, 392, "社3", "社"),
    ]
    for p in positions:
        s += person(*p, scale=0.85)
    s += '''
  <path d="M70 470 C110 455,130 450,165 455" class="arrowB"/>
  <path d="M1295 470 C1255 455,1235 450,1200 455" class="arrowB"/>
  <text x="150" y="805" class="small">左侧上台：语文、数学、英语，按弧线落位</text>
  <text x="850" y="805" class="small">右侧上台：科学、社政，按弧线落位</text>
  <rect x="190" y="870" width="420" height="145" rx="18" class="aud"/>
  <rect x="710" y="870" width="420" height="145" rx="18" class="aud"/>
  <rect x="1230" y="870" width="420" height="145" rx="18" class="aud"/>
  <rect x="630" y="850" width="55" height="185" rx="8" class="aisle"/><text x="657" y="1055" text-anchor="middle" class="small">过道A</text>
  <rect x="1150" y="850" width="55" height="185" rx="8" class="aisle"/><text x="1177" y="1055" text-anchor="middle" class="small">过道B</text>
  <text x="900" y="1095" text-anchor="middle" class="txt">观众席：两条过道，分成左区 / 中区 / 右区</text>
'''
    return s + end()


def timeline_box(x, y, w, h, t, sec, action, color="#ffffff"):
    return f'''
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{color}" stroke="#111827" stroke-width="2.5"/>
  <text x="{x+22}" y="{y+38}" class="h2">{escape(t)}</text>
  <text x="{x+22}" y="{y+72}" class="small">{escape(sec)}</text>
  <text x="{x+22}" y="{y+112}" class="txt">{escape(action)}</text>
'''


def page2():
    s = base("02 动作、走位和歌曲段落对应", "按常见4:15版本排；排练时以实际伴奏字幕为准微调") + legend()
    boxes = [
        ("前奏", "0:00-0:16", "两侧上台，三排弧线，空手上场", "#f8fafc"),
        ("第一段主歌A", "约0:16-0:45", "语文、数学轮唱；唱到本组前半步", "#fff1f2"),
        ("第一段主歌B", "约0:45-1:10", "英语、科学轮唱；本组前半步", "#ecfdf5"),
        ("副歌1", "约1:10-1:40", "社政接入，全体合唱；空手小幅摆手", "#fefce8"),
        ("第二段主歌", "约1:40-2:25", "五组按语、数、英、科、社各接一句", "#ffffff"),
        ("副歌2", "约2:25-3:05", "全体合唱；5名发礼老师退到侧台取篮", "#eef2ff"),
        ("尾副歌", "约3:05-3:55", "台上12人继续唱；5名老师走过道发礼", "#fff7ed"),
        ("尾声", "约3:55-4:15", "听口令回台；最后一句定格、鞠躬", "#f8fafc"),
    ]
    x0, y0, w, h = 90, 210, 395, 170
    for i, item in enumerate(boxes):
        x = x0 + (i % 4) * 430
        y = y0 + (i // 4) * 245
        s += timeline_box(x, y, w, h, *item)
        if i < 7:
            if i % 4 != 3:
                s += f'<path d="M{x+w+10} {y+85} L{x+w+45} {y+85}" class="arrowG"/>\n'
    s += '''
  <rect x="90" y="735" width="1620" height="250" rx="18" class="panel"/>
  <text x="120" y="780" class="h1">舞台动作写法</text>
  <text x="120" y="832" class="txt">1. 小组唱：本组前排代表向前半步，后排保持错位；唱完退回。</text>
  <text x="120" y="878" class="txt">2. 全体合唱：五组站成三排浅弧线，空手从胸前向外小幅摆手，两拍一次。</text>
  <text x="120" y="924" class="txt">3. 取花篮：副歌2尾部启动，拿篮老师从本组后侧退到侧台，沿侧边移动。</text>
  <text x="120" y="970" class="txt">4. 发礼时：台上老师继续唱，台下老师沿过道发给排头，靠通道行进。</text>
  <rect x="1320" y="800" width="320" height="120" rx="16" class="warn"/>
  <text x="1480" y="848" text-anchor="middle" class="h2">排练口令</text>
  <text x="1480" y="888" text-anchor="middle" class="txt">前奏上台 / 副歌取篮 / 尾声回台</text>
'''
    return s + end()


def page3():
    s = base("03 两条过道发礼路线", "发礼是观众互动；老师发给排头，学生往里传")
    s += '''
  <rect x="130" y="150" width="1540" height="170" rx="18" class="stage"/>
  <text x="900" y="205" text-anchor="middle" class="h1">舞台</text>
  <text x="900" y="260" text-anchor="middle" class="txt">台上保留12人继续唱；5名发礼老师从两侧下台</text>
  <rect x="140" y="390" width="390" height="430" rx="18" class="aud"/><text x="335" y="430" text-anchor="middle" class="h2">左区</text>
  <rect x="705" y="390" width="390" height="430" rx="18" class="aud"/><text x="900" y="430" text-anchor="middle" class="h2">中区</text>
  <rect x="1270" y="390" width="390" height="430" rx="18" class="aud"/><text x="1465" y="430" text-anchor="middle" class="h2">右区</text>
  <rect x="570" y="360" width="80" height="500" rx="12" class="aisle"/><text x="610" y="835" text-anchor="middle" class="h2">过道A</text>
  <rect x="1150" y="360" width="80" height="500" rx="12" class="aisle"/><text x="1190" y="835" text-anchor="middle" class="h2">过道B</text>
  <path d="M420 305 C510 350,590 430,610 700" class="arrowR"/>
  <path d="M760 305 C685 360,615 470,610 760" class="arrowR"/>
  <path d="M1020 305 C1095 360,1170 470,1190 760" class="arrowB"/>
  <path d="M1380 305 C1285 360,1210 450,1190 700" class="arrowB"/>
  <path d="M900 305 C790 380,710 520,610 650" class="arrowG"/>
  <path d="M900 305 C1010 380,1090 520,1190 650" class="arrowG"/>
'''
    # baskets labels
    for item in [(350, 320, "语文篮"), (710, 320, "数学篮"), (860, 320, "英语左"), (960, 320, "英语右"), (1060, 320, "科学篮"), (1410, 320, "社政篮")]:
        s += basket(*item)
    s += '''
  <rect x="150" y="875" width="1520" height="190" rx="18" class="panel"/>
  <text x="185" y="920" class="h1">路线分配</text>
  <text x="185" y="970" class="txt">过道A：语文篮、数学篮、英语左，发左区和中区左半。</text>
  <text x="185" y="1018" class="txt">过道B：科学篮、社政篮、英语右，发右区和中区右半。</text>
  <text x="185" y="1060" class="txt">英语4人拆成左右两小篮，沿两条过道发礼；5个花篮版本可提前把英语礼物分成左右两袋。</text>
  <rect x="1240" y="925" width="360" height="92" rx="14" class="warn"/>
  <text x="1420" y="962" text-anchor="middle" class="h2">回台线</text>
  <text x="1420" y="997" text-anchor="middle" class="txt">尾声前20秒，立刻回台</text>
'''
    return s + end()


def page4():
    s = base("04 Ending 与学生后勤", "ending收回舞台；学生负责递、引、传、收")
    s += '''
  <rect x="100" y="165" width="980" height="520" rx="18" class="stage"/>
  <text x="590" y="215" text-anchor="middle" class="h1">尾声回台后的定格</text>
  <path d="M250 550 C430 420,750 420,930 550" class="soft"/>
'''
    final_positions = [
        (330, 550, "语1", "语"), (465, 520, "数1", "数"), (590, 500, "英1", "英"), (715, 520, "科1", "科"), (850, 550, "社1", "社"),
        (300, 405, "语2", "语"), (430, 380, "数2", "数"), (545, 365, "英2", "英"), (635, 365, "英3", "英"), (750, 380, "科2", "科"), (880, 405, "社2", "社"),
        (335, 285, "语3", "语"), (470, 270, "数3", "数"), (590, 255, "英4", "英"), (710, 270, "科3", "科"), (800, 285, "科4", "科"), (930, 310, "社3", "社"),
    ]
    for p in final_positions:
        s += person(*p, scale=0.72)
    s += '''
  <text x="590" y="640" text-anchor="middle" class="txt">最后一句：全体唱，前排5人向前半步；空手定格微笑</text>
  <rect x="1130" y="165" width="570" height="520" rx="18" class="panel"/>
  <text x="1170" y="220" class="h1">Ending顺序</text>
  <text x="1170" y="280" class="txt">1. 尾声前20秒：学生口令“回台”。</text>
  <text x="1170" y="335" class="txt">2. 发礼老师回到侧台，花篮交侧台学生。</text>
  <text x="1170" y="390" class="txt">3. 老师回三排，站回弧线，保持歌曲收束。</text>
  <text x="1170" y="445" class="txt">4. 最后一句全体唱，空手定格2秒。</text>
  <text x="1170" y="500" class="txt">5. 鞠躬，主持人接“谢谢老师们”。</text>
  <rect x="1190" y="555" width="440" height="80" rx="14" class="warn"/>
  <text x="1410" y="605" text-anchor="middle" class="h2">结尾保持简洁，唱完就收。</text>
  <rect x="100" y="755" width="1600" height="290" rx="18" class="panel"/>
  <text x="140" y="805" class="h1">学生后勤</text>
  <rect x="145" y="845" width="250" height="120" rx="14" class="card"/><text x="270" y="895" text-anchor="middle" class="txt">音控 / 歌词字幕</text><text x="270" y="930" text-anchor="middle" class="h2">2人</text>
  <rect x="430" y="845" width="250" height="120" rx="14" class="card"/><text x="555" y="885" text-anchor="middle" class="txt">两侧递篮/收篮</text><text x="555" y="922" text-anchor="middle" class="h2">2人</text><text x="555" y="950" text-anchor="middle" class="small">左1右1</text>
  <rect x="715" y="845" width="250" height="120" rx="14" class="card"/><text x="840" y="885" text-anchor="middle" class="txt">过道引导</text><text x="840" y="922" text-anchor="middle" class="h2">4人</text><text x="840" y="950" text-anchor="middle" class="small">保持通道顺畅</text>
  <rect x="1000" y="845" width="250" height="120" rx="14" class="card"/><text x="1125" y="885" text-anchor="middle" class="txt">礼物传递协助</text><text x="1125" y="922" text-anchor="middle" class="h2">6人</text><text x="1125" y="950" text-anchor="middle" class="small">三区排头传递</text>
  <rect x="1285" y="845" width="250" height="120" rx="14" class="card"/><text x="1410" y="895" text-anchor="middle" class="txt">摄影录像</text><text x="1410" y="930" text-anchor="middle" class="h2">1-2人</text>
  <rect x="1570" y="845" width="95" height="120" rx="14" class="warn"/><text x="1617" y="895" text-anchor="middle" class="txt">口令</text><text x="1617" y="930" text-anchor="middle" class="h2">回台</text>
'''
    return s + end()


def write_markdown():
    md = """# 《心愿便利贴》报告厅节目执行说明 v2

## 核心调整

1. 台上17人采用三排合唱弧线，整体收紧。
2. 报告厅按两条过道组织发礼，观众区分为左区、中区、右区。
3. 分镜拆成四张图：站位、歌曲动作、发礼路线、ending后勤。
4. 动作跟歌曲段落对应，按段落移动。

## 演员站位

- 前排：语1、数1、英1、科1、社1，站成浅弧线。
- 中排：语2、数2、英2、英3、科2、社2，比前排略宽。
- 后排：语3、数3、英4、科3、科4、社3，比中排略宽。

## 歌曲段落对应

| 歌曲段落 | 动作与走位 |
|---|---|
| 前奏 | 两侧上台，进入三排弧线，空手上场。 |
| 第一段主歌A | 语文、数学轮唱；唱到本组，本组向前半步。 |
| 第一段主歌B | 英语、科学轮唱；本组向前半步，其他组原地轻拍。 |
| 副歌1 | 社政接入，全体合唱；空手小幅摆手，两拍一次。 |
| 第二段主歌 | 五组轮唱，每组一句；本组位置完成演唱。 |
| 副歌2 | 全体合唱；5名发礼老师退到侧台取花篮。 |
| 尾副歌 | 台上12人继续唱；发礼老师沿两条过道发给排头。 |
| 尾声 | 听口令回台；最后一句全体唱，空手定格2秒，鞠躬。 |

## 发礼规则

- 过道A：语文篮、数学篮、英语左。
- 过道B：科学篮、社政篮、英语右。
- 英语组4人拆成左右两小篮，沿两条过道发礼。
- 老师发给每排排头，礼物由学生和排头往里传。
- 尾声前20秒回台，原路回台。

## 学生后勤

| 岗位 | 人数 | 任务 |
|---|---:|---|
| 音控/歌词字幕 | 2 | 放伴奏、切歌词、控制音量。 |
| 侧台递篮/收篮 | 2 | 左右侧各1人，副歌递篮，尾声收篮。 |
| 过道引导 | 4 | 两条过道前后各1人，保持通道顺畅。 |
| 礼物传递协助 | 6 | 左中右三区协助排头传礼。 |
| 摄影录像 | 1-2 | 拍上台、发礼、ending定格。 |
| 回台口令 | 1 | 尾声前20秒提醒“回台”。 |
"""
    (OUT / "心愿便利贴_报告厅节目执行说明_v2.md").write_text(md, encoding="utf-8")


write_svg("01_舞台站位与上台.svg", page1())
write_svg("02_歌曲段落动作对应.svg", page2())
write_svg("03_两条过道发礼路线.svg", page3())
write_svg("04_Ending与学生后勤.svg", page4())
write_markdown()

print(OUT)
