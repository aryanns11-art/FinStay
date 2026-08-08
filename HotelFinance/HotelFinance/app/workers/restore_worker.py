import os
import subprocess

from PySide6.QtCore import QThread, Signal

from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)

from app.utils.postgres_tools import PostgreSQLTools


class RestoreWorker(QThread):
    """Run PostgreSQL restore in a background thread."""

    restore_finished = Signal()
    restore_error = Signal(str)
    restore_done = Signal()

    def __init__(self, backup_file):
        super().__init__()

        self.backup_file = backup_file
        self.process = None

    def run(self):

        try:

            # ---------------------------------------------
            # Find pg_restore
            # ---------------------------------------------

            pg_restore = PostgreSQLTools.find_pg_restore()

            if not pg_restore:
                raise RuntimeError(
                    "pg_restore.exe could not be found."
                )

            # ---------------------------------------------
            # Check backup file
            # ---------------------------------------------

            if not os.path.isfile(self.backup_file):
                raise FileNotFoundError(
                    "Selected backup file does not exist."
                )

            # ---------------------------------------------
            # PostgreSQL password
            # ---------------------------------------------

            environment = os.environ.copy()
            environment["PGPASSWORD"] = DB_PASSWORD

            # ---------------------------------------------
            # Restore command
            # ---------------------------------------------

            command = [
                str(pg_restore),

                "--host",
                str(DB_HOST),

                "--port",
                str(DB_PORT),

                "--username",
                str(DB_USER),

                "--dbname",
                str(DB_NAME),

                "--clean",
                "--if-exists",
                "--no-owner",
                "--exit-on-error",

                self.backup_file,
            ]

            # ---------------------------------------------
            # Start pg_restore
            # ---------------------------------------------

            self.process = subprocess.Popen(
                command,
                env=environment,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # ---------------------------------------------
            # Wait for pg_restore
            # ---------------------------------------------

            stdout, stderr = self.process.communicate()

            return_code = self.process.returncode

            self.process = None

            # ---------------------------------------------
            # Restore failed
            # ---------------------------------------------

            if return_code != 0:

                error_message = (
                    stderr.strip()
                    or stdout.strip()
                    or "Database restore failed."
                )

                self.restore_error.emit(
                    error_message
                )

                return

            # ---------------------------------------------
            # Restore successful
            # ---------------------------------------------

            self.restore_finished.emit()

        except Exception as error:

            self.process = None

            self.restore_error.emit(
                str(error)
            )

        finally:
            self.restore_done.emit()

    def stop(self):
        """Stop pg_restore safely."""

        process = self.process

        if process is not None:

            try:

                if process.poll() is None:

                    process.terminate()

                    try:
                        process.wait(
                            timeout=5
                        )

                    except subprocess.TimeoutExpired:

                        process.kill()

                        process.wait()

            except Exception:
                pass

        # Do NOT call quit() here.
        #
        # run() is already finishing after the subprocess
        # has been terminated.

        if self.isRunning():

            self.wait(5000)