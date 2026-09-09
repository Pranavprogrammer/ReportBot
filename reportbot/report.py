from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart

def money(v):
    return f"₹{v:,.0f}"

def build_pdf(metrics, output_path: Path):
    styles = getSampleStyleSheet()
    title = ParagraphStyle("Title2", parent=styles["Title"], alignment=TA_CENTER, fontSize=26, leading=30, spaceAfter=10)
    subtitle = ParagraphStyle("Sub", parent=styles["Normal"], alignment=TA_CENTER, fontSize=11, textColor=colors.HexColor("#64748b"))
    h = ParagraphStyle("H", parent=styles["Heading2"], fontSize=16, leading=20, spaceBefore=12, spaceAfter=8)
    body = ParagraphStyle("Body2", parent=styles["BodyText"], fontSize=9.5, leading=14)

    doc = SimpleDocTemplate(
        str(output_path), pagesize=A4, rightMargin=16*mm, leftMargin=16*mm,
        topMargin=15*mm, bottomMargin=15*mm
    )
    story = [
        Spacer(1, 18*mm),
        Paragraph("REPORTBOT", title),
        Paragraph("Automated Sales Analytics Report", subtitle),
        Spacer(1, 8*mm),
        Paragraph("Executive Summary", h),
        Paragraph(
            f"ReportBot processed incoming sales data and calculated revenue, order volume, "
            f"average order value, growth and portfolio-friendly customer lifetime value estimates.",
            body
        ),
        Spacer(1, 5*mm),
    ]

    summary_data = [
        ["Metric", "Value"],
        ["Total Revenue", money(metrics["total_revenue"])],
        ["Orders", f'{metrics["orders"]:,}'],
        ["Average Order Value", money(metrics["aov"])],
        ["MoM Growth", f'{metrics["mom_growth"]:.2f}%'],
        ["Annualized CLV Proxy", money(metrics["clv"])],
    ]
    table = Table(summary_data, colWidths=[75*mm, 75*mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#0f172a")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ("PADDING", (0,0), (-1,-1), 7),
    ]))
    story += [table, Spacer(1, 7*mm), Paragraph("Top Products", h)]

    top_data = [["Product", "Revenue"]]
    top_data += [[x["product"], money(x["revenue"])] for x in metrics["top_products"]]
    t2 = Table(top_data, colWidths=[100*mm, 50*mm])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#cbd5e1")),
        ("PADDING", (0,0), (-1,-1), 7),
    ]))
    story += [t2, PageBreak(), Paragraph("Regional Performance", h)]

    region_data = [["Region", "Revenue"]]
    region_data += [[x["region"], money(x["revenue"])] for x in metrics["regional"]]
    t3 = Table(region_data, colWidths=[100*mm, 50*mm])
    t3.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#cbd5e1")),
        ("PADDING", (0,0), (-1,-1), 7),
    ]))
    story += [t3, Spacer(1, 7*mm), Paragraph("Daily Revenue Trend", h)]

    d = Drawing(460, 210)
    chart = HorizontalLineChart()
    chart.x = 40
    chart.y = 35
    chart.height = 150
    chart.width = 390
    vals = [x["revenue"] for x in metrics["daily_revenue"]]
    chart.data = [vals or [0]]
    chart.categoryAxis.categoryNames = [x["date"][5:] for x in metrics["daily_revenue"]] or ["N/A"]
    chart.valueAxis.valueMin = 0
    chart.lines[0].strokeWidth = 2
    d.add(chart)
    story.append(d)
    story += [
        Spacer(1, 5*mm),
        Paragraph("Generated automatically by ReportBot. This report is designed for portfolio demonstration and can be scheduled for daily delivery.", body)
    ]
    doc.build(story)
