from dataclasses import dataclass
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
