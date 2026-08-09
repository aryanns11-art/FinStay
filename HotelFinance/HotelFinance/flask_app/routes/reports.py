import calendar
import os
import tempfile
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file

from flask_app import db_session
from app.controllers.transaction_controller import TransactionController
from app.controllers.settings_controller import SettingsController
from app.services.report_generator import create_monthly_report_pdf

bp = Blueprint("reports", __name__)

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
CURRENT_YEAR = datetime.now().year
YEARS = list(range(CURRENT_YEAR - 5, CURRENT_YEAR + 1))


@bp.route("/reports")
def index():
    session = db_session()
    try:
        month = int(request.args.get("month", datetime.now().month))
        year  = int(request.args.get("year",  datetime.now().year))

        tx       = TransactionController(session)
        settings = SettingsController(session)

        income      = tx.get_monthly_income(month, year)
        expense     = tx.get_monthly_expense(month, year)
        profit      = income - expense
        tx_count    = tx.get_monthly_transaction_count(month, year)
        income_cats = tx.get_income_by_category(month, year)
        expense_cats= tx.get_expense_by_category(month, year)
        daily_data  = tx.get_daily_income_expense(month, year)
        hotel_name  = settings.get_hotel_name() or "Hotel Finance"

        # Build daily table rows
        days_in_month = calendar.monthrange(year, month)[1]
        day_map = {int(r[0]): (float(r[1]), float(r[2])) for r in daily_data} if daily_data else {}
        daily_rows = []
        for d in range(1, days_in_month + 1):
            inc, exp = day_map.get(d, (0.0, 0.0))
            daily_rows.append({
                "date":    datetime(year, month, d).strftime("%d %b"),
                "income":  inc,
                "expense": exp,
                "net":     inc - exp,
            })

        return render_template(
            "reports.html",
            hotel_name=hotel_name,
            months=MONTHS,
            years=YEARS,
            selected_month=month,
            selected_year=year,
            income=income,
            expense=expense,
            profit=profit,
            tx_count=tx_count,
            income_cats=income_cats,
            expense_cats=expense_cats,
            daily_rows=daily_rows,
        )
    except Exception:
        from app.utils.logger import logger
        logger.exception("Reports page error")
        flash("Unable to load reports.", "error")
        return redirect(url_for("dashboard.index"))


@bp.route("/reports/export-pdf")
def export_pdf():
    session = db_session()
    try:
        month = int(request.args.get("month", datetime.now().month))
        year  = int(request.args.get("year",  datetime.now().year))

        tx       = TransactionController(session)
        settings = SettingsController(session)

        income       = tx.get_monthly_income(month, year)
        expense      = tx.get_monthly_expense(month, year)
        profit       = income - expense
        tx_count     = tx.get_monthly_transaction_count(month, year)
        daily_data   = tx.get_daily_income_expense(month, year)
        income_cats  = tx.get_income_by_category(month, year)
        expense_cats = tx.get_expense_by_category(month, year)
        hotel_info   = settings.get_settings()

        # Write PDF to a temp file, then stream it
        tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        tmp.close()

        create_monthly_report_pdf(
            tmp.name, month, year,
            income, expense, profit, tx_count,
            daily_data, income_cats, expense_cats,
            hotel_info,
        )

        month_name   = MONTHS[month - 1]
        download_name = f"Hotel_Report_{month_name}_{year}.pdf"

        return send_file(
            tmp.name,
            as_attachment=True,
            download_name=download_name,
            mimetype="application/pdf",
        )
    except Exception:
        from app.utils.logger import logger
        logger.exception("PDF export error")
        flash("Unable to export PDF. Please try again.", "error")
        return redirect(url_for("reports.index"))
