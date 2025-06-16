from datetime import datetime
from uuid import uuid4

from gg.base import CommandBase
from gg.core.database import Database
from gg.core.file_manager import FileManager
from gg.core.blob_manager import BlobManager
from gg.core.logger import Logger


class CommitCommand(CommandBase):
    def __init__(self,
                 database: Database,
                 file_manager: FileManager,
                 blob_manager: BlobManager,
                 logger: Logger) -> None:
        super().__init__(database=database,
                         file_manager=file_manager,
                         blob_manager=blob_manager,
                         logger=logger)

    def execute(self) -> None:
        self.logger.pulse("Executing commit command")

        self.logger.pulse("Checking if repository exist")
        if not self.file_manager.check_if_repository_exists():
            self.logger.info("This is not a gg repository")
            return

        self.logger.pulse("Getting current sprint")
        current_sprint = self.database.get_value(key="CURRENT_SPRINT")
        sprint = self.database.get_sprint(sprint_name=current_sprint)
        self.logger.pulse("Got the current spint")

        if sprint:
            self.logger.pulse("Creating the commit")
            unique_id = uuid4().hex
            author_email = self.database.get_value("AUTHOR_EMAIL")
            author_name = self.database.get_value("AUTHOR_NAME")
            date = datetime.now()

            commit_id = self.database.create_commit(
                unique_id=unique_id,
                author_email=author_email,
                author_name=author_name,
                date=date,
                parent_commit_id=sprint.last_commit_id)
            self.logger.pulse("Created the commit")

            if commit_id:
                self.logger.pulse("Get blobs status")
                blob_status = self.blob_manager.get_blobs_status()
                self.logger.pulse("Got blobs status")

                self.logger.pulse("Checking changes")
                if not len(blob_status):
                    self.logger.info("No Changes to commit")
                    return None

                self.logger.pulse("Creating all blobs")
                files_blob_link = {}
                for file in blob_status.created + blob_status.modified:
                    self.logger.pulse(f"Creating {file} blob")
                    sha256 = self.file_manager.get_sha256(file)
                    blob = self.database.get_blob_by_sha256(sha256=sha256)

                    if blob:
                        files_blob_link[file] = blob.id
                    else:
                        abs_path = self.file_manager.get_absolute_path(file)
                        content = self.file_manager.compress_blob(abs_path)
                        blob_id = self.database.create_blob(sha256=sha256,
                                                            content=content)
                        if blob_id:
                            files_blob_link[file] = blob_id
                    self.logger.pulse(f"Creating {file} blob")
                self.logger.pulse("Created all blobs")

                self.logger.pulse("Creating commit blobs for new and modified")
                for path, blob_id in files_blob_link.items():
                    self.logger.pulse(f"Creating a commit blob for {path}")
                    self.database.create_commit_blob(path=path,
                                                     commit_id=commit_id,
                                                     blob_id=blob_id)
                    self.logger.pulse(f"Created a commit blob for {path}")
                self.logger.pulse("Created commit blobs for new and modified")

                self.logger.pulse("Creating commit blobs for deleted")
                for file in blob_status.deleted:
                    self.logger.pulse(f"Creating a commit blob for {path}")
                    self.database.create_commit_blob(path=file,
                                                     commit_id=commit_id,
                                                     blob_id=None)
                    self.logger.pulse(f"Creating a commit blob for {path}")
                self.logger.pulse("Created commit blobs for deleted")

                self.logger.pulse("Updating sprint last commit id")
                self.database.update_sprint(sprint_name=sprint.name,
                                            last_commit_id=commit_id)
                self.logger.pulse("Updated sprint last commit id")

                if len(blob_status) > 1:
                    self.logger.info(f"{len(blob_status)} changes have been "
                                     "committed successfully")
                else:
                    self.logger.info("1 change has been comitted successfully")
