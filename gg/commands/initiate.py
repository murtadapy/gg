import sys
import os
import ctypes

from gg.base import CommandBase
from gg.database import Database
from gg.file_manager import FileManager
from gg.logger import Logger


class InitiateCommand(CommandBase):
    def __init__(self,
                 path: str,
                 database: Database,
                 file_manager: FileManager,
                 logger: Logger) -> None:
        super().__init__(path=path,
                         database=database,
                         file_manager=file_manager,
                         logger=logger)

    def _create_repostiory(self) -> None:
        os.makedirs(self.path)

        if sys.platform == "win32":
            ctypes.windll.kernel32.SetFileAttributesW(self.path, 0x02)

    def _create_database(self) -> None:
        self.database.create_database()

    def _create_main_sprint(self) -> None:
        self.database.create_sprint(sprint_name="main")

    def execute(self) -> None:
        self.logger.pulse("Executing initate command")

        self.logger.pulse("Checking if repository exists")
        if self.file_manager.check_if_repository_exists():
            self.logger.info(f"The repository is already exist in {self.path}")
            return

        self.logger.pulse("Creating repository folder")
        self._create_repostiory()
        self.logger.pulse("Created repository folder successfully")

        self.logger.pulse("Creating the repository database")
        self._create_database()
        self.logger.pulse("Created database successfully")

        self.logger.pulse("Creating the main sprint")
        self._create_main_sprint()
        self.logger.pulse("Created main sprint successfully")

        self.logger.info(f"Initialized empty gg repository in {self.path}")
