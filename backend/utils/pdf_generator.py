import io
import re
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle
)

SECTION_LABELS = {
    "customer_insights": "Customer Insights",
    "market_insights": "Market & Competitor Analysis",
    "feature_priorities": "Feature Prioritization",
    "swot_analysis": "SWOT Analysis",
    "executive_summary": "Executive Summary",
}

ACCENT_COLORS = {
    "customer_insights": "#f59e0b",
    "market_insights": "#3b82f6",
    "feature_priorities": "#8b5cf6",
    "swot_analysis": "#10b981",
    "executive_summary": "#6366f1",
}

SECTION_NUMBERS = {
    "customer_insights": "01",
    "market_insights": "02",
    "feature_priorities": "03",
    "swot_analysis": "04",
    "executive_summary": "05",
}

PAGE_W = letter[0]
CONTENT_W = PAGE_W - 2 * inch


def _inline(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
    text = re.sub(r"`(.+?)`", r'<font face="Courier">\1</font>', text)
    return text


def _make_rl_table(table_lines: list, accent_hex: str) -> Table | None:
    rows = []
    for line in table_lines:
        s = line.strip()
        if re.match(r"^[\|\-\s:]+$", s):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if any(cells):
            rows.append(cells)

    if not rows:
        return None

    max_cols = max(len(r) for r in rows)
    rows = [r + [""] * (max_cols - len(r)) for r in rows]

    th_style = ParagraphStyle("TH", fontName="Helvetica-Bold", fontSize=8.5,
                               textColor=colors.white, leading=12)
    td_style = ParagraphStyle("TD", fontName="Helvetica", fontSize=8.5,
                               textColor=HexColor("#1e293b"), leading=12)

    table_data = []
    for i, row in enumerate(rows):
        s = th_style if i == 0 else td_style
        table_data.append([Paragraph(_inline(cell), s) for cell in row])

    col_w = CONTENT_W / max_cols
    t = Table(table_data, colWidths=[col_w] * max_cols, repeatRows=1, hAlign="LEFT")

    accent = HexColor(accent_hex)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), accent),
        ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#e2e8f0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]
    for idx in range(1, len(rows)):
        bg = colors.white if idx % 2 == 1 else HexColor("#f8fafc")
        cmds.append(("BACKGROUND", (0, idx), (-1, idx), bg))

    t.setStyle(TableStyle(cmds))
    return t


def _section_header(number: str, label: str, accent_hex: str) -> Table:
    num_s = ParagraphStyle("Num", fontName="Helvetica-Bold", fontSize=9,
                            textColor=HexColor(accent_hex), leading=13)
    lbl_s = ParagraphStyle("Lbl", fontName="Helvetica-Bold", fontSize=13,
                            textColor=HexColor("#0f172a"), leading=17)
    inner = Table(
        [[Paragraph(number, num_s), Paragraph(label, lbl_s)]],
        colWidths=[0.4 * inch, CONTENT_W - 0.4 * inch],
    )
    inner.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    outer = Table([[inner]], colWidths=[CONTENT_W])
    outer.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#f8fafc")),
        ("LINEBELOW", (0, 0), (-1, -1), 2.5, HexColor(accent_hex)),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ]))
    return outer


def _md_flowables(text: str, body, h2, h3, bullet, accent_hex: str) -> list:
    out = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        s = lines[i].strip()

        if s.startswith("|"):
            tbl_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                tbl_lines.append(lines[i])
                i += 1
            tbl = _make_rl_table(tbl_lines, accent_hex)
            if tbl:
                out.append(Spacer(1, 0.06 * inch))
                out.append(tbl)
                out.append(Spacer(1, 0.1 * inch))
            continue

        if not s:
            out.append(Spacer(1, 0.04 * inch))
        elif s.startswith("### "):
            out.append(Paragraph(_inline(s[4:]), h3))
        elif s.startswith("## "):
            out.append(Paragraph(_inline(s[3:]), h2))
        elif s.startswith("# "):
            out.append(Paragraph(_inline(s[2:]), h2))
        elif s.startswith("- ") or s.startswith("* "):
            out.append(Paragraph("•  " + _inline(s[2:]), bullet))
        elif re.match(r"^\d+\.\s", s):
            out.append(Paragraph(_inline(re.sub(r"^\d+\.\s", "", s)), bullet))
        else:
            out.append(Paragraph(_inline(s), body))
        i += 1
    return out


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(HexColor("#e2e8f0"))
    canvas.setLineWidth(0.5)
    canvas.line(inch, 0.65 * inch, PAGE_W - inch, 0.65 * inch)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(HexColor("#94a3b8"))
    canvas.drawString(inch, 0.45 * inch, "Product Strategy Report — Confidential")
    canvas.drawRightString(PAGE_W - inch, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def generate_pdf(results: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter,
        rightMargin=inch, leftMargin=inch,
        topMargin=inch, bottomMargin=0.9 * inch,
    )
    base = getSampleStyleSheet()

    title_s  = ParagraphStyle("TS", parent=base["Title"],   fontName="Helvetica-Bold",
                               textColor=HexColor("#0f172a"), fontSize=26, spaceAfter=4)
    sub_s    = ParagraphStyle("SS", parent=base["Normal"],  fontName="Helvetica",
                               textColor=HexColor("#64748b"), fontSize=11, spaceAfter=0)
    h2_s     = ParagraphStyle("H2", parent=base["Heading2"], fontName="Helvetica-Bold",
                               textColor=HexColor("#1e293b"), fontSize=11, spaceBefore=10, spaceAfter=3)
    h3_s     = ParagraphStyle("H3", parent=base["Heading3"], fontName="Helvetica-BoldOblique",
                               textColor=HexColor("#334155"), fontSize=10, spaceBefore=7, spaceAfter=2)
    body_s   = ParagraphStyle("BS", parent=base["Normal"],  fontName="Helvetica",
                               textColor=HexColor("#334155"), fontSize=9.5, leading=15, spaceAfter=3)
    bullet_s = ParagraphStyle("BU", parent=base["Normal"],  fontName="Helvetica",
                               textColor=HexColor("#334155"), fontSize=9.5, leading=14, spaceAfter=2, leftIndent=14)

    story = [
        Spacer(1, 0.15 * inch),
        Paragraph("Product Strategy Report", title_s),
        Paragraph("AI-Powered Multi-Agent Analysis", sub_s),
        Spacer(1, 0.2 * inch),
        HRFlowable(width="100%", thickness=2.5, color=HexColor("#6366f1")),
        Spacer(1, 0.35 * inch),
    ]

    for key, label in SECTION_LABELS.items():
        content = results.get(key, "")
        if not content:
            continue
        accent = ACCENT_COLORS.get(key, "#6366f1")
        num = SECTION_NUMBERS.get(key, "")
        story.append(_section_header(num, label, accent))
        story.append(Spacer(1, 0.12 * inch))
        story.extend(_md_flowables(content, body_s, h2_s, h3_s, bullet_s, accent))
        story.append(Spacer(1, 0.3 * inch))

    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)
    return buffer.getvalue()
