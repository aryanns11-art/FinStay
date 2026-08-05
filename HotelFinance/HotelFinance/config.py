from pathlib import Path
import os
from dotenv import load_dotenv

# Project Root
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# Database Configuration
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Application
APP_NAME = os.getenv("APP_NAME", "Hotel Finance Manager")
APP_THEME = os.getenv("APP_THEME", "dark")