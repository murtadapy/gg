from abc import ABC
from abc import abstractmethod

from gg.database import Database
from gg.logger import Logger


class CommandBase(ABC):
    def __init__(self, path: str, database: Database, logger: Logger) -> None:
        self.path = path
        self.database = database
        self.logger = logger

    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError()
