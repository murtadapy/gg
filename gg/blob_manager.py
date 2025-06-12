from typing import List

from gg.database import Database
from gg.file_manager import FileManager


class BlobManager:
    def __init__(self,
                 tree_path: str,
                 file_manager: FileManager,
                 database: Database) -> None:
        self.tree_path = tree_path
        self.file_manager = file_manager
        self.database = database

    def _get_modified_blobs(self) -> List[str]:
        modified_blobs: List[str] = []

        files = self.file_manager.get_all_files()
        current_sprint = self.database.get_active_sprint()
        last_commit = self.database.get_last_commit(sprint_name=current_sprint)
        blobs = self.database.get_commit_blobs(commit_id=last_commit)


        while blobs:
            blob = blobs.pop()

            for file in files:
                ...
                
        return []
