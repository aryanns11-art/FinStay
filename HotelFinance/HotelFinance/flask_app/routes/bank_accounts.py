"""
Flask routes for Bank Accounts management.
All business logic lives in BankAccountController / BankAccountService.
"""

from datetime import date
from decimal import Decimal, InvalidOperation

from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_app import db_session
from app.controllers.bank_account_controller import BankAccountController
from app.controllers.settings_controller import SettingsController

bp = Blueprint("bank_accounts", __name__)


def _hotel_name(session) -> str:
    return SettingsController(session).get_hotel_name() or "Hotel Finance"


# ── List / main page ───────────────────────────────────────────────────────────

@bp.route("/bank-accounts")
def index():
    session = db_session()
    try:
        ctrl   = BankAccountController(session)
        today  = date.today()

        accounts = ctrl.get_all_accounts()

        # Build a summary dict for each account
        summaries = {}
        for acct in accounts:
            summaries[acct.id] = ctrl.get_account_summary(acct.id, today)

        return render_template(
            "bank_accounts.html",
            hotel_name=_hotel_name(session),
            accounts=accounts,
            summaries=summaries,
            today=today,
        )
    except Exception:
        from app.utils.logger import logger
        logger.exception("Bank accounts list error")
        flash("Unable to load bank accounts.", "error")
        return redirect(url_for("dashboard.index"))


# ── Add account ────────────────────────────────────────────────────────────────

@bp.route("/bank-accounts/add", methods=["POST"])
def add():
    session = db_session()
    try:
        name           = request.form.get("name", "").strip()
        account_number = request.form.get("account_number", "").strip() or None

        ctrl = BankAccountController(session)
        ctrl.create_account(name, account_number)
        flash("Bank account added successfully.", "success")

    except ValueError as e:
        flash(str(e), "error")
    except Exception:
        from app.utils.logger import logger
        logger.exception("Add bank account error")
        flash("Unable to add bank account. Please try again.", "error")

    return redirect(url_for("bank_accounts.index"))


# ── Edit account ───────────────────────────────────────────────────────────────

@bp.route("/bank-accounts/<int:account_id>/edit", methods=["POST"])
def edit(account_id: int):
    session = db_session()
    try:
        name           = request.form.get("name", "").strip()
        account_number = request.form.get("account_number", "").strip() or None

        ctrl = BankAccountController(session)
        ctrl.edit_account(account_id, name, account_number)
        flash("Bank account updated successfully.", "success")

    except ValueError as e:
        flash(str(e), "error")
    except Exception:
        from app.utils.logger import logger
        logger.exception("Edit bank account error")
        flash("Unable to update bank account. Please try again.", "error")

    return redirect(url_for("bank_accounts.index"))


# ── Deactivate account ─────────────────────────────────────────────────────────

@bp.route("/bank-accounts/<int:account_id>/deactivate", methods=["POST"])
def deactivate(account_id: int):
    session = db_session()
    try:
        ctrl = BankAccountController(session)
        ctrl.deactivate_account(account_id)
        flash("Bank account deactivated.", "success")

    except ValueError as e:
        flash(str(e), "error")
    except Exception:
        from app.utils.logger import logger
        logger.exception("Deactivate bank account error")
        flash("Unable to deactivate bank account. Please try again.", "error")

    return redirect(url_for("bank_accounts.index"))


# ── Set / update opening balance ───────────────────────────────────────────────

@bp.route("/bank-accounts/<int:account_id>/opening-balance", methods=["POST"])
def set_opening_balance(account_id: int):
    session = db_session()
    try:
        raw = request.form.get("opening_balance", "0").strip()
        try:
            opening_balance = Decimal(raw)
        except InvalidOperation:
            raise ValueError("Opening balance must be a valid number.")

        ctrl  = BankAccountController(session)
        today = date.today()
        ctrl.set_opening_balance(account_id, today, opening_balance)
        flash("Opening balance saved successfully.", "success")

    except ValueError as e:
        flash(str(e), "error")
    except Exception:
        from app.utils.logger import logger
        logger.exception("Set opening balance error")
        flash("Unable to save opening balance. Please try again.", "error")

    return redirect(url_for("bank_accounts.index"))


# ── Account detail page ────────────────────────────────────────────────────────

@bp.route("/bank-accounts/<int:account_id>")
def detail(account_id: int):
    session = db_session()
    try:
        ctrl  = BankAccountController(session)
        today = date.today()

        account = ctrl.get_account_by_id(account_id)
        if not account:
            flash("Bank account not found.", "error")
            return redirect(url_for("bank_accounts.index"))

        summary      = ctrl.get_account_summary(account_id, today)
        transactions = ctrl.get_today_transactions(account_id, today)

        return render_template(
            "bank_accounts.html",
            hotel_name=_hotel_name(session),
            accounts=ctrl.get_all_accounts(),
            summaries={account_id: summary},
            today=today,
            detail_account=account,
            detail_transactions=transactions,
        )
    except Exception:
        from app.utils.logger import logger
        logger.exception("Bank account detail error")
        flash("Unable to load account details.", "error")
        return redirect(url_for("bank_accounts.index"))
