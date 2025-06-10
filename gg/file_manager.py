import os


class FileManager:
    def __init__(self, path: str) -> None:
        self.path = path

    def check_if_repository_exists(self) -> bool:
        return os.path.exists(self.path)
