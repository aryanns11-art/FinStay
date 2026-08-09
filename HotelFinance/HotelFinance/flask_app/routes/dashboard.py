from datetime import date

from flask import Blueprint, render_template, flash

from flask_app import db_session
from app.controllers.transaction_controller import TransactionController
from app.controllers.settings_controller import SettingsController

bp = Blueprint("dashboard", __name__)


@bp.route("/")
def index():
    session = db_session()
    try:
        tx = TransactionController(session)
        settings = SettingsController(session)
        today = date.today()

        income        = tx.get_today_income(today)
        expense       = tx.get_today_expense(today)
        profit        = income - expense
        cash_income   = tx.get_cash_income(today)
        cash_expense  = tx.get_cash_expense(today)
        online_income  = tx.get_online_income(today)
        online_expense = tx.get_online_expense(today)
        income_count   = tx.get_income_transaction_count(today)
        expense_count  = tx.get_expense_transaction_count(today)
        highest_income  = tx.get_highest_income_transaction(today)
        highest_expense = tx.get_highest_expense_transaction(today)
        hotel_name = settings.get_hotel_name() or "Hotel Finance"

        return render_template(
            "dashboard.html",
            hotel_name=hotel_name,
            today=today,
            income=income,
            expense=expense,
            profit=profit,
            cash_income=cash_income,
            cash_expense=cash_expense,
            online_income=online_income,
            online_expense=online_expense,
            income_count=income_count,
            expense_count=expense_count,
            highest_income=highest_income,
            highest_expense=highest_expense,
        )
    except Exception as e:
        from app.utils.logger import logger
        logger.exception("Dashboard error")
        flash("Unable to load dashboard data.", "error")
        return render_template("dashboard.html", hotel_name="Hotel Finance",
                               today=date.today(), income=0, expense=0, profit=0,
                               cash_income=0, cash_expense=0, online_income=0,
                               online_expense=0, income_count=0, expense_count=0,
                               highest_income=None, highest_expense=None)
