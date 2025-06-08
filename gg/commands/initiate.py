from gg.base import CommandBase
from gg.logger import Logger


class InitiateCommand(CommandBase):
    def __init__(self, logger: Logger) -> None:
        super().__init__(logger=logger)

    def execute(self) -> None:
        self.logger.pulse("Executing initate command")
        ...
