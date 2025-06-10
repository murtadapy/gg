from gg.base import CommandBase
from gg.database import Database
from gg.file_manager import FileManager
from gg.logger import Logger


class StatusCommand(CommandBase):
    def __init__(self,
                 path: str,
                 database: Database,
                 file_manager: FileManager,
                 logger: Logger) -> None:
        super().__init__(path=path,
                         database=database,
                         file_manager=file_manager,
                         logger=logger)

    def execute(self) -> None:
        self.logger.pulse("Executing status command")
