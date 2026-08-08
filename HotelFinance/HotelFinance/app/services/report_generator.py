from datetime import datetime
import calendar
from io import BytesIO
from xml.sax.saxutils import escape

import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def _format_currency(value):
    try:
        return f"₹ {float(value):,.2f}"
    except (TypeError, ValueError):
        return f"₹ {value}"


def _draw_income_expense_chart(income, expense, width=400, height=220):
    fig, axis = plt.subplots(figsize=(width / 100, height / 100), dpi=100)
    values = [float(income), float(expense)]
    bars = axis.bar(["Income", "Expense"], values, color=["#2E8B57", "#C76B3A"])
    axis.set_ylabel("Amount")
    axis.yaxis.set_major_formatter(lambda value, position: f"{int(value):,}")
    axis.bar_label(bars, labels=[f"{value:,.0f}" for value in values], padding=3)
    plt.tight_layout()

    buffer = BytesIO()
    fig.savefig(buffer, format="PNG", bbox_inches="tight")
    plt.close(fig)
    buffer.seek(0)
    return buffer


def _draw_category_chart(categories, title, color, width=400, height=220):
    if not categories:
        return None

    labels = [str(category) for category, _ in categories]
    amounts = [float(amount) for _, amount in categories]

    fig, axis = plt.subplots(figsize=(width / 100, height / 100), dpi=100)
    positions = range(len(labels))
    axis.barh(positions, amounts, color=color)
    axis.set_yticks(positions)
    axis.set_yticklabels(labels)
    axis.invert_yaxis()
    axis.set_title(title)
    axis.set_xlabel("Amount")
    axis.xaxis.set_major_formatter(lambda value, position: f"{int(value):,}")
    plt.tight_layout()

    buffer = BytesIO()
    fig.savefig(buffer, format="PNG", bbox_inches="tight")
    plt.close(fig)
    buffer.seek(0)
    return buffer


def _build_daily_table(month, year, daily_data):
    days_in_month = calendar.monthrange(year, month)[1]
    day_map = {
        int(row[0]): (float(row[1]), float(row[2]))
        for row in daily_data
    } if daily_data else {}

    rows = [["Date", "Income", "Expense", "Net"]]
    for day in range(1, days_in_month + 1):
        income, expense = day_map.get(day, (0.0, 0.0))
        net = income - expense
        date_label = datetime(year, month, day).strftime("%d %b")
        rows.append([
            date_label,
            _format_currency(income),
            _format_currency(expense),
            _format_currency(net),
        ])

    return rows


def _add_footer(canvas_obj, document, hotel_name):
    canvas_obj.saveState()
    width, _ = A4
    margin = 20 * mm
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.setFillColor(colors.grey)
    canvas_obj.drawString(margin, 15 * mm, f"{hotel_name} — Monthly Financial Report")
    canvas_obj.drawRightString(width - margin, 15 * mm, datetime.now().strftime("Generated: %d %b %Y"))
    canvas_obj.drawCentredString(width / 2.0, 12 * mm, f"Page {document.page}")
    canvas_obj.restoreState()


def _create_category_table(title, categories):
    rows = [[title, "Amount"]]
    rows.extend([str(category), _format_currency(amount)] for category, amount in categories)

    if len(rows) == 1:
        rows.append(["No category data available", ""])

    table = Table(rows, colWidths=[100 * mm, 60 * mm])
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#D1D5DB")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F3F4F6")),
        ("ALIGN", (1, 1), (1, -1), "RIGHT"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


def create_monthly_report_pdf(
    file_path,
    month,
    year,
    income,
    expense,
    profit,
    transactions,
    daily_data,
    income_categories,
    expense_categories,
    hotel_information=None,
):
    """Build the reusable A4 monthly financial report."""

    document = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=25 * mm,
        bottomMargin=30 * mm,
    )

    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    hotel_heading = ParagraphStyle(
        "HotelHeading",
        parent=styles["Heading1"],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1F2937"),
    )
    report_heading = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#374151"),
    )
    section_heading = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading3"],
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#1F2937"),
    )
    small = ParagraphStyle("Small", parent=normal, fontSize=9)

    hotel_name = getattr(hotel_information, "hotel_name", None) or "Hotel Expense Tracker"
    hotel_details = []
    for value in (
        getattr(hotel_information, "hotel_address", None),
        getattr(hotel_information, "phone_number", None),
        getattr(hotel_information, "email", None),
    ):
        if value:
            hotel_details.append(escape(str(value)))
    gstin = getattr(hotel_information, "gstin", None)
    if gstin:
        hotel_details.append(f"GSTIN: {escape(str(gstin))}")

    flowables = []
    flowables.append(Paragraph(escape(str(hotel_name)).upper(), hotel_heading))
    flowables.append(Spacer(1, 4))
    flowables.append(Paragraph("Monthly Financial Report", report_heading))
    flowables.append(Spacer(1, 6))
    flowables.append(Paragraph(f"Report Period: {calendar.month_name[month]} {year}", small))
    flowables.append(Paragraph(f"Generated: {datetime.now().strftime('%d %b %Y')}", small))
    if hotel_details:
        flowables.append(Spacer(1, 4))
        flowables.append(Paragraph(" | ".join(hotel_details), small))
    flowables.append(Spacer(1, 10))

    flowables.append(Paragraph("Financial Overview", section_heading))
    summary_table = Table([
        ["Monthly Income", _format_currency(income)],
        ["Monthly Expense", _format_currency(expense)],
        ["Net Profit", _format_currency(profit)],
        ["Transaction Count", str(transactions)],
    ], colWidths=[100 * mm, 60 * mm])
    summary_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#D1D5DB")),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F3F4F6")),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    flowables.append(summary_table)
    flowables.append(Spacer(1, 12))

    flowables.append(Paragraph("Monthly Income vs Expense", section_heading))
    flowables.append(Image(_draw_income_expense_chart(income, expense), width=130 * mm, height=70 * mm))
    flowables.append(Spacer(1, 12))

    flowables.append(Paragraph("Category Analysis", section_heading))
    flowables.append(_create_category_table("Income by Category", income_categories))
    flowables.append(Spacer(1, 8))
    flowables.append(_create_category_table("Expense by Category", expense_categories))

    flowables.append(PageBreak())
    flowables.append(Paragraph("Category Charts", section_heading))
    income_chart = _draw_category_chart(income_categories, "Income by Category", "#2E8B57")
    if income_chart:
        flowables.append(Image(income_chart, width=150 * mm, height=70 * mm))
    expense_chart = _draw_category_chart(expense_categories, "Expense by Category", "#C76B3A")
    if expense_chart:
        flowables.append(Image(expense_chart, width=150 * mm, height=70 * mm))
    if not income_chart and not expense_chart:
        flowables.append(Paragraph("No category data available for this period.", normal))

    flowables.append(PageBreak())
    flowables.append(Paragraph("Daily Financial Data", section_heading))
    daily_table = Table(_build_daily_table(month, year, daily_data), colWidths=[40 * mm, 45 * mm, 45 * mm, 45 * mm], repeatRows=1)
    daily_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F3F4F6")),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    flowables.append(daily_table)

    footer = lambda canvas_obj, doc: _add_footer(canvas_obj, doc, hotel_name)
    document.build(flowables, onFirstPage=footer, onLaterPages=footer)
