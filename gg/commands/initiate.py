import sys
import os
import ctypes

from gg.base import CommandBase
from gg.database import Database
from gg.logger import Logger


class InitiateCommand(CommandBase):
    def __init__(self, path: str, database: Database, logger: Logger) -> None:
        super().__init__(path=path, database=database, logger=logger)

    def _create_database(self) -> None:
        self.database.create_database()

    def _create_repostiory(self) -> None:
        os.makedirs(self.path, exist_ok=True)

        if sys.platform == "win32":
            ctypes.windll.kernel32.SetFileAttributesW(self.path, 0x02)

    def _create_main_sprint(self) -> None:
        self.database.create_sprint(sprint_name="main")

    def execute(self) -> None:
        self.logger.pulse("Executing initate command")

        self._create_repostiory()
        self.logger.pulse("Created Repository folder")

        self._create_database()
        self.logger.pulse("Created database")

        self._create_main_sprint()
        self.logger.pulse("Created main sprint")

        self.logger.info(f"Initialized empty gg repository in {self.path}")
