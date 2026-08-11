from datetime import date, datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

from flask_app import db_session
from app.controllers.transaction_controller import TransactionController
from app.controllers.category_controller import CategoryController
from app.controllers.payment_method_controller import PaymentMethodController
from app.controllers.settings_controller import SettingsController
from app.models.transaction import Transaction

bp = Blueprint("transactions", __name__)


@bp.route("/transactions")
def index():
    session = db_session()
    try:
        tx       = TransactionController(session)
        settings = SettingsController(session)
        cats     = CategoryController(session)
        methods  = PaymentMethodController(session)

        keyword  = request.args.get("q", "").strip()
        tx_type  = request.args.get("type", "All")

        if keyword:
            transactions = tx.search_transactions(keyword)
        elif tx_type in ("Income", "Expense"):
            transactions = tx.get_transactions_by_type(tx_type)
        else:
            transactions = tx.get_transactions()

        categories      = cats.get_categories()
        payment_methods = methods.get_payment_methods()
        hotel_name      = settings.get_hotel_name() or "Hotel Finance"

        return render_template(
            "transactions.html",
            hotel_name=hotel_name,
            transactions=transactions,
            categories=categories,
            payment_methods=payment_methods,
            keyword=keyword,
            tx_type=tx_type,
            today=date.today().isoformat(),
            now_time=datetime.now().strftime("%H:%M"),
        )
    except Exception:
        from app.utils.logger import logger
        logger.exception("Transactions list error")
        flash("Unable to load transactions.", "error")
        return redirect(url_for("dashboard.index"))


@bp.route("/transactions/add", methods=["POST"])
def add():
    session = db_session()
    try:
        category_id        = int(request.form["category_id"])
        payment_method_id  = int(request.form["payment_method_id"])
        amount             = float(request.form["amount"])
        description        = request.form.get("description", "").strip() or None
        tx_date            = date.fromisoformat(request.form["transaction_date"])
        tx_time            = datetime.strptime(request.form["transaction_time"], "%H:%M").time()

        transaction = Transaction(
            category_id=category_id,
            payment_method_id=payment_method_id,
            amount=amount,
            description=description,
            transaction_date=tx_date,
            transaction_time=tx_time,
        )

        tx = TransactionController(session)
        tx.add_transaction(transaction)
        flash("Transaction saved successfully.", "success")
    except ValueError as e:
        flash(f"Invalid data: {e}", "error")
    except Exception:
        from app.utils.logger import logger
        logger.exception("Add transaction error")
        flash("Unable to save transaction. Please try again.", "error")

    return redirect(url_for("transactions.index"))


@bp.route("/categories/add", methods=["POST"])
def add_category():
    session = db_session()

    try:
        name = request.form.get("category_name", "").strip()
        category_type = request.form.get("category_type", "").strip()

        categories = CategoryController(session)

        categories.create_category(
            name=name,
            category_type=category_type,
        )

        flash(
            f"{category_type} category '{name}' added successfully.",
            "success",
        )

    except ValueError as e:
        flash(str(e), "error")

    except Exception:
        session.rollback()

        from app.utils.logger import logger
        logger.exception("Add category error")

        flash(
            "Unable to add category. The category may already exist.",
            "error",
        )

    return redirect(url_for("transactions.index"))


@bp.route("/categories/delete/<int:category_id>", methods=["POST"])
def delete_category(category_id):
    session = db_session()

    try:
        categories = CategoryController(session)
        categories.delete_category(category_id)

        flash("Category deleted successfully.", "success")

    except ValueError as e:
        session.rollback()
        flash(str(e), "error")

    except Exception:
        session.rollback()

        from app.utils.logger import logger
        logger.exception("Delete category error")

        flash("Unable to delete category.", "error")

    return redirect(url_for("transactions.index"))


@bp.route("/transactions/delete/<int:transaction_id>", methods=["POST"])
def delete(transaction_id):
    session = db_session()
    try:
        transaction = session.query(Transaction).filter(
            Transaction.id == transaction_id
        ).first()

        if transaction:
            tx = TransactionController(session)
            tx.delete_transaction(transaction)
            flash("Transaction deleted.", "success")
        else:
            flash("Transaction not found.", "error")
    except Exception:
        from app.utils.logger import logger
        logger.exception("Delete transaction error")
        flash("Unable to delete transaction. Please try again.", "error")

    return redirect(url_for("transactions.index"))
