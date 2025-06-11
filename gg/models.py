from dataclasses import dataclass


@dataclass
class Blob:
    id: int
    content: bytes
    sha256: str


@dataclass
class CommitBlob:
    commit_id: int
    blob_id: int
    path: str
