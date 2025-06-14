from gg.database import Database
from gg.file_manager import FileManager
from gg.models import BlobStatus


class BlobManager:
    def __init__(self,
                 tree_path: str,
                 file_manager: FileManager,
                 database: Database) -> None:
        self.tree_path = tree_path
        self.file_manager = file_manager
        self.database = database

    def get_blobs_status(self) -> BlobStatus:
        blobs_status = BlobStatus()

        files = self.file_manager.get_all_files()
        current_sprint = self.database.get_active_sprint()
        sprint = self.database.get_sprint(sprint_name=current_sprint)

        if sprint:
            blobs = self.database.get_commit_blobs(
                commit_id=sprint.last_commit_id)
            commit = self.database.get_commit(id=sprint.id)
            while blobs and files:
                if files and not blobs:
                    blobs = self.database.get_commit_blobs(
                        commit_id=commit.parent_commit_id)

                    commit = self.database.get_commit(
                        id=commit.parent_commit_id)

                blob_commit = blobs.pop()
                path = blob_commit.path
                if path in files:
                    blob = self.database.get_blob(blob_commit.blob_id)
                    if blob.sha256 != self.file_manager.get_sha256(path):
                        blobs_status.modified.append(path)
                    else:
                        blobs_status.unchanged.append(path)
                else:
                    blobs_status.deleted.append(blob_commit.path)

                files.remove(path)

        for file in files:
            blobs_status.created.append(file)

        return blobs_status
