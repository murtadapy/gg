from typing import List
from typing import Set

import os
import sys
import pathlib
import hashlib


class FileManager:
    def __init__(self, path: str) -> None:
        self.tree_path = path
        self.gg_path = os.path.join(path, ".gg")

    def check_if_repository_exists(self) -> bool:
        return os.path.exists(self.gg_path)

    def get_ignored_entities(self) -> Set[str]:
        ggignore_path = os.path.join(self.tree_path, ".ggignore")
        if os.path.exists(ggignore_path):
            with open(os.path.join(self.tree_path, ".ggignore")) as f:
                return {x.strip("\n") for x in f.readlines()}
        return set()

    def get_sha256(self, path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(path, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(block)
        return sha256_hash.hexdigest()

    def get_all_files(self) -> List[str]:
        all_files: List[str] = []
        ignored_entities = self.get_ignored_entities()
        for root, dirs, files in os.walk(self.tree_path):
            dirs[:] = [x for x in dirs if x not in ignored_entities]
            for file in files:
                if file not in ignored_entities:
                    root_path = sys.path[0]
                    file_path = pathlib.Path(os.path.join(root, file))
                    relative_path = file_path.relative_to(root_path).as_posix()
                    all_files.append(relative_path)
        return all_files
