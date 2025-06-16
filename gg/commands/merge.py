from gg.base import CommandBase
from gg.core.database import Database
from gg.core.file_manager import FileManager
from gg.core.blob_manager import BlobManager
from gg.core.logger import Logger


class MergeCommand(CommandBase):
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
            self.logger.pulse("Updating last commit of base sprint")
            base_sprint = self.database.get_sprint_by_base_commit(
                sprint.base_commit_id)

            if base_sprint:
                self.database.update_sprint(
                    sprint_name=base_sprint.name,
                    last_commit_id=sprint.last_commit_id)

                self.logger.pulse("Updated last commit of base sprint")

                self.logger.info(f"Merged {sprint.name} to {base_sprint.name}")
                return None

            self.logger.info(f"Couldn't merge {sprint.name} to its base")
