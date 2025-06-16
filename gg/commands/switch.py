from gg.base import CommandBase
from gg.database import Database
from gg.file_manager import FileManager
from gg.blob_manager import BlobManager
from gg.logger import Logger


class SwitchCommand(CommandBase):
    def __init__(self,
                 database: Database,
                 file_manager: FileManager,
                 blob_manager: BlobManager,
                 logger: Logger,
                 sprint_name: str) -> None:
        super().__init__(database=database,
                         file_manager=file_manager,
                         blob_manager=blob_manager,
                         logger=logger)
        self.sprint_name = sprint_name

    def execute(self) -> None:
        self.logger.pulse("Executing switch command")

        self.logger.pulse("Checking if repository exist")
        if not self.file_manager.check_if_repository_exists():
            self.logger.info("This is not a gg repository")
            return

        self.logger.pulse(f"Getting {self.sprint_name} sprint")
        sprint = self.database.get_sprint(sprint_name=self.sprint_name)
        self.logger.pulse("Got the sprint")

        if sprint:
            self.logger.pulse("Deleting current tree")
            self.database.update_value("CURRENT_SPRINT", self.sprint_name)
            self.file_manager.delete_all_tree()
            self.logger.pulse("Deleted current tree")

            self.logger.pulse("Writing sprint blobs")

            commit = self.database.get_commit(sprint.last_commit_id)
            written_blobs = set()

            while True:
                if not commit:
                    break

                commit_blobs = self.database.get_commit_blobs(
                    commit_id=commit.id)

                for commit_blob in commit_blobs:
                    self.logger.pulse(f"Writing {commit_blob} blob")

                    if commit_blob.blob_id in written_blobs:
                        continue

                    blob = self.database.get_blob(blob_id=commit_blob.blob_id)
                    if blob:
                        path = self.file_manager.get_absolute_path(
                            commit_blob.path)

                        self.file_manager.create_all_folders(path)

                        with open(path, "w") as f:
                            c = self.file_manager.decompress_blob(blob.content)
                            f.write(c)

                            written_blobs.add(commit_blob.blob_id)

                commit = self.database.get_commit(commit.parent_commit_id)

            self.logger.pulse("Wrote sprint blobs")
        else:
            self.logger.info("Sprint is not found")
        self.logger.info(f"Switched to  sprint {self.sprint_name}")
