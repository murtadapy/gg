from abc import ABC
from abc import abstractmethod

import os
import sys

from gg.database import Database
from gg.file_manager import FileManager
from gg.logger import Logger


class CommandBase(ABC):
    def __init__(self,
                 path: str,
                 database: Database,
                 file_manager: FileManager,
                 logger: Logger) -> None:
        self.tree_path = path
        self.gg_path = os.path.join(sys.path[0], ".gg")
        self.database = database
        self.file_manager = file_manager
        self.logger = logger

    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError()
