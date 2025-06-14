from typing import List

import os
import sqlite3
import importlib.resources as resources
from datetime import datetime

from gg.models import Blob
from gg.models import CommitBlob
from gg.models import Sprint
from gg.models import Commit


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

    def create_blob(self, id: int, content: bytes, sha256: str) -> None:
        with self._get_connection() as connection:
            connection.execute("""
                               INSERT INTO BLOB(ID, CONTENT, SHA256)
                               VALUES(?, ?, ?)
                               """, (id, content, sha256))
            connection.commit()

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

    def get_commit(self,
                   id: int | None = -1,
                   unique_id: str | None = "") -> Commit:
        with self._get_connection() as connection:
            cursor = connection.execute("""
                                        SELECT ID, UNQIUE_ID, AUTHOR_EMAIL
                                        AUTHOR_NAME, DATE, PARENT_COMMIT_ID
                                        FROM COMMIT
                                        WHERE ID=? OR UNQIUE_ID=?
                                        """, (id, unique_id))
            record = cursor.fetchone()
            return Commit(id=record[0],
                          unique_id=record[1],
                          author_email=record[2],
                          author_name=record[3],
                          date=record[4],
                          parent_commit_id=record[5])

    def create_commit(self,
                      id: int,
                      unique_id: str,
                      author_email: str,
                      author_name: str,
                      date: datetime,
                      parent_commit_id: int) -> None:
        with self._get_connection() as connection:
            connection.execute("""
                               INSERT INTO COMMIT(ID, UNIQUE_ID, AUTHOR_EMAIL,
                                           AUTHOR_NAME, DATE, PARENT_COMMIT_ID)
                               VALUES(?, ?, ?, ?, ?, ?)""",
                               (id, unique_id, author_email,
                                author_name, date, parent_commit_id))
            connection.commit()

    def create_commit_blob(self,
                           commit_id: int,
                           blob_id: str,
                           path: str) -> None:
        with self._get_connection() as connection:
            connection.execute("""
                               INSERT INTO COMMIT_BLOB(COMMIT_ID, BLOB_ID,
                               PATH) VALUES(?, ?, ?)""",
                               (commit_id, blob_id, path))
            connection.commit()

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

    def get_sprint(self,
                   sprint_id: int | None = -1,
                   sprint_name: str | None = "") -> Sprint | None:
        with self._get_connection() as connection:
            cursor = connection.execute("""
                               SELECT ID, NAME, BASE_COMMIT_ID,
                               LAST_COMMIT_ID
                               FROM SPRINT
                               WHERE ID=? OR NAME=?
                               """, (sprint_id, sprint_name))
            record = cursor.fetchone()
            if record:
                return Sprint(id=record[0],
                              name=record[1],
                              base_commit_id=record[2],
                              last_commit_id=record[3])
            return None

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

    def get_active_sprint(self) -> str:
        with self._get_connection() as connection:
            cursor = connection.execute("""
                                        SELECT CONFIG_VALUE
                                        FROM CONFIG
                                        WHERE CONFIG_KEY='CURRENT_SPRINT'""")
            return cursor.fetchone()[0]

    def update_active_sprint(self, sprint_name: str) -> None:
        with self._get_connection() as connection:
            connection.execute("""
                               UPDATE CONFIG
                               SET CONFIG_VALUE=?
                               WHERE CONFIG_KEY='CURRENT_SPRINT'""",
                               (sprint_name,))
