import re
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_app import db_session
from app.controllers.settings_controller import SettingsController
from app.controllers.backup_controller import BackupController

bp = Blueprint("settings", __name__)


@bp.route("/settings")
def index():
    session = db_session()
    try:
        ctrl     = SettingsController(session)
        settings = ctrl.get_settings()
        hotel_name = ctrl.get_hotel_name() or "Hotel Finance"

        backup_ctrl  = BackupController()
        last_backup  = backup_ctrl.get_last_backup()
        last_backup_time = None
        if last_backup:
            last_backup_time = datetime.fromtimestamp(
                last_backup.stat().st_mtime
            ).strftime("%d %b %Y %I:%M %p")

        return render_template(
            "settings.html",
            hotel_name=hotel_name,
            settings=settings,
            last_backup_time=last_backup_time,
        )
    except Exception:
        from app.utils.logger import logger
        logger.exception("Settings page error")
        flash("Unable to load settings.", "error")
        return redirect(url_for("dashboard.index"))


@bp.route("/settings/hotel", methods=["POST"])
def save_hotel():
    session = db_session()
    try:
        hotel_name    = request.form.get("hotel_name", "").strip()
        hotel_address = request.form.get("hotel_address", "").strip() or None
        phone_number  = request.form.get("phone_number", "").strip()  or None
        email         = request.form.get("email", "").strip()         or None
        gstin         = request.form.get("gstin", "").strip()         or None

        if not hotel_name:
            flash("Hotel name is required.", "error")
            return redirect(url_for("settings.index"))

        if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            flash("Please enter a valid email address.", "error")
            return redirect(url_for("settings.index"))

        ctrl = SettingsController(session)
        ctrl.save_hotel_information(hotel_name, hotel_address, phone_number, email, gstin)
        flash("Hotel information saved.", "success")
    except Exception:
        from app.utils.logger import logger
        logger.exception("Settings save error")
        flash("Unable to save hotel information. Please try again.", "error")

    return redirect(url_for("settings.index"))


@bp.route("/settings/backup", methods=["POST"])
def backup():
    try:
        ctrl  = BackupController()
        bfile = ctrl.backup_database()
        flash(f"Backup created: {bfile.name}", "success")
    except Exception:
        from app.utils.logger import logger
        logger.exception("Backup error")
        flash("Backup could not be created. Please try again.", "error")

    return redirect(url_for("settings.index"))
