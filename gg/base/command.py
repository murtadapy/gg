import os
from abc import ABC
from abc import abstractmethod

from gg.core.database import Database
from gg.core.file_manager import FileManager
from gg.core.blob_manager import BlobManager
from gg.core.path import Path
from gg.core.logger import Logger


class CommandBase(ABC):
    def __init__(self,
                 database: Database,
                 file_manager: FileManager,
                 blob_manager: BlobManager,
                 logger: Logger) -> None:
        self.tree_path = Path.get_root_path()
        self.gg_path = os.path.join(self.tree_path, ".gg")
        self.database = database
        self.file_manager = file_manager
        self.blob_manager = blob_manager
        self.logger = logger

    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError()
