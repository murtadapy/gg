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

        # Get all blobs of current sprint by doing the following:
        # Get all blobs in the tree of the repository
        # Get current sprint last commit id
        # Find all blobs of the last commit id
        # If we didn't find all blobs init,we search on its children
        # recursively
        # once we get each blob, then we compare its SHA-256 in database
        # And check if it is the same or not.
