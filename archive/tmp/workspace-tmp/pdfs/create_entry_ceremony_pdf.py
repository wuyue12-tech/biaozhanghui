from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


OUTPUT = "output/pdf/八升九入境仪式活动方案_短版.pdf"

FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"
FONT_NAME = "ArialUnicode"
pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))


def p(text, style):
    return Paragraph(text, style)


def section(title, styles):
    return [
        Spacer(1, 7 * mm),
        Paragraph(title, styles["section"]),
        Spacer(1, 3 * mm),
    ]


def bullet(text, styles):
    return Paragraph(f"• {text}", styles["body"])


def make_table(data, col_widths, styles, header=True):
    table_data = []
    for row_index, row in enumerate(data):
        row_style = styles["table_header"] if header and row_index == 0 else styles["table"]
        table_data.append([Paragraph(str(cell), row_style) for cell in row])
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT", repeatRows=1 if header else 0)
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), FONT_NAME),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17324d") if header else colors.white),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white if header else colors.HexColor("#1f2933")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f6f8fa")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d8dee6")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT_NAME, 9)
    canvas.setFillColor(colors.HexColor("#6b7280"))
    canvas.drawString(18 * mm, 12 * mm, "八升九入境仪式活动方案")
    canvas.drawRightString(192 * mm, 12 * mm, f"第 {doc.page} 页")
    canvas.restoreState()


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="title_cn",
        fontName=FONT_NAME,
        fontSize=22,
        leading=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0f263d"),
        spaceAfter=5 * mm,
    )
)
styles.add(
    ParagraphStyle(
        name="subtitle",
        fontName=FONT_NAME,
        fontSize=11,
        leading=18,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#4b5563"),
    )
)
styles.add(
    ParagraphStyle(
        name="section",
        fontName=FONT_NAME,
        fontSize=15,
        leading=22,
        textColor=colors.HexColor("#17324d"),
        spaceAfter=2 * mm,
    )
)
styles.add(
    ParagraphStyle(
        name="body",
        fontName=FONT_NAME,
        fontSize=10.5,
        leading=17,
        textColor=colors.HexColor("#1f2933"),
        alignment=TA_LEFT,
        spaceAfter=1.2 * mm,
    )
)
styles.add(
    ParagraphStyle(
        name="lead",
        fontName=FONT_NAME,
        fontSize=12,
        leading=20,
        textColor=colors.HexColor("#111827"),
        leftIndent=0,
        rightIndent=0,
        spaceAfter=2 * mm,
    )
)
styles.add(
    ParagraphStyle(
        name="table",
        fontName=FONT_NAME,
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#1f2933"),
    )
)
styles.add(
    ParagraphStyle(
        name="table_header",
        fontName=FONT_NAME,
        fontSize=9.5,
        leading=14,
        textColor=colors.white,
    )
)

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=18 * mm,
    leftMargin=18 * mm,
    topMargin=16 * mm,
    bottomMargin=18 * mm,
)

story = []
story.append(Paragraph("八升九入境仪式活动方案", styles["title_cn"]))
story.append(Paragraph("短版汇报稿｜场地：室内篮球馆｜时长：85 分钟｜对象：八年级学生约 110 人、教师 17 人、家长代表若干", styles["subtitle"]))
story.extend(section("一、活动名称", styles))
story.append(Paragraph("九年级入境挑战赛", styles["lead"]))
story.append(
    Paragraph(
        "学生以 14 支导师小队为单位，在篮球馆完成三关挑战，形成一张“入境行动牌”；家长写支持卡，导师完成认证，帮助学生带着具体行动进入九年级。",
        styles["body"],
    )
)

story.extend(section("二、活动目标", styles))
for item in [
    "让学生看见九年级可能遇到的真实挑战，如作业节奏、考试压力、时间管理、睡眠、手机、亲子沟通和主动求助。",
    "让学生把“认真听课、努力学习、调整心态”等宽泛表达，转化为能在九年级执行的小行动。",
    "让 14 支导师小队在现场完成分工、选择、改写、说明和认证，形成真实的团队参与。",
    "让家长看见孩子在团队中的状态，并写下一件可以在家里提供的具体支持。",
    "让导师成为学生进入九年级后的支持入口，完成有标准、有收束的入境认证。",
]:
    story.append(bullet(item, styles))

story.extend(section("三、活动过程", styles))
story.append(
    make_table(
        [
            ["时间", "环节", "现场动作"],
            ["0-12 分钟", "集结发布", "14 支小队进入战队区，队长领取任务包；主持说明规则，领导发布挑战令。"],
            ["12-25 分钟", "第一关：信号侦察接力", "6 人接力取回信号碎片，分成 3 堆并命名，解锁红袋信号卡，选出 1 个九年级挑战。"],
            ["25-55 分钟", "第二关：行动补给传球", "完成 10 次传球，至少 7 人触球，解锁蓝袋行动卡，补写谁来做、何时做、怎么检查。"],
            ["55-73 分钟", "第三关：三方支援通道", "3 名代表带行动牌完成同伴、家长、导师三方支援，解锁金袋支持卡并写入行动牌。"],
            ["73-85 分钟", "认证入境", "导师按统一标准确认行动牌，贴入境章；领导点亮荣誉章，全体完成入境合影。"],
        ],
        [25 * mm, 38 * mm, 101 * mm],
        styles,
    )
)

story.append(PageBreak())
story.extend(section("四、其他", styles))
story.append(Paragraph("1. 前期准备", styles["lead"]))
for item in [
    "学生共创：每人提交 1 条九年级真实挑战；各导师班完成行动改写、队名队牌和 10 秒入场动作；每队至少 2-3 条学生原句进入现场卡包。",
    "教师筹备：策划老师筛选学生素材，制成信号卡、行动卡、支持卡、入境行动牌、导师认证卡和支援路线卡。",
    "家长准备：每队邀请 1-2 位家长代表进入边线观察与支持环节，其余家长在观察区完成支持卡。",
]:
    story.append(bullet(item, styles))

story.append(Spacer(1, 3 * mm))
story.append(Paragraph("2. 现场分工", styles["lead"]))
story.append(
    make_table(
        [
            ["角色", "任务"],
            ["总策划与主持总控", "推进全流程，掌握时间、口令和现场节奏。"],
            ["14 位导师", "对应本队，发任务包、过程提醒、检查行动牌、完成认证。"],
            ["运行教师", "负责音响计时、物资巡场、家长引导和安全巡场。"],
            ["家长代表", "观察学生团队状态，阅读行动牌，填写家庭支持卡。"],
            ["领导", "开场见证、巡场观察、结尾点亮荣誉章。"],
        ],
        [45 * mm, 119 * mm],
        styles,
    )
)

story.append(Spacer(1, 4 * mm))
story.append(Paragraph("3. 场地与物资", styles["lead"]))
for item in [
    "篮球馆划分为主持区、战队区、任务推进区、家长观察区、入境墙五个区域。",
    "每队准备任务包：红袋、蓝袋、金袋，信号碎片卡、信号卡、行动卡、支持卡、入境行动牌、导师认证卡、支援路线卡、软球、马克笔、入境章贴纸。",
    "全场准备：入境墙、地贴编号、信号点地贴、补给圈地贴、无线麦、音响、倒计时屏、家长支持卡、荣誉章贴纸和备用文具。",
]:
    story.append(bullet(item, styles))

story.append(Spacer(1, 4 * mm))
story.append(Paragraph("4. 完成标准", styles["lead"]))
story.append(
    make_table(
        [
            ["项目", "标准"],
            ["真实信号", "每队选择一个具体九年级挑战。"],
            ["具体行动", "两条行动写清谁做、何时做、怎么检查。"],
            ["三方支持", "行动牌包含同伴、家长、导师三方支持。"],
            ["导师认证", "导师围绕真实信号、两条行动、最需要的支持完成三问认证。"],
            ["活动留痕", "每队留下 1 张入境行动牌，后续用于九年级第一次导师谈话和家校沟通。"],
        ],
        [38 * mm, 126 * mm],
        styles,
    )
)

doc.build(story, onFirstPage=footer, onLaterPages=footer)
