from typing import List
from typing import Set

import os
import pathlib
import hashlib
import io
import gzip


from gg.path import Path


class FileManager:
    def __init__(self) -> None:
        self.tree_path = Path.get_root_path()
        self.gg_path = os.path.join(self.tree_path, ".gg")

    def check_if_repository_exists(self) -> bool:
        return os.path.exists(self.gg_path)

    def get_ignored_entities(self) -> Set[str]:
        ignored_enitites: Set[str] = set({".gg"})
        ggignore_path = os.path.join(self.tree_path, ".ggignore")
        if os.path.exists(ggignore_path):
            with open(os.path.join(self.tree_path, ".ggignore")) as f:
                for line in f.readlines():
                    ignored_enitites.add(line.strip("\n"))
        return ignored_enitites

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
                    file_path = pathlib.Path(os.path.join(root, file))
                    relative_path = file_path.relative_to(self.tree_path)
                    all_files.append(relative_path.as_posix())
        return all_files

    def compress_blob(self, path: str) -> bytes:
        with open(path, 'rb') as file:
            out = io.BytesIO()
            with gzip.GzipFile(fileobj=out, mode="wb") as zip:
                zip.write(file.read())
            return out.getvalue()

    def get_absolute_path(self, relative_path: str) -> str:
        return os.path.join(self.tree_path, relative_path)
