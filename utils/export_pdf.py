"""
PDF export using ReportLab — branded Nova Commerce header, KPI summary table,
and real chart images (rendered via kaleido) embedded from live data.
"""

import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def build_pdf_report(kpis: dict, revenue_chart_fig, category_chart_fig, narrative: str = None) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.6 * inch)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "NovaTitle", parent=styles["Title"], textColor=colors.HexColor("#171a21"), fontSize=22,
    )
    subtitle_style = ParagraphStyle(
        "NovaSubtitle", parent=styles["Normal"], textColor=colors.HexColor("#666c7a"), fontSize=11,
    )
    body_style = ParagraphStyle(
        "NovaBody", parent=styles["Normal"], fontSize=10, leading=14,
    )

    elements = []
    elements.append(Paragraph("Nova Commerce", title_style))
    elements.append(Paragraph("Executive Performance Report — InsightForge", subtitle_style))
    elements.append(Spacer(1, 20))

    # KPI table
    kpi_data = [
        ["Revenue", "Orders", "Customers", "Profit (est.)", "MoM Growth"],
        [
            f"${kpis['revenue']:,.0f}", f"{kpis['orders']:,}", f"{kpis['customers']:,}",
            f"${kpis['profit']:,.0f}", f"{kpis['growth']:.1f}%",
        ],
    ]
    kpi_table = Table(kpi_data, colWidths=[95] * 5)
    kpi_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#171a21")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
    ]))
    elements.append(kpi_table)
    elements.append(Spacer(1, 24))

    if narrative:
        elements.append(Paragraph("Executive Summary", styles["Heading2"]))
        elements.append(Paragraph(narrative, body_style))
        elements.append(Spacer(1, 20))

    # Embed charts as images
    for fig, title in [(revenue_chart_fig, "Revenue Trend"), (category_chart_fig, "Sales by Category")]:
        img_bytes = fig.to_image(format="png", width=700, height=350, scale=2)
        elements.append(Paragraph(title, styles["Heading3"]))
        elements.append(Image(io.BytesIO(img_bytes), width=6.3 * inch, height=3.15 * inch))
        elements.append(Spacer(1, 16))

    doc.build(elements)
    return buffer.getvalue()