from typing import List

import os
import sqlite3
import importlib.resources as resources
from datetime import datetime

from gg.core.models import Blob
from gg.core.models import CommitBlob
from gg.core.models import Sprint
from gg.core.models import Commit
from gg.core.path import Path


class Database:
    def __init__(self) -> None:
        path = Path.get_root_path()
        self.database = os.path.join(path, ".gg", "gg.db")

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database)

    def create_database(self) -> None:
        with self._get_connection() as connection:
            with resources.open_text("gg", "database.sql") as sql:
                connection.executescript(sql.read())
            connection.commit()

    def create_blob(self, content: bytes, sha256: str) -> int | None:
        with self._get_connection() as connection:
            cursor = connection.execute("""
                                        INSERT INTO BLOB(CONTENT, SHA256)
                                        VALUES(?, ?)
                                        """, (content, sha256))
            connection.commit()
            return cursor.lastrowid

    def get_blob(self, blob_id: int) -> Blob | None:
        with self._get_connection() as connection:
            cursor = connection.execute("""
                                        SELECT ID, CONTENT, SHA256
                                        FROM BLOB
                                        WHERE ID=?""",
                                        (blob_id,))

            record = cursor.fetchone()
            if record:
                return Blob(id=record[0],
                            content=record[1],
                            sha256=record[2])
            return None

    def get_blob_by_sha256(self, sha256: str) -> Blob | None:
        with self._get_connection() as connection:
            cursor = connection.execute("""
                                        SELECT ID, CONTENT, SHA256
                                        FROM BLOB
                                        WHERE SHA256=?""",
                                        (sha256,))
            record = cursor.fetchone()
            if record:
                return Blob(id=record[0],
                            content=record[1],
                            sha256=record[2])
            return None

    def get_commit(self,
                   id: int | None = -1,
                   unique_id: str | None = "") -> Commit | None:
        with self._get_connection() as connection:
            cursor = connection.execute("""
                                        SELECT ID, UNIQUE_ID, AUTHOR_EMAIL,
                                        AUTHOR_NAME, DATE, PARENT_COMMIT_ID
                                        FROM `COMMIT`
                                        WHERE ID=? OR UNIQUE_ID=?
                                        """, (id, unique_id))

            record = cursor.fetchone()
            if record:
                return Commit(id=record[0],
                              unique_id=record[1],
                              author_email=record[2],
                              author_name=record[3],
                              date=record[4],
                              parent_commit_id=record[5])
            return None

    def create_commit(self,
                      unique_id: str,
                      author_email: str,
                      author_name: str,
                      date: datetime,
                      parent_commit_id: int) -> int | None:
        with self._get_connection() as connection:
            cursor = connection.execute("""
                                        INSERT INTO `COMMIT`(UNIQUE_ID,
                                        AUTHOR_EMAIL,AUTHOR_NAME, DATE,
                                        PARENT_COMMIT_ID)
                                        VALUES(?, ?, ?, ?, ?)""",
                                        (unique_id, author_email,
                                         author_name, date, parent_commit_id))
            connection.commit()
            return cursor.lastrowid

    def create_commit_blob(self,
                           commit_id: int,
                           blob_id: int | None,
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
                                        WHERE COMMIT_ID=?""",
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

    def get_sprint_by_base_commit(self, base_commit_id: int) -> Sprint | None:

        with self._get_connection() as connection:
            cursor = connection.execute("""
                               SELECT ID, NAME, BASE_COMMIT_ID,
                               LAST_COMMIT_ID
                               FROM SPRINT
                               WHERE LAST_COMMIT_ID=?
                               """, (base_commit_id,))
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

    def update_sprint(self,
                      sprint_name: str,
                      last_commit_id: int) -> None:
        with self._get_connection() as connection:
            connection.execute("""
                               UPDATE SPRINT
                               SET LAST_COMMIT_ID=?
                               WHERE NAME=?
                               """, (last_commit_id, sprint_name))
            connection.commit()

    def get_value(self, key: str) -> str:
        with self._get_connection() as connection:
            cursor = connection.execute("""
                                        SELECT CONFIG_VALUE
                                        FROM CONFIG
                                        WHERE CONFIG_KEY=?""",
                                        (key,))
            return cursor.fetchone()[0]

    def update_value(self, key: str, value: str) -> None:
        with self._get_connection() as connection:
            connection.execute("""
                               UPDATE CONFIG
                               SET CONFIG_VALUE=?
                               WHERE CONFIG_KEY=?""",
                               (value, key,))
            connection.commit()
