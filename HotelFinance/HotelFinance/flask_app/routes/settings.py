import os
import re
import tempfile
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_app import db_session
from app.controllers.settings_controller import SettingsController
from app.controllers.backup_controller import BackupController
from app.controllers.custom_field_controller import CustomFieldController

bp = Blueprint("settings", __name__)


@bp.route("/settings")
def index():
    session = db_session()
    try:
        ctrl = SettingsController(session)
        settings = ctrl.get_settings()
        hotel_name = ctrl.get_hotel_name() or "Hotel Finance"

        custom_field_ctrl = CustomFieldController(session)
        custom_fields = custom_field_ctrl.get_all()

        backup_ctrl = BackupController()
        last_backup = backup_ctrl.get_last_backup()
        last_backup_time = None
        if last_backup:
            last_backup_time = datetime.fromtimestamp(
                last_backup.stat().st_mtime
            ).strftime("%d %b %Y %I:%M %p")

        return render_template(
            "settings.html",
            hotel_name=hotel_name,
            settings=settings,
            custom_fields=custom_fields,
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
        hotel_name = request.form.get("hotel_name", "").strip()
        hotel_address = request.form.get("hotel_address", "").strip() or None
        phone_number = request.form.get("phone_number", "").strip() or None
        email = request.form.get("email", "").strip() or None
        gstin = request.form.get("gstin", "").strip() or None

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


@bp.route("/settings/custom-field", methods=["POST"])
def add_custom_field():
    session = db_session()
    try:
        field_name = request.form.get("field_name", "").strip()
        field_value = request.form.get("field_value", "").strip()

        if not field_name:
            flash("Field name is required.", "error")
            return redirect(url_for("settings.index"))

        if not field_value:
            flash("Field value is required.", "error")
            return redirect(url_for("settings.index"))

        ctrl = CustomFieldController(session)
        ctrl.add_field(field_name, field_value)
        flash("Custom field saved.", "success")
    except ValueError as exc:
        flash(str(exc), "error")
    except Exception:
        from app.utils.logger import logger
        logger.exception("Custom field save error")
        flash("Unable to save custom field. Please try again.", "error")

    return redirect(url_for("settings.index"))


@bp.route("/settings/custom-field/<int:field_id>/delete", methods=["POST"])
def delete_custom_field(field_id):
    session = db_session()
    try:
        ctrl = CustomFieldController(session)
        ctrl.delete_field(field_id)
        flash("Custom field deleted.", "success")
    except ValueError as exc:
        flash(str(exc), "error")
    except Exception:
        from app.utils.logger import logger
        logger.exception("Custom field delete error")
        flash("Unable to delete custom field. Please try again.", "error")

    return redirect(url_for("settings.index"))


@bp.route("/settings/backup", methods=["POST"])
def backup():
    try:
        ctrl = BackupController()
        bfile = ctrl.backup_database()
        flash(f"Backup created: {bfile.name}", "success")
    except Exception:
        from app.utils.logger import logger
        logger.exception("Backup error")
        flash("Backup could not be created. Please try again.", "error")

    return redirect(url_for("settings.index"))


@bp.route("/settings/restore", methods=["POST"])
def restore():
    uploaded_file = request.files.get("backup_file")

    if not uploaded_file or not uploaded_file.filename:
        flash("Please select a valid backup file to restore.", "error")
        return redirect(url_for("settings.index"))

    temp_path = None
    try:
        with tempfile.NamedTemporaryFile("wb", suffix=".db", delete=False) as temp_file:
            uploaded_file.save(temp_file.name)
            temp_path = temp_file.name

        BackupController().restore_database(temp_path)
        flash(
            "Database restored successfully. The application data has been restored from the selected backup.",
            "success",
        )
    except FileNotFoundError:
        flash("Restore failed. The selected file may not exist or may not be a valid Hotel Finance database.", "error")
    except (RuntimeError, OSError, ValueError):
        flash("Restore failed. The selected file may not be a valid Hotel Finance database.", "error")
    except Exception:
        from app.utils.logger import logger
        logger.exception("Restore error")
        flash("Restore failed. The selected file may not be a valid Hotel Finance database.", "error")
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except OSError:
                pass

    return redirect(url_for("settings.index"))
