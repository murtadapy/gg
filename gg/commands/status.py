from gg.base import CommandBase
from gg.database import Database
from gg.logger import Logger


class StatusCommand(CommandBase):
    def __init__(self, path: str, database: Database, logger: Logger) -> None:
        super().__init__(path=path, database=database, logger=logger)

    def execute(self) -> None:
        self.logger.pulse("Executing status command")
