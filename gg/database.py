from typing import List

import os
import sqlite3
import importlib.resources as resources

from gg.models import Blob
from gg.models import CommitBlob


class Database:
    def __init__(self, path: str) -> None:
        self.database = os.path.join(path, ".gg", "gg.db")

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database)

    def create_database(self) -> None:
        with self._get_connection() as connection:
            with resources.open_text("gg", "database.sql") as sql:
                connection.executescript(sql.read())
            connection.commit()

    def create_sprint(self,
                      sprint_name: str,
                      base_commit_id: int | None = None) -> None:
        with self._get_connection() as connection:
            connection.execute("""
                               INSERT INTO SPRINT(NAME,
                                                  BASE_COMMIT_ID,
                                                  LAST_COMMIT_ID)
                               VALUES (?, ?, ?)""", (sprint_name,
                                                     base_commit_id,
                                                     base_commit_id))
            connection.commit()

    def get_last_commit(self, sprint_name: str) -> str:
        with self._get_connection() as connection:
            cursor = connection.execute("""
                               SELECT LAST_COMMIT_ID
                               FROM SPRINT
                               WHERE NAME=? )""", (sprint_name))

            return cursor.fetchone()[0]

    def get_commit_blobs(self, commit_id: int) -> List[CommitBlob]:
        with self._get_connection() as connection:
            cursor = connection.execute("""
                                        SELECT COMMIT_ID, BLOB_ID, PATH
                                        FROM COMMIT_BLOB
                                        WHERE COMMIT_ID=?)""",
                                        (commit_id,))

            commit_blobs: List[CommitBlob] = []
            for record in cursor.fetchall():
                commit_blobs.append(
                    CommitBlob(commit_id=record[0],
                               blob_id=record[1],
                               path=record[2]))
            return commit_blobs

    def get_blob(self, blob_id: int) -> Blob:
        with self._get_connection() as connection:
            cursor = connection.execute("""
                                        SELECT ID, CONTENT, SHA256
                                        FROM BLOB
                                        WHERE ID=?)""",
                                        (blob_id,))

            record = cursor.fetchone()
            return Blob(id=record[0],
                        content=record[1],
                        sha256=record[2])

    def get_current_sprint(self) -> str:
        with self._get_connection() as connection:
            cursor = connection.execute("""
                                        SELECT CONFIG_VALUE
                                        FROM CONFIG
                                        WHERE CONFIG_KEY='CURRENT_SPRINT'""")
            return cursor.fetchone()[0]

    def update_current_sprint(self, sprint_name: str) -> None:
        with self._get_connection() as connection:
            connection.execute("""
                               UPDATE CONFIG
                               SET CONFIG_VALUE=?
                               WHERE CONFIG_KEY='CURRENT_SPRINT'""",
                               (sprint_name,))
