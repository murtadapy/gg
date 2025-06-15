import sys
import os
import ctypes

from gg.base import CommandBase
from gg.database import Database
from gg.file_manager import FileManager
from gg.blob_manager import BlobManager
from gg.logger import Logger


class InitiateCommand(CommandBase):
    def __init__(self,
                 database: Database,
                 file_manager: FileManager,
                 blob_manager: BlobManager,
                 logger: Logger) -> None:
        super().__init__(database=database,
                         file_manager=file_manager,
                         blob_manager=blob_manager,
                         logger=logger)

    def _create_repostiory(self) -> None:
        os.makedirs(self.gg_path)

        if sys.platform == "win32":
            ctypes.windll.kernel32.SetFileAttributesW(self.gg_path, 0x02)

    def _create_database(self) -> None:
        self.database.create_database()

    def _create_main_sprint(self) -> None:
        self.database.create_sprint(sprint_name="main")
        self.database.update_value("CURRENT_SPRINT", "main")

    def execute(self) -> None:
        self.logger.pulse("Executing initate command")

        self.logger.pulse("Checking if repository exists")
        if self.file_manager.check_if_repository_exists():
            self.logger.info("The repository is "
                             f"already exist in {self.gg_path}")
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

        self.logger.info(f"Initialized empty gg repository in {self.gg_path}")
