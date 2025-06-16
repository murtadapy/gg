from gg.base import CommandBase
from gg.database import Database
from gg.file_manager import FileManager
from gg.blob_manager import BlobManager
from gg.logger import Logger


class SprintCommand(CommandBase):
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
        self.logger.pulse("Executing sprint command")

        self.logger.pulse("Checking if repository exist")
        if not self.file_manager.check_if_repository_exists():
            self.logger.info("This is not a gg repository")
            return

        self.logger.pulse("Get current sprint")
        sprint_name = self.database.get_value("CURRENT_SPRINT")
        sprint = self.database.get_sprint(sprint_name=sprint_name)
        self.logger.pulse("Got the current sprint")

        if sprint:
            self.logger.pulse(f"Creating {self.sprint_name} sprint")
            self.database.create_sprint(sprint_name=self.sprint_name,
                                        base_commit_id=sprint.last_commit_id)
            self.logger.pulse(f"Created {self.sprint_name} sprint")

            self.logger.pulse(f"Switching to the {self.sprint_name} sprint")
            self.database.update_value("CURRENT_SPRINT", self.sprint_name)
            self.logger.pulse(f"Switched to the {self.sprint_name} sprint")

        self.logger.info(f"Switched to {self.sprint_name}")
