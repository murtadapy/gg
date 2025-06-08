from abc import ABC
from abc import abstractmethod

from gg.logger import Logger


class CommandBase(ABC):
    def __init__(self, path: str, logger: Logger) -> None:
        self.path = path
        self.logger = logger

    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError()
