from pathlib import Path
import os
import sys

from dotenv import load_dotenv


# =========================================================
# Application Base Directory
# =========================================================

if getattr(sys, "frozen", False):
    # Running as a PyInstaller executable
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    # Running normally from source
    BASE_DIR = Path(__file__).resolve().parent


# =========================================================
# Load Environment Variables
# =========================================================

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


# =========================================================
# Database Configuration (SQLite)
# =========================================================

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATA_DIR / "hotel_finance.db"

# Absolute path URL so the DB does not depend on the working directory.
DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"

BACKUP_DIR = BASE_DIR / "backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)


# =========================================================
# Application
# =========================================================

APP_NAME = os.getenv(
    "APP_NAME",
    "Hotel Finance Manager"
)

APP_THEME = os.getenv(
    "APP_THEME",
    "dark"
)
