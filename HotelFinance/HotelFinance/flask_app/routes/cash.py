from datetime import date

from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_app import db_session
from app.controllers.transaction_controller import TransactionController
from app.controllers.daily_balance_controller import DailyBalanceController
from app.controllers.cash_denomination_controller import CashDenominationController
from app.controllers.settings_controller import SettingsController

bp = Blueprint("cash", __name__)

DENOMINATIONS = (500, 200, 100, 50, 20, 10, 5, 2, 1)


@bp.route("/cash")
def index():
    session = db_session()
    try:
        today    = date.today()
        tx       = TransactionController(session)
        bal      = DailyBalanceController(session)
        denom    = CashDenominationController(session)
        settings = SettingsController(session)

        balance      = bal.get_balance(today)
        cash_opening   = float(balance.cash_opening)   if balance else 0.0
        online_opening = float(balance.online_opening) if balance else 0.0

        cash_income    = float(tx.get_today_cash_income(today))
        cash_expense   = float(tx.get_today_cash_expense(today))
        online_income  = float(tx.get_today_online_income(today))
        online_expense = float(tx.get_today_online_expense(today))

        cash_closing   = cash_opening   + cash_income   - cash_expense
        online_closing = online_opening + online_income - online_expense

        denom_record   = denom.get_by_date(today)
        transactions   = tx.get_today_transactions(today)
        hotel_name     = settings.get_hotel_name() or "Hotel Finance"

        return render_template(
            "cash.html",
            hotel_name=hotel_name,
            today=today,
            balance=balance,
            cash_opening=cash_opening,
            cash_income=cash_income,
            cash_expense=cash_expense,
            cash_closing=cash_closing,
            online_opening=online_opening,
            online_income=online_income,
            online_expense=online_expense,
            online_closing=online_closing,
            denom_record=denom_record,
            denominations=DENOMINATIONS,
            transactions=transactions,
        )
    except Exception:
        from app.utils.logger import logger
        logger.exception("Cash page error")
        flash("Unable to load cash management data.", "error")
        return redirect(url_for("dashboard.index"))


@bp.route("/cash/opening-balance", methods=["POST"])
def save_opening_balance():
    session = db_session()
    try:
        today          = date.today()
        cash_opening   = float(request.form.get("cash_opening", 0))
        online_opening = float(request.form.get("online_opening", 0))

        bal     = DailyBalanceController(session)
        balance = bal.get_balance(today)

        if balance:
            balance.cash_opening   = cash_opening
            balance.online_opening = online_opening
            bal.update_balance()
        else:
            bal.create_balance(today, cash_opening, online_opening)

        flash("Opening balance saved.", "success")
    except Exception:
        from app.utils.logger import logger
        logger.exception("Opening balance save error")
        flash("Unable to save opening balance. Please try again.", "error")

    return redirect(url_for("cash.index"))


@bp.route("/cash/denominations", methods=["POST"])
def save_denominations():
    session = db_session()
    try:
        today = date.today()
        denom = CashDenominationController(session)
        record = denom.get_or_create(today)

        record.denomination_500 = int(request.form.get("d500", 0))
        record.denomination_200 = int(request.form.get("d200", 0))
        record.denomination_100 = int(request.form.get("d100", 0))
        record.denomination_50  = int(request.form.get("d50",  0))
        record.denomination_20  = int(request.form.get("d20",  0))
        record.denomination_10  = int(request.form.get("d10",  0))
        record.denomination_5   = int(request.form.get("d5",   0))
        record.denomination_2   = int(request.form.get("d2",   0))
        record.denomination_1   = int(request.form.get("d1",   0))

        record.total = sum([
            record.denomination_500 * 500,
            record.denomination_200 * 200,
            record.denomination_100 * 100,
            record.denomination_50  * 50,
            record.denomination_20  * 20,
            record.denomination_10  * 10,
            record.denomination_5   * 5,
            record.denomination_2   * 2,
            record.denomination_1   * 1,
        ])

        denom.save_or_update(record)
        flash("Denomination counts saved.", "success")
    except Exception:
        from app.utils.logger import logger
        logger.exception("Denomination save error")
        flash("Unable to save denominations. Please try again.", "error")

    return redirect(url_for("cash.index"))
