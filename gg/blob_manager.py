from typing import List


class BlobManager:
    def __init__(self, tree_path) -> None:
        self.tree_path = tree_path

    def _get_modified_blobs(self) -> List[str]:
        return []
