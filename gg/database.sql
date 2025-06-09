PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS blobs (
    id TEXT PRIMARY KEY,
    content BLOB NOT NULL
);

CREATE TABLE IF NOT EXISTS commits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uniqueId TEXT NOT NULL,
    authorEmail TEXT NOT NULL,
    authorName TEXT NOT NULL,
    date TEXT NOT NULL,
    parentCommitId INTEGER,
    FOREIGN KEY(parentCommitId) REFERENCES commits(id)
);

CREATE TABLE IF NOT EXISTS commit_blobs (
    commitId INTEGER NOT NULL,
    blobId TEXT NOT NULL,
    path TEXT NOT NULL,
    PRIMARY KEY (commitId, path),
    FOREIGN KEY(commitId) REFERENCES commits(id),
    FOREIGN KEY(blobId) REFERENCES blobs(id)
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS sprints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    baseCommitId INTEGER,
    FOREIGN KEY(baseCommitId) REFERENCES commits(id)
);

CREATE TABLE IF NOT EXISTS sprint_blobs (
    sprintId INTEGER NOT NULL,
    blobId TEXT NOT NULL,
    path TEXT NOT NULL,
    PRIMARY KEY (sprintId, path),
    FOREIGN KEY(sprintId) REFERENCES sprints(id),
    FOREIGN KEY(blobId) REFERENCES blobs(id)
) WITHOUT ROWID;