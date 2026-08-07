import os
import shutil
from pathlib import Path


class PostgreSQLTools:
    """Locate PostgreSQL command-line tools on Windows."""

    @staticmethod
    def find_tool(tool_name):
        """
        Find a PostgreSQL executable.

        Checks:
        1. Windows PATH
        2. Common PostgreSQL installation folders
        """

        # =====================================================
        # Check PATH
        # =====================================================

        tool = shutil.which(tool_name)

        if tool:
            return Path(tool)

        # =====================================================
        # Check PostgreSQL installation folders
        # =====================================================

        postgres_root = Path(
            r"C:\Program Files\PostgreSQL"
        )

        if postgres_root.exists():

            versions = []

            for folder in postgres_root.iterdir():

                if folder.is_dir():

                    bin_folder = folder / "bin"

                    executable = (
                        bin_folder /
                        f"{tool_name}.exe"
                    )

                    if executable.exists():
                        versions.append(executable)

            # Newest PostgreSQL version first
            versions.sort(
                key=lambda path: path.parent.parent.name,
                reverse=True,
            )

            if versions:
                return versions[0]

        return None

    @classmethod
    def find_pg_dump(cls):
        """Find pg_dump.exe."""
        return cls.find_tool("pg_dump")

    @classmethod
    def find_pg_restore(cls):
        """Find pg_restore.exe."""
        return cls.find_tool("pg_restore")