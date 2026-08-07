import os
import subprocess

from PySide6.QtCore import QThread, Signal
from config import ( DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)

from app.utils.postgres_tools import PostgreSQLTools


class RestoreWorker(QThread):
    """Run PostgreSQL restore without freezing the UI."""

    finished = Signal()
    error = Signal(str)

    def __init__(self, backup_file):
        super().__init__()

        self.backup_file = backup_file
        self.process = None

    def run(self):

        try:

            pg_restore = (
                PostgreSQLTools.find_pg_restore()
            )

            if not pg_restore:
                raise RuntimeError(
                    "pg_restore.exe could not be found."
                )

            if not os.path.exists(self.backup_file):
                raise FileNotFoundError(
                    "Selected backup file does not exist."
                )

            environment = os.environ.copy()
            environment["PGPASSWORD"] = DB_PASSWORD

            command = [
                str(pg_restore),

                "--host",
                DB_HOST,

                "--port",
                str(DB_PORT),

                "--username",
                DB_USER,

                "--dbname",
                DB_NAME,

                "--clean",

                "--if-exists",

                "--no-owner",

                "--exit-on-error",

                self.backup_file,
            ]

            self.process = subprocess.Popen(
                command,
                env=environment,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            stdout, stderr = self.process.communicate()

            if self.process.returncode != 0:

                raise RuntimeError(
                    stderr.strip()
                    or "Database restore failed."
                )

            self.finished.emit()

        except Exception as error:

            self.error.emit(str(error))

        finally:

            self.process = None

    def stop(self):
        """Stop pg_restore if it is running."""

        if self.process:

            self.process.terminate()

            try:
                self.process.wait(timeout=5)

            except subprocess.TimeoutExpired:

                self.process.kill()
                self.process.wait()

        if self.isRunning():
            self.quit()
            self.wait(5000)