
from gg.base import CommandBase
from gg.core.database import Database
from gg.core.file_manager import FileManager
from gg.core.blob_manager import BlobManager
from gg.core.logger import Logger


class ConfigCommand(CommandBase):
    def __init__(self,
                 database: Database,
                 file_manager: FileManager,
                 blob_manager: BlobManager,
                 logger: Logger,
                 config_key: str,
                 config_value: str) -> None:
        super().__init__(database=database,
                         file_manager=file_manager,
                         blob_manager=blob_manager,
                         logger=logger)
        self.config_key = config_key
        self.config_value = config_value

    def execute(self) -> None:
        self.logger.pulse("Executing config command")

        self.logger.pulse("Checking if repository exist")
        if not self.file_manager.check_if_repository_exists():
            self.logger.info("This is not a gg repository")
            return

        self.logger.pulse("Updating config value")
        self.database.update_value(key=self.config_key,
                                   value=self.config_value)
        self.logger.pulse("Updated config value")

        self.logger.info(f"Updated {self.config_key} successfully")
