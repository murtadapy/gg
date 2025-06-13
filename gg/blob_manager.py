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
        sprint = self.database.get_sprint(sprint_name=current_sprint)
        blobs = self.database.get_commit_blobs(commit_id=sprint.last_commit_id)

        while blobs:
            blob = blobs.pop()

            for file in files:
                ...

        return []

        # Get all blobs of current sprint by doing the following:
        # Get all blobs in the tree of the repository
        # Get current sprint last commit id
        # Find all blobs of the last commit id
        # If we didn't find all blobs init,we search on its children
        # recursively
        # once we get each blob, then we compare its SHA-256 in database
        # And check if it is the same or not.
