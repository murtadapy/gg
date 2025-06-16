from typing import List

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime


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


@dataclass
class Sprint:
    id: int
    name: str
    base_commit_id: int
    last_commit_id: int


@dataclass
class Commit:
    id: int
    unique_id: str
    author_email: str
    author_name: str
    date: datetime
    parent_commit_id: int


@dataclass
class BlobStatus:
    created: List[str] = field(default_factory=list)
    modified: List[str] = field(default_factory=list)
    deleted: List[str] = field(default_factory=list)
    unchanged: List[str] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.created +
                   self.modified +
                   self.deleted)
