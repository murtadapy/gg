
from gg.base import CommandBase
from gg.database import Database
from gg.file_manager import FileManager
from gg.blob_manager import BlobManager
from gg.logger import Logger


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

        self.logger.pulse("Updating config value")
        self.database.update_value(key=self.config_key,
                                   value=self.config_value)
        self.logger.pulse("Updated config value")

        self.logger.info(f"Updated {self.config_key} successfully")
