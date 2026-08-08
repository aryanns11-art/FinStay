from datetime import datetime
import calendar
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
)

import matplotlib.pyplot as plt


def _format_currency(value):
    try:
        return f"₹ {float(value):,.2f}"
    except Exception:
        return f"₹ {value}"


def _draw_expense_chart(expense_categories, width=400, height=220):
    # expense_categories: list of (category, amount)
    if not expense_categories:
        return None

    labels = [str(cat) for cat, _ in expense_categories]
    amounts = [float(amt) for _, amt in expense_categories]

    fig, ax = plt.subplots(figsize=(width / 100, height / 100), dpi=100)
    y_pos = range(len(labels))
    ax.barh(y_pos, amounts, color="#FF9800")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel("Amount")
    ax.xaxis.set_major_formatter(lambda x, pos: f"{int(x):,}")
    plt.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format="PNG", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf


def _build_daily_table(month, year, daily_data):
    # daily_data is expected as iterable of (day, income, expense)
    days_in_month = calendar.monthrange(year, month)[1]
    # map day -> (income, expense)
    day_map = {int(row[0]): (float(row[1]), float(row[2])) for row in daily_data} if daily_data else {}

    rows = [["Date", "Income", "Expense", "Net"]]
    for day in range(1, days_in_month + 1):
        income, expense = day_map.get(day, (0.0, 0.0))
        net = income - expense
        date_label = datetime(year, month, day).strftime("%d %b")
        rows.append([date_label, _format_currency(income), _format_currency(expense), _format_currency(net)])

    return rows


def _add_footer(canvas_obj, doc):
    canvas_obj.saveState()
    width, height = A4
    margin = 20 * mm
    footer_text = f"Hotel Expense Tracker — Monthly Financial Statement"
    gen_text = f"Generated on: {datetime.now().strftime('%d %b %Y')}"
    page_text = f"Page {doc.page}"
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.setFillColor(colors.grey)
    canvas_obj.drawString(margin, 15 * mm, footer_text)
    canvas_obj.drawRightString(width - margin, 15 * mm, gen_text)
    canvas_obj.drawCentredString(width / 2.0, 12 * mm, page_text)
    canvas_obj.restoreState()


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
):
    # Build a reusable monthly financial statement using ReportLab Platypus
    doc = SimpleDocTemplate(file_path, pagesize=A4, rightMargin=20 * mm, leftMargin=20 * mm, topMargin=25 * mm, bottomMargin=30 * mm)

    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    heading = ParagraphStyle("Heading", parent=styles["Heading1"], fontSize=14, leading=16)
    small = ParagraphStyle("Small", parent=normal, fontSize=9)

    flowables = []

    # Header
    flowables.append(Paragraph("HOTEL EXPENSE TRACKER", heading))
    flowables.append(Spacer(1, 4))
    flowables.append(Paragraph("Monthly Financial Statement", normal))
    flowables.append(Spacer(1, 6))
    flowables.append(Paragraph(f"{calendar.month_name[month]} {year}", ParagraphStyle("Period", parent=normal, fontSize=12)))
    flowables.append(Spacer(1, 8))

    # Generated date
    flowables.append(Paragraph(f"Generated: {datetime.now().strftime('%d %b %Y')}", small))
    flowables.append(Spacer(1, 10))

    # 1. Monthly Summary
    flowables.append(Paragraph("<b>1. MONTHLY SUMMARY</b>", styles["Heading3"]))
    summary_table = [
        ["Total Income", _format_currency(income)],
        ["Total Expenses", _format_currency(expense)],
        ["Net Result", _format_currency(profit)],
        ["Transaction Count", str(transactions)],
    ]
    t = Table(summary_table, colWidths=[100 * mm, 60 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    flowables.append(t)
    flowables.append(Spacer(1, 12))

    # 2. Expense Breakdown (chart)
    flowables.append(Paragraph("<b>2. EXPENSE BREAKDOWN</b>", styles["Heading3"]))
    buf = _draw_expense_chart(expense_categories)
    if buf:
        img = Image(buf, width=160 * mm, height=80 * mm)
        flowables.append(img)
    else:
        flowables.append(Paragraph("No expense category data available for this period.", normal))

    flowables.append(Spacer(1, 12))

    # 3. Daily Financial Summary (table)
    flowables.append(Paragraph("<b>3. DAILY FINANCIAL SUMMARY</b>", styles["Heading3"]))
    daily_table_rows = _build_daily_table(month, year, daily_data)
    table = Table(daily_table_rows, colWidths=[40 * mm, 45 * mm, 45 * mm, 45 * mm])
    table_style = TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f2f2f2")),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
    ])
    table.setStyle(table_style)
    flowables.append(table)

    # Build PDF
    doc.build(flowables, onFirstPage=_add_footer, onLaterPages=_add_footer)
