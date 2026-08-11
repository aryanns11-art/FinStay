"""
Flask application factory.

Reuses the existing SQLAlchemy engine and SessionLocal from the desktop app.
Sessions are scoped per-request via SQLAlchemy's scoped_session.
"""

from flask import Flask
from sqlalchemy.orm import scoped_session

from app.database.session import SessionLocal
from app.database.init_db import create_tables


# Per-request database session — created once here, used everywhere
db_session = scoped_session(SessionLocal)


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Secret key for flash messages / WTForms CSRF
    app.config["SECRET_KEY"] = "hotel-finance-flask-secret-2024"

    # Ensure tables exist (safe to call on every startup — checks before creating)
    create_tables()

    # Tear down the scoped session after every request
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # Register blueprints
    from flask_app.routes.dashboard import bp as dashboard_bp
    from flask_app.routes.transactions import bp as transactions_bp
    from flask_app.routes.cash import bp as cash_bp
    from flask_app.routes.reports import bp as reports_bp
    from flask_app.routes.settings import bp as settings_bp
    from flask_app.routes.bank_accounts import bp as bank_accounts_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(cash_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(bank_accounts_bp)

    return app
