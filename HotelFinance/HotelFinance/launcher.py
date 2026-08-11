"""
HotelFinance Windows Launcher
==============================
Entry point packaged into HotelFinance.exe by PyInstaller.

Strategy
--------
Flask is run in a background DAEMON THREAD (not a subprocess).
The Flask app factory is imported directly — same process, no child Python.

Clean shutdown
--------------
A Windows console-control handler catches CTRL+C and the window-close (X button)
events.  On either event it sets a threading.Event which causes main() to return,
after which Python exits and all daemon threads die with it.

Werkzeug's dev server cannot be stopped cleanly from another thread, but because
the Flask thread is a daemon it is forcibly terminated by the OS when the main
thread exits — which is exactly what we want.

Database / backup paths
-----------------------
config.py already handles sys.frozen:
    BASE_DIR = Path(sys.executable).resolve().parent
So data/ and backups/ always sit next to HotelFinance.exe, never in _MEIPASS.
"""

import os
import sys
import time
import threading
import webbrowser

# ── 1. Fix sys.path for frozen bundle ───────────────────────────────────────
if getattr(sys, "frozen", False):
    # _MEIPASS contains all collected Python packages
    sys.path.insert(0, sys._MEIPASS)
    # Also insert the EXE directory so config.py / .env resolve correctly
    sys.path.insert(0, os.path.dirname(sys.executable))
else:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── 2. Force Agg backend BEFORE matplotlib is imported anywhere ─────────────
os.environ["MPLBACKEND"] = "Agg"

# ── 3. Constants ─────────────────────────────────────────────────────────────
HOST = "127.0.0.1"
PORT = 5000
URL  = f"http://{HOST}:{PORT}"

# ── 4. Shutdown event shared between main thread and console handler ─────────
_shutdown = threading.Event()


def _install_console_handler():
    """
    Register a Windows console-control handler so that:
      - Ctrl+C  (CTRL_C_EVENT)
      - Ctrl+Break
      - Window X button  (CTRL_CLOSE_EVENT)
      - Logoff / Shutdown
    all set _shutdown and give the main thread a moment to exit cleanly.
    """
    try:
        import ctypes
        import ctypes.wintypes

        HANDLER_ROUTINE = ctypes.WINFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.DWORD)

        @HANDLER_ROUTINE
        def _handler(ctrl_type):
            _shutdown.set()
            # Give the main thread up to 5 s to exit before Windows kills us
            time.sleep(5)
            return True   # suppress default handler

        ctypes.windll.kernel32.SetConsoleCtrlHandler(_handler, True)
    except Exception:
        pass   # non-Windows or ctypes unavailable — KeyboardInterrupt fallback used


# ── 5. Flask thread ──────────────────────────────────────────────────────────

def _run_flask():
    """Start the Flask dev server in a background daemon thread."""
    from flask_app import create_app
    flask_app = create_app()
    flask_app.run(host=HOST, port=PORT, debug=False, use_reloader=False)


def _wait_for_flask(timeout: int = 30) -> bool:
    """Poll until Flask responds or timeout expires."""
    import urllib.request
    import urllib.error

    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(URL, timeout=1)
            return True
        except Exception:
            time.sleep(0.25)
    return False


# ── 6. Main ──────────────────────────────────────────────────────────────────

def main():
    _install_console_handler()

    # Set a visible console title
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(
            "Hotel Finance — close this window to stop the application"
        )
    except Exception:
        pass

    # Start Flask in a daemon thread (dies when main thread exits)
    flask_thread = threading.Thread(target=_run_flask, daemon=True, name="flask-server")
    flask_thread.start()

    print(f"Starting Hotel Finance…")
    print(f"Server: {URL}")
    print()

    # Wait for readiness
    if _wait_for_flask(timeout=30):
        print("Ready — opening browser.")
        webbrowser.open(URL)
    else:
        print(f"WARNING: Flask did not start within 30 seconds.")
        print(f"Try opening {URL} manually.")

    print()
    print("Hotel Finance is running.")
    print("Close this window (or press Ctrl+C) to stop.")
    print()

    # Block until shutdown event or Ctrl+C
    try:
        while not _shutdown.is_set():
            # Wake up every second to check — allows clean Ctrl+C on Windows
            _shutdown.wait(timeout=1.0)
    except KeyboardInterrupt:
        pass

    print("Shutting down…")
    # Daemon thread will be killed when we return here and Python exits
    sys.exit(0)


if __name__ == "__main__":
    main()
