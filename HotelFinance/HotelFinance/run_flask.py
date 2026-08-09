"""
Flask entry point for Hotel Finance web application.

Usage:
    python run_flask.py

Opens at: http://127.0.0.1:5000
"""

import sys
import os

# Ensure the project root is on sys.path so that
# 'config', 'app.*', and 'flask_app.*' can all be imported.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask_app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False,   # avoids double-init with SQLAlchemy on Windows
    )
