from typing import List

import os
import hashlib


class FileManager:
    def __init__(self, path: str) -> None:
        self.tree_path = path
        self.gg_path = os.path.join(path, ".gg")

    def check_if_repository_exists(self) -> bool:
        return os.path.exists(self.gg_path)

    def get_sha256(self, path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(path, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(block)
        return sha256_hash.hexdigest()

    def get_all_files(self) -> List[str]:
        return []
