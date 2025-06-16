from gg.base import CommandBase
from gg.core.database import Database
from gg.core.file_manager import FileManager
from gg.core.blob_manager import BlobManager
from gg.core.logger import Logger


class StatusCommand(CommandBase):
    def __init__(self,
                 database: Database,
                 file_manager: FileManager,
                 blob_manager: BlobManager,
                 logger: Logger) -> None:
        super().__init__(database=database,
                         file_manager=file_manager,
                         blob_manager=blob_manager,
                         logger=logger)

    def execute(self) -> None:
        self.logger.pulse("Executing status command")

        self.logger.pulse("Checking if repository exist")
        if not self.file_manager.check_if_repository_exists():
            self.logger.info("This is not a gg repository")
            return

        self.logger.pulse("Getting blobs status")
        blob_status = self.blob_manager.get_blobs_status()
        self.logger.pulse("Got blobs status")

        self.logger.pulse("Creating the response message")
        current_sprint = self.database.get_value("CURRENT_SPRINT")
        message = f"On sprint {current_sprint}\n"

        if (not blob_status.created and not blob_status.modified
                and not blob_status.deleted):
            message += "No Changes have been made"
        else:
            for blob in blob_status.created:
                message += f"\tCreated: {blob}\n"

            for blob in blob_status.modified:
                message += f"\tModified: {blob}\n"

            for blob in blob_status.deleted:
                message += f"\tDeleted: {blob}\n"

        self.logger.pulse("Created the response message")
        self.logger.info(message)
