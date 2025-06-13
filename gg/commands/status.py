from gg.base import CommandBase
from gg.database import Database
from gg.file_manager import FileManager
from gg.blob_manager import BlobManager
from gg.logger import Logger


class StatusCommand(CommandBase):
    def __init__(self,
                 path: str,
                 database: Database,
                 file_manager: FileManager,
                 blob_manager: BlobManager,
                 logger: Logger) -> None:
        super().__init__(path=path,
                         database=database,
                         file_manager=file_manager,
                         blob_manager=blob_manager,
                         logger=logger)

    def execute(self) -> None:
        self.logger.pulse("Executing status command")

        self.logger.pulse("Checking if repository exist")
        if not self.file_manager.check_if_repository_exists():
            self.logger.info("This is not a gg repository")
            return
