from abc import ABC
from abc import abstractmethod

import os
import sys

from gg.database import Database
from gg.file_manager import FileManager
from gg.blob_manager import BlobManager
from gg.logger import Logger


class CommandBase(ABC):
    def __init__(self,
                 path: str,
                 database: Database,
                 file_manager: FileManager,
                 blob_manager: BlobManager,
                 logger: Logger) -> None:
        self.tree_path = path
        self.gg_path = os.path.join(sys.path[0], ".gg")
        self.database = database
        self.file_manager = file_manager
        self.blob_manager = blob_manager
        self.logger = logger

    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError()
