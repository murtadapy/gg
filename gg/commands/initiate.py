import sys
import os
import ctypes

from gg.base import CommandBase
from gg.database import Database
from gg.logger import Logger


class InitiateCommand(CommandBase):
    def __init__(self, path: str, logger: Logger) -> None:
        super().__init__(path=path, logger=logger)

    def _create_database(self) -> None:
        Database.create_database(self.path)

    def _create_repostiory(self) -> None:
        os.makedirs(self.path, exist_ok=True)

        if sys.platform == "win32":
            ctypes.windll.kernel32.SetFileAttributesW(self.path, 0x02)

    def execute(self) -> None:
        self.logger.pulse("Executing initate command")

        self._create_repostiory()
        self.logger.pulse("Created Repository folder")

        self._create_database()
        self.logger.pulse("Created database")

        self.logger.info(f"Initialized empty gg repository in {self.path}")
